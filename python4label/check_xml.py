import os
import re
import shutil
import xml.etree.ElementTree as ET

root_path = '/Users/anker/Desktop/zaibo'

folderA_path = root_path + '/images'
folderB_path = root_path + "/labels"

# Set the name of the new folder to move the files to

new_image_folder_name = root_path + "/not_match/images"
new_xml_folder_name = root_path + "/not_match/labels"

# Create the new folder if it doesn't already exist
if not os.path.exists(new_image_folder_name):os.makedirs(new_image_folder_name)
if not os.path.exists(new_xml_folder_name):os.makedirs(new_xml_folder_name)
# Define a regular expression pattern with a capturing group
pattern = r"(\d+)_objects"

# Loop through the files in the folder
for xml_name in os.listdir(folderB_path):
    file_name = os.path.splitext(xml_name)[0]
    # Check if the file is an XML file
    if xml_name.endswith(".xml"):
        # Extract the object number from the file name
        match = re.search(pattern, xml_name)
        if match:
            object_number = int(match.group(1))

            # Load the XML file into an ElementTree object
            tree = ET.parse(folderB_path + '/' + xml_name)
            # Get the root element of the XML document
            root = tree.getroot()
            # Count the number of object elements in the document
            num_xml_objects = len(root.findall('object'))

            # Compare the object number to the index in the file name
            if object_number != num_xml_objects:
                # Move the file to the new folder
                os.rename(os.path.join(folderB_path, xml_name), os.path.join(new_xml_folder_name, xml_name))
                try:
                    shutil.move(os.path.join(folderA_path, file_name + '.jpg'), os.path.join(new_image_folder_name, file_name + '.jpg'))
                except:

                    continue
                try:
                    shutil.move(os.path.join(folderA_path, file_name + '.JPG'), os.path.join(new_image_folder_name, file_name + '.JPG'))
                except:

                    continue
