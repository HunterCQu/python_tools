import os
import cv2
import xml.etree.ElementTree as ET
from os import listdir, getcwd

# 设置类别，这里假设有4个类，分别是'holothurian', 'echinus', 'scallop', 'starfish'
classes = ['car']


# 定义坐标转换函数
def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[2]) / 2.0 - 1
    y = (box[1] + box[3]) / 2.0 - 1
    width = box[2] - box[0]
    height = box[3] - box[1]
    x = x * dw
    width = width * dw
    y = y * dh
    height = height * dh
    return (x, y, width, height)


# 读图片文件名文件，将其成列表存入image_ids
image_ids = open('/data1/zhixin_dataset/zhixinTrainData/eufycam/img.txt').read().strip().split()
num_xml = open('/data1/zhixin_dataset/zhixinTrainData/eufycam/all1.txt').read().strip().split()
list_file = open('file.txt', 'w')

# 循环，批量操作
for n in num_xml:
    list_file.write('image/%s.jpg' % image_ids)
    in_file = open('%s' % n)
    out_file = open('%s' % n[:-3] + 'txt', 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()


    # 获取图片信息（高和宽）
    s = root.find('size')
    width = float(s.find('width').text)
    height = float(s.find('height').text)

    # 假如xml文件中有图片信息，则直接找到那一行调用数值即可，就不用读图了
    # 判断所寻找类别在xml文件中存不存在
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        # 如果存在类名，则继续找到bndbox里的内容
        xmlbox = obj.find('bndbox')
        box = (float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text), float(xmlbox.find('xmax').text),
               float(xmlbox.find('ymax').text))

        # 调用转换函数完成坐标转换
        bb = convert((width, height), box)
        # 将新坐标输出到txt文件中
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

list_file.close()

