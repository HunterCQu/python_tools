import cv2

import matplotlib.pyplot as plt
import os, sys
import xml.etree.ElementTree as ET
import copy
import random
import shutil
import os.path
import numpy as np


LABEL = ["box", "plastic", "envelope"]

box_area = 1
def read_xml_info(w, h, quadrant, xmlpath):
    if os.path.exists(xmlpath) == False:
        return [], []
    tree = ET.parse(xmlpath)
    root = tree.getroot()

    namelist = []               #返回名字
    obj_ori = root.iter('object')
    for obj in root.iter('object'):
        types = obj.find('name').text
        namelist.append(types)

    infolist = []              #返回坐标
    for box in root.iter('bndbox'):
        xmin = float(box.find('xmin').text)
        ymin = float(box.find('ymin').text)
        xmax = float(box.find('xmax').text)
        ymax = float(box.find('ymax').text)
        if h == int(ymax):
            print(xmlpath)
        area = (ymax - ymin) * (xmax - xmin)
        infolist.append([xmin,ymin,xmax,ymax,area])

    return infolist, namelist



def read_txt_info(w, h, txtpath):
    if os.path.exists(txtpath) == False:
        return [], []

    txtfile = open(txtpath)
    txtlist = txtfile.readlines()
    namelist = []               #返回名字
    infolist = []              #返回坐标

    for i in txtlist:
        oneline = i.strip().split(' ')
        if oneline[0] == '0':
            namelist.append(LABEL[0])
        elif oneline[0] == '1':
            namelist.append(LABEL[1])
        elif oneline[0] == '2':
            namelist.append(LABEL[2])

        xmin = int((float(oneline[1])*w+1) - (float(oneline[3])*w*0.5))
        ymin = int((float(oneline[2])*h+1) - (float(oneline[4])*h*0.5))
        xmax = int((float(oneline[1])*w+1) + (float(oneline[3])*w*0.5))
        ymax = int((float(oneline[2])*h+1) + (float(oneline[4])*h*0.5))
        area = (ymax - ymin) * (xmax - xmin)
        infolist.append([xmin,ymin,xmax,ymax,area])

        return infolist, namelist




def write_xml(width, hight, name, info, outxmlpath, filename):
    # if LABEL not in name:
    #     return False
    state = False
    for i in range(len(name)):
        w = info[i][2] - info[i][0]
        h = info[i][3] - info[i][1]
        print(w*h)

        if w * h > box_area and str(name[i]):            #太小的框不要
            state = True
    if state == False:
        return False

    xml_file = open((outxmlpath + '.xml'), 'w')
    print(outxmlpath + '.xml')
    xml_file.write('<annotation>\n')
    xml_file.write('    <folder>VOC2007</folder>\n')
    xml_file.write('    <filename>' + str(filename) + '.jpg' + '</filename>\n')
    xml_file.write('    <size>\n')
    xml_file.write('        <width>' + str(width) + '</width>\n')
    xml_file.write('        <height>' + str(hight) + '</height>\n')
    xml_file.write('        <depth>3</depth>\n')
    xml_file.write('    </size>\n')

    # write the region of image on xml file
    flag = False
    for i in range(len(name)):
        w = info[i][2] - info[i][0]
        h = info[i][3] - info[i][1]
        print(w*h)

        if w * h > box_area and str(name[i]):            #太小的框不要
            xml_file.write('    <object>\n')
            xml_file.write('        <name>' + str(name[i]) + '</name>\n')
            xml_file.write('        <pose>Unspecified</pose>\n')
            xml_file.write('        <truncated>0</truncated>\n')
            xml_file.write('        <difficult>0</difficult>\n')
            xml_file.write('        <bndbox>\n')
            xml_file.write('            <xmin>' + str(int(info[i][0])) + '</xmin>\n')
            xml_file.write('            <ymin>' + str(int(info[i][1])) + '</ymin>\n')
            xml_file.write('            <xmax>' + str(int(info[i][2])) + '</xmax>\n')
            xml_file.write('            <ymax>' + str(int(info[i][3])) + '</ymax>\n')
            xml_file.write('        </bndbox>\n')
            xml_file.write('    </object>\n')
            flag = True

    xml_file.write('</annotation>')
    return flag

print("-----start-------")
root_path = ".n"
picpath = os.path.join(root_path, "/data1/workspace_hunter/t8214_data/3.28/images/")   #原始图像路径
xmlpath = os.path.join(root_path, "/data1/workspace_hunter/t8214_data/3.28/labels/")   #原始xml路径
picnamelist = os.listdir(picpath)
xmlnamelist = os.listdir(xmlpath)
savepicpath = os.path.join(root_path, "/data1/workspace_hunter/t8214_data/3.28/xml/")   #生成的图像保存的路径

if not os.path.exists(savepicpath):
    os.makedirs(savepicpath)


for i in range(len(picnamelist)):
    #pic1 = cv2.imread(os.path.join(picpath, picnamelist[i]))

    print("-----reading image : {}-------".format(picpath+picnamelist[i]))
    pic1 = cv2.imread(picpath+picnamelist[i])
    if pic1 is None:
        continue
    h, w = pic1.shape[:2]
    xmlname1 = picnamelist[i].split('.jpg')[0]+'.txt'

    print("-----reading label-------")
    info, name = read_txt_info(w, h, xmlpath + xmlname1)
    
    
    print("-----saving xml-------")
    flag = write_xml(w,h,name,info,savepicpath+picnamelist[i].split('.jpg')[0], picnamelist[i].split('.jpg')[0])
    # if flag == True:
    #     cv2.imwrite(savepicpath+picnamelist[i].split('.jpg')[0]+'.jpg',pic1)




