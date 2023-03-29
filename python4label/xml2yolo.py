import os
import xml.etree.ElementTree as ET

# Define the mapping of classes to integer labels
class_to_label = {'box': 0, 'plastic': 1, 'envelope': 2, 'ignore': -1}

# Define the input and output directories
input_dir = '/data1/workspace_hunter/3rd_package_data/3rd_week_done/xml'
output_dir = '/data1/workspace_hunter/3rd_package_data/3rd_week_done/labels'

# Iterate over each XML file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.xml'):
        # Parse the XML file
        tree = ET.parse(os.path.join(input_dir, filename))
        root = tree.getroot()

        size = root.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)

        # Open the corresponding output txt file
        txt_filename = os.path.splitext(filename)[0] + '.txt'
        with open(os.path.join(output_dir, txt_filename), 'w') as f:
            # Iterate over each object in the XML file
            for obj in root.findall('object'):
                # Get the class label and convert it to an integer
                cls = obj.find('name').text
                if cls == 'ignore':
                    continue  # Skip objects with name 'ignore'
                if cls not in class_to_label:
                    continue
                label = class_to_label[cls]

                # Get the bounding box coordinates
                bbox = obj.find('bndbox')
                xmin = float(bbox.find('xmin').text)
                ymin = float(bbox.find('ymin').text)
                xmax = float(bbox.find('xmax').text)
                ymax = float(bbox.find('ymax').text)

                # Convert the bounding box coordinates to YOLO format
                width = int(root.find('size').find('width').text)
                height = int(root.find('size').find('height').text)
                x_center = (xmin + xmax) / 2 / width
                y_center = (ymin + ymax) / 2 / height
                bbox_width = (xmax - xmin) / width
                bbox_height = (ymax - ymin) / height

                # Write the label and bounding box coordinates to the output txt file
                f.write(f'{label} {x_center} {y_center} {bbox_width} {bbox_height}\n')
