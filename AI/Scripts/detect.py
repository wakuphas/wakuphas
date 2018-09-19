from darkflow.net.build import TFNet
import cv2
import numpy as np

# model, weights, labelsをロード
options = {"model": "cfg/yolo-obj.cfg", "load": "backup/yolo-obj_500.weights", "threshold": 0.01, "labels": "labels_airplane.txt"}
tfnet = TFNet(options)
print("Model loading ... success!")

# 画像の読み込み
img = cv2.imread('test_airport.jpg')

# 解析を行う
items = tfnet.return_predict(img)
print("Analyzing ... success!")

# 検出できたものを確認
#print(items)

# class nameをすべて記述する
class_names = ['airplane']

count = 0

for item in items:
    # 四角を描くのに必要な情報とラベルを取り出す
    tlx = item['topleft']['x']
    tly = item['topleft']['y']
    brx = item['bottomright']['x']
    bry = item['bottomright']['y']
    label = item['label']
    conf = item['confidence']

    # 自信のあるものを表示
    if conf >= 0.1:

        for i in class_names:
            if label == i:
                #print ("\n", i)
                class_num = class_names.index(i)
                # airplane の数をカウント
                if i == "airplane":
                    count += 1
        
            # 検出位置の表示
            cv2.rectangle(img, (tlx, tly), (brx, bry), (200,200,0), 2)
            text = label + " " + ('%.2f' % conf)
            cv2.putText(img, text, (tlx+10, tly-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200,200,0), 2)


# airplaneの数を画面上に出力
text2 =  "airplane =" + ('%.d' % count)
cv2.putText(img, text2, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200,200,0), 2)

# 結果を表示
print ("\n")
print("Number of airplane =", count)

# 表示
cv2.imshow("View", img)
cv2.waitKey(0)
# 保存して閉じる
cv2.imwrite('out.jpg', img)
cv2.destroyAllWindows()
