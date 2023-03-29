import os
import shutil

root_path = './jinjin_230317'
folderA_path = root_path + '/images'
folderB_path = root_path + '/labels'
unique_files_path = 'unique_files'

new_folder_name = "useless_file"
# Get a list of XML files in folderA
folderA_files = [os.path.splitext(f)[0] for f in os.listdir(folderA_path) if f.endswith('.jpg') or f.endswith('.JPG')]

# Get a list of JPG files in folderB
folderB_files = [os.path.splitext(f)[0] for f in os.listdir(folderB_path) if f.endswith('.xml')]

# Find the files that are not in both folderA and folderB
unique_files = set(folderA_files) ^ set(folderB_files)

# Create the output folder if it doesn't exist
if not os.path.exists(unique_files_path):
    os.makedirs(unique_files_path)

# Move the unique files to the output folder
for f in unique_files:
    if f in folderA_files:
        try:
            shutil.move(os.path.join(folderA_path, f + '.jpg'), os.path.join(unique_files_path, f + '.jpg'))
        except:
            continue
        try:
            shutil.move(os.path.join(folderA_path, f + '.JPG'), os.path.join(unique_files_path, f + '.JPG'))
        except:
            continue

    elif f in folderB_files:
        shutil.move(os.path.join(folderB_path, f + '.xml'), os.path.join(unique_files_path, f + '.xml'))
    else:
        print(f"File {f} not found in either {folderA_path} or {folderB_path}")
