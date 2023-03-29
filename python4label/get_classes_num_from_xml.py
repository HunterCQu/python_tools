import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

# Define the directory containing the XML files
xml_dir = '/Users/anker/python_tools/test/xml'

# Initialize a dictionary to store the count of objects
object_count = {}

# Loop through each XML file in the directory
for filename in os.listdir(xml_dir):
    if filename.endswith('.xml'):
        # Parse the XML file
        tree = ET.parse(os.path.join(xml_dir, filename))
        root = tree.getroot()

        # Count the number of objects in the XML file
        for obj in root.findall('object'):
            obj_name = obj.find('name').text
            if obj_name not in object_count:
                object_count[obj_name] = 0
            object_count[obj_name] += 1

# Create a fan chart using the object count data
labels = list(object_count.keys())
counts = list(object_count.values())
total_counts = sum(counts)
percentages = [(count/total_counts)*100 for count in counts]
angles = [360*perc/100 for perc in percentages]

fig, ax = plt.subplots()
ax.set_title('Object Count')
ax.axis('equal')

wedges, _ = ax.pie(angles, startangle=90, counterclock=False, wedgeprops={'width': 0.7})
for i, wedge in enumerate(wedges):
    percentage = round(percentages[i], 2)
    label = f'{labels[i]} ({counts[i]}, {percentage}%)'
    angle = (wedge.theta2 - wedge.theta1)/2 + wedge.theta1
    x = np.cos(np.deg2rad(angle))
    y = np.sin(np.deg2rad(angle))
    ha = 'center' if abs(x) < abs(y) else ('left' if x > 0 else 'right')
    va = 'center' if abs(y) < abs(x) else ('bottom' if y > 0 else 'top')
    ax.text(x*1.2, y*1.2, label, ha=ha, va=va)

plt.show()
