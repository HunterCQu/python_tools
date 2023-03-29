import os

# Define the directory containing the files
dir_path = '/path/to/folder/'

# Loop through each file in the directory
for filename in os.listdir(dir_path):
    if filename.endswith('.JPG'):
        # Construct the new filename by replacing .JPG with .jpg
        new_filename = filename.replace('.JPG', '.jpg')

        # Rename the file
        os.rename(os.path.join(dir_path, filename), os.path.join(dir_path, new_filename))
