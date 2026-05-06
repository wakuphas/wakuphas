import os
import sys
from datetime import datetime
from urllib.parse import urlparse

import paramiko
import requests

# ==============================================================================
# SGLI Granule ID search and G-Portal SFTP download script
#
# Features:
#   1. Search for SGLI granule IDs using the G-Portal CSW API
#   2. Download matched files from the G-Portal SFTP server
#
# G-Portal SFTP connection:
#   Host: ftp.gportal.jaxa.jp
#   Port: 2051
#   Auth: username/password
# ==============================================================================

# ── SFTP connection settings ─────────────────────────────────────
SFTP_HOST = "ftp.gportal.jaxa.jp"
SFTP_PORT = 2051
SFTP_USER = os.getenv("GPORTAL_SFTP_USER", "")
SFTP_PASSWORD = os.getenv("GPORTAL_SFTP_PASSWORD", "")

# ── CSW API paging settings ──────────────────────────────────────
MAX_PER_PAGE = 20
MAX_TOTAL = 100


def _validate_credentials():
    if SFTP_USER and SFTP_PASSWORD:
        return

    print("[ERROR] SFTP credentials are not set.")
    print("        Set the GPORTAL_SFTP_USER and GPORTAL_SFTP_PASSWORD environment variables.")
    sys.exit(1)


# ──────────────────────────────────────────────────────────────────
# CSW API: fetch all records with pagination
# ──────────────────────────────────────────────────────────────────
def fetch_all_records(base_url, max_per_page=MAX_PER_PAGE, max_total=MAX_TOTAL):
    all_features = []
    start_pos = 1

    while len(all_features) < max_total:
        paged_url = f"{base_url}&startPosition={start_pos}"
        print(f"[INFO] Fetching startPosition={start_pos} ...")
        response = requests.get(paged_url)
        if response.status_code != 200:
            print("[ERROR] Failed to access the G-Portal CSW API.")
            break

        data = response.json()
        features = data.get("features", [])
        if not features:
            break

        all_features.extend(features)
        print(f"[INFO] Retrieved {len(features)} records (total: {len(all_features)})")

        if len(features) < max_per_page:
            break
        start_pos += max_per_page

        if len(all_features) >= max_total:
            print(f"[INFO] Reached the upper limit of {max_total} records. Stopping fetch.")
            break

    return all_features[:max_total]


# ──────────────────────────────────────────────────────────────────
# CSW API: search granules by quantity, orbit, date, and bounding box
# ──────────────────────────────────────────────────────────────────
def search_granules(quantity, orbit_code, date_str, lat_ll, lon_ll, lat_ur, lon_ur):
    """
    Search granules using the G-Portal CSW API and return
    a dictionary in the form {file_name: sftp_path}.
    """
    orbit_dir_map = {"A": "Ascending", "D": "Descending"}
    orbit_dir = orbit_dir_map.get(orbit_code.upper())
    if orbit_dir is None:
        print("[ERROR] Orbit direction must be 'A' (Ascending) or 'D' (Descending).")
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

    print("[INFO] Search URL:")
    print(base_url)
    print()

    features = fetch_all_records(base_url)
    print(f"[INFO] Found {len(features)} granules in total.\n")

    granule_map = {}
    for feat in features:
        props = feat.get("properties", {})
        file_url = props.get("product", {}).get("fileName", "")
        if not file_url:
            continue

        file_name = file_url.split("/")[-1]

        if "X0000" in file_name:
            print(f"[SKIP] Excluded because it contains X0000: {file_name}")
            continue

        sftp_path = extract_sftp_path(file_url)
        granule_map[file_name] = sftp_path

    return granule_map


# ──────────────────────────────────────────────────────────────────
# Convert a CSW fileName URL to an SFTP server path
# ──────────────────────────────────────────────────────────────────
def extract_sftp_path(file_url):
    """
    Extract an SFTP path from the fileName URL returned by G-Portal CSW.

    Pattern 1 (preferred): the URL contains /standard/
      https://gportal.jaxa.jp/gpr/product/standard/GCOM-C/.../file.h5
      → /standard/GCOM-C/.../file.h5

    Pattern 2: use the path after /gpr/product/
      https://gportal.jaxa.jp/gpr/product/...
      → /...

    Pattern 3: fallback to the parsed path as-is
    """
    parsed = urlparse(file_url)
    path = parsed.path

    if "/standard/" in path:
        return path[path.index("/standard/") :]

    if "/gpr/product/" in path:
        return path[len("/gpr/product") :]

    return path


# ──────────────────────────────────────────────────────────────────
# SFTP connection and file download
# ──────────────────────────────────────────────────────────────────
def download_via_sftp(granule_map, output_dir="."):
    """
    granule_map: {file_name: path_on_sftp_server}
    output_dir : local download directory
    """
    if not granule_map:
        print("[WARN] No granules available for download.")
        return

    _validate_credentials()
    os.makedirs(output_dir, exist_ok=True)

    print(f"[INFO] Connecting to SFTP: {SFTP_HOST}:{SFTP_PORT} (user: {SFTP_USER})")

    transport = None
    sftp = None
    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("[INFO] SFTP connection established successfully.\n")

        success_list = []
        fail_list = []

        for file_name, sftp_path in granule_map.items():
            local_path = os.path.join(output_dir, file_name)

            if os.path.exists(local_path):
                print(f"[SKIP] Already exists: {file_name}")
                success_list.append(file_name)
                continue

            print(f"[DL]   {sftp_path}")
            print(f"       → {local_path}")

            try:
                sftp.get(sftp_path, local_path, callback=_progress_callback(file_name))
                print()
                success_list.append(file_name)
                print(f"[OK]   Download completed: {file_name}\n")
            except FileNotFoundError:
                print(f"\n[ERROR] File not found on the SFTP server: {sftp_path}")
                fail_list.append((file_name, "FileNotFound"))
            except PermissionError:
                print(f"\n[ERROR] Permission denied: {sftp_path}")
                fail_list.append((file_name, "PermissionError"))
            except Exception as e:
                print(f"\n[ERROR] Download failed ({file_name}): {e}")
                fail_list.append((file_name, str(e)))
                if os.path.exists(local_path):
                    os.remove(local_path)

        print("=" * 60)
        print(f"[SUMMARY] Success: {len(success_list)} / Failed: {len(fail_list)}")
        if fail_list:
            print("[SUMMARY] Failed files:")
            for fn, reason in fail_list:
                print(f"  - {fn} ({reason})")
        print("=" * 60)

    except paramiko.AuthenticationException:
        print("[ERROR] SFTP authentication failed. Check the username and password.")
        sys.exit(1)
    except paramiko.SSHException as e:
        print(f"[ERROR] SFTP connection error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        sys.exit(1)
    finally:
        if sftp:
            sftp.close()
        if transport:
            transport.close()
        print("[INFO] SFTP connection closed.")


def _progress_callback(file_name):
    """Return a callback that prints SFTP download progress in 5 percent steps."""
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
# Main
# ──────────────────────────────────────────────────────────────────
def main():
    auto_mode = "--auto" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--auto"]

    if len(args) < 7:
        print("Usage:")
        print("  python get_sgli_granuleID_and_file.py <quantity> <orbit> <date_yyyymmdd> <lat_ll> <lon_ll> <lat_ur> <lon_ur> [output_dir] [--auto]")
        print()
        print("Examples:")
        print("  python get_sgli_granuleID_and_file.py SST D 20250702 35 135 45 150")
        print("  python get_sgli_granuleID_and_file.py NDVIF D 20250701 0 0 0 0 ./download")
        print("  python get_sgli_granuleID_and_file.py IWPRK D 20210710 35.0 139.5 35.8 140.2 ./download")
        print("  python get_sgli_granuleID_and_file.py SST_Q D 20250702 35 135 45 150 ./download --auto")
        print()
        print("Arguments:")
        print("  <quantity>       Quantity code (e.g. SST, SST_Q, NDVIF, CHL)")
        print("  <orbit>          Orbit direction: A=Ascending / D=Descending")
        print("  <date_yyyymmdd>  Target date (e.g. 20250702)")
        print("  <lat_ll>         Bounding box lower latitude (degrees)")
        print("  <lon_ll>         Bounding box lower longitude (degrees)")
        print("  <lat_ur>         Bounding box upper latitude (degrees)")
        print("  <lon_ur>         Bounding box upper longitude (degrees)")
        print("  [output_dir]     Output directory, defaults to the current directory")
        print("  [--auto]         Skip the confirmation prompt and start downloading automatically")
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
    print(" SGLI Granule Search & Download")
    print("=" * 60)
    print(f"  Quantity   : {quantity}")
    print(f"  Orbit      : {orbit_code} ({'Ascending' if orbit_code == 'A' else 'Descending'})")
    print(f"  Date       : {yyyymmdd}")
    print(f"  Latitude   : {lat_ll}° to {lat_ur}°")
    print(f"  Longitude  : {lon_ll}° to {lon_ur}°")
    print(f"  Output dir : {output_dir}")
    print(f"  Auto mode  : {'ON' if auto_mode else 'OFF'}")
    print("=" * 60)
    print()

    granule_map = search_granules(quantity, orbit_code, yyyymmdd, lat_ll, lon_ll, lat_ur, lon_ur)

    print("[INFO] Retrieved files:")
    for fn, path in granule_map.items():
        print(f"  {fn}")
        print(f"    SFTP: {path}")
    print()

    if not granule_map:
        print("[INFO] No matching granules were found. Exiting.")
        sys.exit(0)

    if not auto_mode:
        try:
            answer = input(f"Download the {len(granule_map)} files listed above? [yes/no]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n[INFO] Cancelled.")
            sys.exit(0)

        if answer not in ("yes", "y"):
            print("[INFO] Download cancelled.")
            sys.exit(0)
    else:
        print(f"[INFO] Auto-download mode: starting download for {len(granule_map)} files.")

    download_via_sftp(granule_map, output_dir=output_dir)


if __name__ == "__main__":
    main()
