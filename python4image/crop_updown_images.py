#Crop the up-down image
import os
import cv2
import glob
import shutil

def crop(main,dual,image_path, image_list):
    if not os.path.exists(main): os.makedirs(main)
    if not os.path.exists(dual): os.makedirs(dual)
    if not os.path.exists(image_path + "/small_pic"):os.makedirs(image_path + "/small_pic")

    for il in image_list:
        image_file = os.path.join(image_path, il)
        img = cv2.imread(image_file)
        if img is None: continue
        h,w,c=img.shape
        # print(il)
        if h == 2300 and w == 1600:  # find 1600x2300 pic to crop
            main_img = img[0:1200, :]
            dual_img = img[1450:, :]
            if main_img is not None:
                try:
                    cv2.imwrite(os.path.join(main, il[:-4] + "_main_" + '.jpg'), main_img)
                    cv2.imwrite(os.path.join(dual, il[:-4] + "_dual_" + '.jpg'), dual_img)
                except cv2.error as e:
                    print("Error in file:", il)
                    # continue with your code
        # elif h > w and h != 2300:  # drop the pic which smaller than 1600x2300
        #     shutil.move(os.path.join(il), image_path + "./small_pic")  # Move the file to the destination folder
    print("====================Finished Crop================")

def rename_jpg_files(folder_path, image_list):
    for root, dirs, files in os.walk(folder_path):
        for file in image_list:
            # width, height = im.size
            if file.endswith('.JPG') or file.endswith('.jpg'):
                file_name = os.path.basename(file)
                old_path = os.path.join(root, file)
                path_name = os.path.dirname(old_path)
                new_path = path_name.replace('/', '_')
                new_name = str(new_path) + "_" + str(file_name) # replace with your desired new name
                new_path = os.path.join(root, new_name)
                try:
                    os.rename(old_path, new_path)
                except os.error as e:
                    print(f"Error: {e}")
                    pass
    print("====================Finished Rename================")


def get_images_folder_4_labelimage(image_path, image_list):
    if not os.path.exists(image_path + "/images"): os.makedirs(image_path + "/images")

    for il in image_list:
        image_file = os.path.join(image_path, il)
        img = cv2.imread(image_file)
        if img is None: continue
        h, w, c = img.shape
        if h != 2300 and il.endswith('.jpg'):
            try:
                shutil.move(os.path.join(il), image_path + "/images")
            except shutil.Error as e:
                print(f"Error: {e}")
                pass
        elif "_dual_" in os.path.basename(il):
            shutil.move(os.path.join(il), image_path + "/images")



if __name__ == "__main__":
    image_path = "/Users/anker/python_tools/3.28"
    save_main_path = image_path + "./main"
    save_dual_path = image_path + "./dual"
    JPG_list = glob.glob(os.path.join(image_path, "**/*.JPG"), recursive=True)
    jpg_list = glob.glob(os.path.join(image_path, "**/*.jpg"), recursive=True)
    image_list = JPG_list + jpg_list


    # crop(save_main_path, save_dual_path, image_path, image_list)

    # rename_jpg_files(image_path, image_list)

    get_images_folder_4_labelimage(image_path, image_list)


