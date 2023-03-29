import os
import cv2

def vid2img(vid_path, save_img_path):
    vids = os.listdir(vid_path)
    for vid in vids:
        vid_name = os.path.join(vid_path, vid)
        vidcap = cv2.VideoCapture(vid_name)
        suc, image = vidcap.read()
        count = 0

        while suc:
            count += 1
            if count % 1 == 0:
                resize_image = cv2.resize(image, (960,540), interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(os.path.join(save_img_path, vid[:-4]+'_frame_%d.jpg'%count), resize_image)
                suc, image = vidcap.read()
                print('read a new frame: ', suc, count)
            else:
                continue


if __name__ == "__main__":
    vid_path = "./"
    save_img_path = "./1110/"
    vid2img(vid_path, save_img_path)

