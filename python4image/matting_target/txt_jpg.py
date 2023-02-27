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


def json2txt(__main__):
    img1 = Image.open(img[n])
    size = [img1.size[0], img1.size[1]]
    contents = []
    sum = 0
    test1 = open(label[n])
    for line in test1:
        sum += 1
        test2 = line.split(' ')
        x, y, w, h = [float(test2[1]) * size[0], float(test2[2]) * size[1],
                      float(test2[3]) * size[0], float(test2[4].replace('\n', '')) * size[1]]

        ran_ex = random.randrange(200,300)
        if w >= size[0]/2:
            nw = size[0]
            nh = size[1]
            ncx = test2[1]
            ncy = test2[2]
            ncw = test2[3]
            nch = test2[4]
        else:
            nw = np.minimum(w+ran_ex, size[0]/2)
            nh = np.minimum(h+ran_ex, size[1]/2)
            ncx = 0.5
            ncy = 0.5
            ncw = w / nw
            nch = h / nh

        contents.append('0')
        contents.append(str(ncx))
        contents.append(str(ncy))
        contents.append(str(ncw))
        contents.append(str(nch))
        contents.append("\n")
        if sum >= 2:
            with open(label_out + file_name[:-3] + 'txt', 'a', encoding='gb18030') as fw:  # [:-3] for the .jpg files
                fw.write(" ".join(contents))
            contents = []
        elif sum <= 1:
            with open(label_out + file_name[:-3] + 'txt', 'w', encoding='gb18030') as fw:  # [:-3] for the .jpg files
                fw.write(" ".join(contents))
            contents = []

        # print(" ".join(contents))

    return x, y, nw, nh


def get_files(img_path, label_path):

    images = sorted(glob.glob(os.path.join(img_path + '*.jpg')))
    labels = sorted(glob.glob(os.path.join(label_path + '*.txt')))


    return images, labels


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


def matting(path, x, y, w, h):
    img = Image.open(path)
    size = [img.size[0], img.size[1]]
    if w == size[0]:
        left = 0
        top = 0
        right = w
        bottom = h
        box = (left, top, right, bottom)
    else:
        left = float(x - w/2)
        top = float(y - h/2)
        right = float(x + w/2)
        bottom = float(y + h/2)
        box = (left, top, right, bottom)
    image1 = img.crop(box)  # 图像裁剪


    image1.save(img_out + path.split('/')[-1])  # 存储裁剪得到的图像

    # image1.show()


if __name__ == "__main__":
    img_in = '/data1/workspace_hunter/data/parceldata_3rd/1/images/'
    label_in = '/data1/workspace_hunter/data/parceldata_3rd/labels/'
    img_out = '/data1/workspace_hunter/data/parceldata_3rd/1/images_out/'
    label_out = '/data1/workspace_hunter/data/parceldata_3rd/1/labels_out/'
    img, label = get_files(img_in, label_in)
    arix = []
    new = []
    a = []
    for n in range(6500):
        file_name = img[n].split('/')[-1]
        a = json2txt(label[n])
        matting(img[n], a[0], a[1], a[2], a[3])
        print(n)
