import glob
import traceback
 
import numpy as np
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import os

base_path = './'
 
 
def generate_images(class_name, generator):
    # jpgファイル取得
    dir = base_path + class_name + '/'
    if not os.path.exists(dir + "output"):
        os.mkdir(dir + "output")
    savedir = base_path + class_name + '/output/'
    images = glob.glob(dir + '/*.jpg')
    print("input files = ", len(images))
 
    for i, image in enumerate(images):
        # 画像を読み取り
        image = load_img(image)
        # numpy arrayに変換
        x = img_to_array(image)
 
        # 4次元データに変換
        x = np.expand_dims(x, axis=0)
 
        g = generator.flow(x, save_to_dir=savedir, save_prefix=class_name, save_format='jpg')
        
        # output画像をinputの何倍作成するか 1で1倍, 10で10倍
        for j in range(10):
            g.next()
 
    print("output files = ", len(glob.glob(savedir + '/*.jpg')))





 
if __name__ == '__main__':
 
    try:
        # 画像データの拡張パラメータを設定
        train_datagen = ImageDataGenerator(
            rotation_range=0., # 画像をランダムに回転する回転範囲（0-180）
            width_shift_range=0., # ランダムに水平シフトする範囲
            height_shift_range=0., # ランダムに垂直シフトする範囲
            shear_range=0.2, # シアー強度（反時計回りのシアー角度（ラジアン））
            zoom_range=0.2, # ランダムにズームする範囲
            horizontal_flip=True, # 水平方向に入力をランダムに反転
            vertical_flip=True, # 垂直方向に入力をランダムに反転
            rescale=1.0 / 255, # 与えられた値をデータに積算する
            )
 
        generate_images('airplane', train_datagen)
        #generate_images('gorilla', train_datagen)
        #generate_images('chimpanzee', train_datagen)
 
    except Exception as e:
        traceback.print_exc()
