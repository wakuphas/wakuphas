import os
import sys
from datetime import datetime
from urllib.parse import urlparse

import paramiko
import requests

# ==============================================================================
# SGLI Granule ID 取得 & G-Portal SFTPダウンロードスクリプト
#
# 機能:
#   1. G-Portal CSW APIを使って、指定条件に合うSGLIのgranule IDを検索
#   2. 見つかったファイルをG-PortalのSFTPサーバからダウンロード
#
# G-Portal SFTP接続情報:
#   ホスト: ftp.gportal.jaxa.jp
#   ポート: 2051
#   認証:   ユーザ名/パスワード
# ==============================================================================

# ── SFTP接続設定 ──────────────────────────────────────────────────
SFTP_HOST = "ftp.gportal.jaxa.jp"
SFTP_PORT = 2051
SFTP_USER = os.getenv("GPORTAL_SFTP_USER", "")
SFTP_PASSWORD = os.getenv("GPORTAL_SFTP_PASSWORD", "")

# ── CSW APIページング設定 ─────────────────────────────────────────
MAX_PER_PAGE = 20
MAX_TOTAL = 100


def _validate_credentials():
    if SFTP_USER and SFTP_PASSWORD:
        return

    print("[ERROR] SFTP認証情報が未設定です。")
    print("        環境変数 GPORTAL_SFTP_USER と GPORTAL_SFTP_PASSWORD を設定してください。")
    sys.exit(1)


# ──────────────────────────────────────────────────────────────────
# CSW API: 全レコードをページングしながら取得
# ──────────────────────────────────────────────────────────────────
def fetch_all_records(base_url, max_per_page=MAX_PER_PAGE, max_total=MAX_TOTAL):
    all_features = []
    start_pos = 1

    while len(all_features) < max_total:
        paged_url = f"{base_url}&startPosition={start_pos}"
        print(f"[INFO] Fetching startPosition={start_pos} ...")
        response = requests.get(paged_url)
        if response.status_code != 200:
            print("[ERROR] G-Portal CSW APIへのアクセスに失敗しました。")
            break

        data = response.json()
        features = data.get("features", [])
        if not features:
            break

        all_features.extend(features)
        print(f"[INFO] {len(features)} 件取得 (合計: {len(all_features)} 件)")

        if len(features) < max_per_page:
            break
        start_pos += max_per_page

        if len(all_features) >= max_total:
            print(f"[INFO] 上限 {max_total} 件に達したため取得を停止します。")
            break

    return all_features[:max_total]


# ──────────────────────────────────────────────────────────────────
# CSW API: 物理量・軌道・日付・バウンディングボックスでgranuleを検索
# ──────────────────────────────────────────────────────────────────
def search_granules(quantity, orbit_code, date_str, lat_ll, lon_ll, lat_ur, lon_ur):
    """
    G-Portal CSW APIを使ってgranuleを検索し、
    {file_name: sftp_path} の辞書を返す。
    """
    orbit_dir_map = {"A": "Ascending", "D": "Descending"}
    orbit_dir = orbit_dir_map.get(orbit_code.upper())
    if orbit_dir is None:
        print("[ERROR] 軌道方向は 'A'(昇交点) または 'D'(降交点) を指定してください。")
        sys.exit(1)

    date = datetime.strptime(date_str, "%Y%m%d")
    start_time = date.strftime("%Y-%m-%dT00:00:00Z")
    end_time = date.strftime("%Y-%m-%dT23:59:59Z")

    base_url = (
        "https://gportal.jaxa.jp/csw/csw"
        "?service=CSW&version=3.0.0&request=GetRecords"
        f"&startTime={start_time}"
        f"&endTime={end_time}"
        f"&bbox={lon_ll},{lat_ll},{lon_ur},{lat_ur}"
        "&sat=GCOM-C"
        f"&q={quantity}"
        f"&orbitDirection={orbit_dir}"
        "&outputFormat=application/json"
        f"&maxRecords={MAX_PER_PAGE}"
    )

    print("[INFO] 検索URL:")
    print(base_url)
    print()

    features = fetch_all_records(base_url)
    print(f"[INFO] 合計 {len(features)} 件のgranuleが見つかりました。\n")

    granule_map = {}
    for feat in features:
        props = feat.get("properties", {})
        file_url = props.get("product", {}).get("fileName", "")
        if not file_url:
            continue

        file_name = file_url.split("/")[-1]

        if "X0000" in file_name:
            print(f"[SKIP] X0000を含むため除外: {file_name}")
            continue

        sftp_path = extract_sftp_path(file_url)
        granule_map[file_name] = sftp_path

    return granule_map


# ──────────────────────────────────────────────────────────────────
# CSWの fileName URL → SFTPサーバ上のパスに変換
# ──────────────────────────────────────────────────────────────────
def extract_sftp_path(file_url):
    """
    G-Portal CSWが返す fileName URL からSFTPパスを抽出する。

    パターン1 (推奨): URL内に /standard/ が含まれる場合
      https://gportal.jaxa.jp/gpr/product/standard/GCOM-C/.../file.h5
      → /standard/GCOM-C/.../file.h5

    パターン2: /gpr/product/ 以降のパス
      https://gportal.jaxa.jp/gpr/product/...
      → /...

    パターン3: フォールバック (パスが取得できない場合はファイル名のみ)
    """
    parsed = urlparse(file_url)
    path = parsed.path

    if "/standard/" in path:
        return path[path.index("/standard/") :]

    if "/gpr/product/" in path:
        return path[len("/gpr/product") :]

    return path


# ──────────────────────────────────────────────────────────────────
# SFTP接続 & ファイルダウンロード
# ──────────────────────────────────────────────────────────────────
def download_via_sftp(granule_map, output_dir="."):
    """
    granule_map: {ファイル名: SFTPサーバ上のパス}
    output_dir : ダウンロード先ローカルディレクトリ
    """
    if not granule_map:
        print("[WARN] ダウンロード対象のgranuleがありません。")
        return

    _validate_credentials()
    os.makedirs(output_dir, exist_ok=True)

    print(f"[INFO] SFTP接続中: {SFTP_HOST}:{SFTP_PORT} (ユーザ: {SFTP_USER})")

    transport = None
    sftp = None
    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("[INFO] SFTP接続成功\n")

        success_list = []
        fail_list = []

        for file_name, sftp_path in granule_map.items():
            local_path = os.path.join(output_dir, file_name)

            if os.path.exists(local_path):
                print(f"[SKIP] 既に存在します: {file_name}")
                success_list.append(file_name)
                continue

            print(f"[DL]   {sftp_path}")
            print(f"       → {local_path}")

            try:
                sftp.get(sftp_path, local_path, callback=_progress_callback(file_name))
                print()
                success_list.append(file_name)
                print(f"[OK]   ダウンロード完了: {file_name}\n")
            except FileNotFoundError:
                print(f"\n[ERROR] SFTPサーバにファイルが見つかりません: {sftp_path}")
                fail_list.append((file_name, "FileNotFound"))
            except PermissionError:
                print(f"\n[ERROR] アクセス権限がありません: {sftp_path}")
                fail_list.append((file_name, "PermissionError"))
            except Exception as e:
                print(f"\n[ERROR] ダウンロード失敗 ({file_name}): {e}")
                fail_list.append((file_name, str(e)))
                if os.path.exists(local_path):
                    os.remove(local_path)

        print("=" * 60)
        print(f"[SUMMARY] 成功: {len(success_list)} 件 / 失敗: {len(fail_list)} 件")
        if fail_list:
            print("[SUMMARY] 失敗ファイル一覧:")
            for fn, reason in fail_list:
                print(f"  - {fn} ({reason})")
        print("=" * 60)

    except paramiko.AuthenticationException:
        print("[ERROR] SFTP認証に失敗しました。ユーザ名・パスワードを確認してください。")
        sys.exit(1)
    except paramiko.SSHException as e:
        print(f"[ERROR] SFTP接続エラー: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 予期しないエラー: {e}")
        sys.exit(1)
    finally:
        if sftp:
            sftp.close()
        if transport:
            transport.close()
        print("[INFO] SFTP接続を切断しました。")


def _progress_callback(file_name):
    """SFTPダウンロードの進捗を表示するコールバック関数を返す（5%刻みで更新）"""
    last_pct = [-1]

    def callback(transferred, total):
        if total <= 0:
            return
        pct = transferred / total * 100
        step = int(pct // 5)
        if step == last_pct[0] and pct < 100:
            return
        last_pct[0] = step

        bar_len = 30
        filled = int(bar_len * transferred / total)
        bar = "#" * filled + "-" * (bar_len - filled)
        mb_done = transferred / 1024 / 1024
        mb_total = total / 1024 / 1024
        print(
            f"\r  [{bar}] {pct:5.1f}%  {mb_done:.1f}/{mb_total:.1f} MB",
            end="",
            flush=True,
        )

    return callback


# ──────────────────────────────────────────────────────────────────
# メイン
# ──────────────────────────────────────────────────────────────────
def main():
    auto_mode = "--auto" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--auto"]

    if len(args) < 7:
        print("使い方:")
        print("  python get_sgli_granuleID_and_file.py <物理量> <軌道> <日付YYYYMMDD> <lat_ll> <lon_ll> <lat_ur> <lon_ur> [出力ディレクトリ] [--auto]")
        print()
        print("例:")
        print("  python get_sgli_granuleID_and_file.py SST D 20250702 35 135 45 150")
        print("  python get_sgli_granuleID_and_file.py NDVIF D 20250701 0 0 0 0 ./download")
        print("  python get_sgli_granuleID_and_file.py IWPRK D 20210710 35.0 139.5 35.8 140.2 ./download")
        print("  python get_sgli_granuleID_and_file.py SST_Q D 20250702 35 135 45 150 ./download --auto")
        print()
        print("引数:")
        print("  <物理量>            物理量コード (例: SST, SST_Q, NDVIF, CHL)")
        print("  <軌道>          軌道方向 A=昇交点 / D=降交点")
        print("  <日付YYYYMMDD>  対象日付 (例: 20250702)")
        print("  <lat_ll>        バウンディングボックス 南緯 (度)")
        print("  <lon_ll>        バウンディングボックス 西経 (度)")
        print("  <lat_ur>        バウンディングボックス 北緯 (度)")
        print("  <lon_ur>        バウンディングボックス 東経 (度)")
        print("  [出力ディレクトリ]  省略時はカレントディレクトリ")
        print("  [--auto]        確認プロンプトをスキップして自動DL")
        sys.exit(1)

    quantity = args[0].upper()
    orbit_code = args[1].upper()
    yyyymmdd = args[2]
    lat_ll = float(args[3])
    lon_ll = float(args[4])
    lat_ur = float(args[5])
    lon_ur = float(args[6])
    output_dir = args[7] if len(args) >= 8 else "."

    print("=" * 60)
    print(" SGLI Granule 検索 & ダウンロード")
    print("=" * 60)
    print(f"  物理量    : {quantity}")
    print(f"  軌道方向  : {orbit_code} ({'昇交点' if orbit_code == 'A' else '降交点'})")
    print(f"  日付      : {yyyymmdd}")
    print(f"  範囲(緯度): {lat_ll}° 〜 {lat_ur}°")
    print(f"  範囲(経度): {lon_ll}° 〜 {lon_ur}°")
    print(f"  出力先    : {output_dir}")
    print(f"  自動DL    : {'ON' if auto_mode else 'OFF'}")
    print("=" * 60)
    print()

    granule_map = search_granules(quantity, orbit_code, yyyymmdd, lat_ll, lon_ll, lat_ur, lon_ur)

    print("[INFO] 取得ファイル一覧:")
    for fn, path in granule_map.items():
        print(f"  {fn}")
        print(f"    SFTP: {path}")
    print()

    if not granule_map:
        print("[INFO] 該当するgranuleが見つかりませんでした。終了します。")
        sys.exit(0)

    if not auto_mode:
        try:
            answer = input(f"上記 {len(granule_map)} 件をダウンロードしますか？ [yes/no]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n[INFO] キャンセルしました。")
            sys.exit(0)

        if answer not in ("yes", "y"):
            print("[INFO] ダウンロードをキャンセルしました。")
            sys.exit(0)
    else:
        print(f"[INFO] 自動DLモード: {len(granule_map)} 件のダウンロードを開始します。")

    download_via_sftp(granule_map, output_dir=output_dir)


if __name__ == "__main__":
    main()
