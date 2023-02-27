from skimage import io, transform, color
import numpy as np
import cv2
import os


def convert_gray(i):  # 图片处理与格式化的函数
    gray = cv2.cvtColor(i, cv2.COLOR_GRAY2RGB)  # 将彩色图片转换为灰度图片
    return gray


datapath = './images/'
filelist = os.listdir(datapath)


for file in filelist:
    img = cv2.imread(datapath + file)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    new_name = file.split('/')
    path = './out/' + new_name[-1]
    cv2.imwrite(path, gray)
