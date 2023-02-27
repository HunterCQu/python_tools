import os
import cv2

def vid2img(vid_path, im_dir):
    vids = os.listdir(vid_path)
    for vid in vids:
        vid_name = os.path.join(vid_path, vid)
        vidcap = cv2.VideoCapture(vid_name)
        suc, image = vidcap.read()
        count = 0

        while suc:
            count += 1
            if count % 1 == 0:
                resize_image = cv2.resize(image, (1920,1080), interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(os.path.join(im_dir, vid[:-4]+'_frame_%d.jpg'%count), resize_image)
                suc, image = vidcap.read()
                print('read a new frame: ', suc, count)
            else:
                continue
        fps=15
        img = cv2.imread(os.path.join(im_dir, vid[:-4]+'_frame_%d.jpg'%count))
        h, w, c = img.shape
        img_size = (w,h)

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        videoWriter = cv2.VideoWriter(video_output, fourcc, 15, img_size)

        im_list = os.listdir(im_dir)
        #im_list.sort()

        for i in range(0, len(im_list)):
            im_name = os.path.join(im_dir, "1_frame_"+str(i+1)+".jpg")
            print(im_name)
            frame = cv2.imread(im_name, 1)
            videoWriter.write(frame)


        videoWriter.release()
        print('Done !')
        print("img size : h, w", h, w)

        


if __name__ == "__main__":
    vid_path = "/data1/workspace_hunter/face_data/huian_0822/video_4_3/"
    im_dir = "./out/"
    vid2img(vid_path, im_dir)




