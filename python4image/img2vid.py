import os
import cv2

im_dir = "./out/"
video_output = "./2.mp4"

fps=15
img = cv2.imread(os.path.join(im_dir, '1_frame_1.jpg'))
h, w, c = img.shape
img_size = (w,h)

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
videoWriter = cv2.VideoWriter(video_output, fourcc, fps, img_size)

im_list = os.listdir(im_dir)
#im_list.sort()

for i in range(0, len(im_list)):
    im_name = os.path.join(im_dir, "frame_"+str(i+1)+".jpg")
    print(im_name)
    frame = cv2.imread(im_name, 1)
    videoWriter.write(frame)


videoWriter.release()
print('Done !')
print("img size : h, w", h, w)
