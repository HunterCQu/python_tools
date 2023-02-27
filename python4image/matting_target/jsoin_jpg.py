# coding: utf-8
from PIL import Image
import os
import os.path
import numpy as np
import cv2
import json
import base64
import glob
from tqdm import tqdm
import random


def json2txt(json_file):
    contents = []
    with open(json_file, 'r', encoding='utf-8') as f:   # need to transform the .json file coding type first
        data = json.load(f)
        file_name = data['imagePath']

        shapes_dic = data['shapes'][0]
        contents.append(LABELS[shapes_dic['label']])
        points = shapes_dic['points']
        og_width = data['imageWidth']
        og_height = data['imageHeight']

        x1, y1 = points[0]
        x2, y2 = points[1]



        ran_ex = random.randrange(200, 400)
        new_outside = [np.maximum(x1-ran_ex, 0.1), np.maximum(y1-ran_ex, 0.1),
        np.minimum(x2+ran_ex, og_width), np.minimum(y2+ran_ex, og_height)]

        cut_width = abs(new_outside[2] - new_outside[0])
        cut_height = abs(new_outside[3] - new_outside[1])
        nwidth = abs(x2 - x1) / cut_width
        nheight = abs(y2 - y1) / cut_height
        x_cut = ran_ex/cut_width
        y_cut = ran_ex/cut_height

        ncx = float(nwidth / 2.0) + x_cut
        ncy = float(nheight / 2.0) + y_cut



        contents.append(str(ncx))
        contents.append(str(ncy))
        contents.append(str(nwidth))
        contents.append(str(nheight))


        # print(" ".join(contents))
    with open(label_out_dir + os.sep + file_name[:-3] + 'txt', 'w',
              encoding='gb18030') as fw:  # [:-3] for the .jpg files
        fw.write(" ".join(contents))

    return x1, x2, y1, y2, new_outside


def get_json(json_path):
    jsons_path = sorted(glob.glob(os.path.join(json_path + '*.json'), ))

    return jsons_path


def get_img(img_path):
    images_path = sorted(glob.glob(os.path.join(img_path + '*.jpg')))

    return images_path


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


def matting(path, x1, y1, x2, y2):

    img = Image.open(path)

    # if x1 < x2 and y2 > y1:  ##From Top-Left
    box1 = (x1, y1, x2, y2)  # 设置左、上、右、下的像素
    # elif x1 > x2 and y2 < y1:  ##Bottom-Right
    #     box1 = (x2, y2, x1, y1)  # 设置左、上、右、下的像素
    # elif x1 < x2 and y2 < y1:  ##From Bottom-Left
    #     box1 = (x1, y2, x2, y1)  # 设置左、上、右、下的像素
    # elif x1 > x2 and y2 > y1:  ##From Top-Right
    #     box1 = (x2, y1, x1, y2)  # 设置左、上、右、下的像素

    image1 = img.crop(box1)  # 图像裁剪


    image1.save(img_out_dir + path.split('/')[-1])  # 存储裁剪得到的图像

    # image1.show()


if __name__ == "__main__":

    LABELS = {'parcel': '0'}
    img_in_dir = '/Users/anker/Desktop/aaa/images/'
    json_path = '/Users/anker/Desktop/aaa/labels/'
    label_out_dir = '/Users/anker/Desktop/aaa/labels_out/'
    img_out_dir = '/Users/anker/Desktop/aaa/images_out/'


    files = get_json(json_path)
    imgs = get_img(img_in_dir)
    a = []
    for n in range(13):
        a = json2txt(files[n])
        x1, y1, x2, y2 = (a[4])[0], (a[4])[1], (a[4])[2], (a[4])[3]
        matting(imgs[n], x1, y1, x2, y2)
