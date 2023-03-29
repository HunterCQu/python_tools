import os
from PIL import Image

def rename_jpg_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # width, height = im.size
            if file.endswith('.JPG'):
                file_name = os.path.basename(file)
                old_path = os.path.join(root, file)
                path_name = os.path.dirname(old_path)
                new_path = path_name.replace('/', '_')
                new_name = str(new_path) + "_" + str(file_name) # replace with your desired new name
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)




# To use this function, simply call it with the path to the folder you want to search for .jpg files:

if __name__ == '__main__':

    folder_path = '/Users/anker/python_tools/3.28'
    rename_jpg_files(folder_path)