import os


path = './images/'
path_out = './labels/'
files = os.listdir(path)

for file in files:
    new_name = file.split('/')
    new_name = str(new_name).split('.')
    txt = open(path_out + new_name[-2] + '.txt', "w")
    txt.write("")
