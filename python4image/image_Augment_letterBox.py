import cv2
import numpy as np
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
    
txt_path=r'/data1/workspace_hunter/data/test/package_shadow/labels/'
img_path=r'/data1/workspace_hunter/data/test/package_shadow/img/'

jpg_list = [fn for fn in os.listdir(img_path) if fn.endswith('.jpg')]
countImage=0


import cv2
import numpy as np
import xml.etree.ElementTree as ET


class_dict = {'aircraft': 1}

def letterbox2(img, new_shape=(768, 768), color=(128, 128, 128),
              auto=False, scaleFill=False, scaleup=True, interp=cv2.INTER_AREA):
    shape = img.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = max(new_shape) / max(shape)
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, 32), np.mod(dh, 32)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = new_shape
        ratio = new_shape[0] / shape[1], new_shape[1] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=interp)  # INTER_AREA is better, INTER_LINEAR is faster
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    print(top, bottom,left, right)
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)


def letterbox(img, new_shape=(600,800), color=(128, 128, 128), auto=False, scaleFill=False, scaleup=True):
    # Resize image to a 32-pixel-multiple rectangle https://github.com/ultralytics/yolov3/issues/232
    shape = img.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, 64), np.mod(dh, 64)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)
    
def getbox(xmin,ymin,xmax,ymax,w,h):

    x_center = (xmin + xmax) / (2 * w)
    y_center = (ymin + ymax) / (2 * h)
    width = (xmax - xmin) / w
    height = (ymax - ymin) / h
    
    return [x_center,y_center,width,height]


def letterbox_label(x,w,h,ratio,pad):
    # Normalized xywh to pixel xyxy format
    labels = x.copy()
    labels[:, 1] = ratio[0] * w * (x[:, 1] - x[:, 3] / 2) + pad[0]  # pad width
    labels[:, 2] = ratio[1] * h * (x[:, 2] - x[:, 4] / 2) + pad[1]  # pad height
    labels[:, 3] = ratio[0] * w * (x[:, 1] + x[:, 3] / 2) + pad[0]
    labels[:, 4] = ratio[1] * h * (x[:, 2] + x[:, 4] / 2) + pad[1]
    return labels
    
    
for jpg_file in jpg_list:
    countImage+=1
    print("//////////Processing "+ str(countImage)+"th image//////////")
    AnotPath=txt_path+jpg_file[:-3]+'txt'
    imagePath=img_path+jpg_file[:-3]+'jpg'
    img0 = cv2.imread(imagePath)
    width=img0.shape[1]
    height=img0.shape[0]
    img_letterbox = letterbox(img0)
    
    img = img_letterbox[0]
    ratio = img_letterbox[1]
    pad = img_letterbox[2]
    newLabel=[]
    
    
    
    with open(AnotPath, 'rb') as f:
        x = np.array([x.split() for x in f.read().splitlines()], dtype=np.float32)
        newLabel=letterbox_label(x,width,height,ratio,pad)
    #print(newLabel)
    for bbox in newLabel:
    
        box=getbox(bbox[1],bbox[2],bbox[3],bbox[4],800, 600)
        txtfile=open(r'/data1/workspace_hunter/data/test/package_shadow/image_letter/labels/lbox_'+str(jpg_file[:-3])+"txt","a+")
        txtfile.write("%d %.6f %.6f %.6f %.6f\n" %(0,box[0],box[1],box[2],box[3]))
        txtfile.close()
    
    # cv2.imshow("1",img)
    # cv2.waitKey(0)
    
    img_augmentedName=r'/data1/workspace_hunter/data/test/package_shadow/image_letter/images/lbox_'+str(jpg_file[:-3])+'jpg'
    cv2.imwrite(img_augmentedName, img)
