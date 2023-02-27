import os
import random

if __name__ == '__main__':
    # 文件路径
    script_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(script_path, 'all.txt')

    # 读取文件
    total_list = []
    with open(dir_path, 'r') as f:
        for line in f:
            line = line.strip('\n')
            total_list.append(line)
    

    # 划分数据集
    random.seed(12345)
    random.shuffle(total_list)
    total_len = len(total_list)
    train_len = int(0.8 * total_len)
    train_list = total_list[:train_len]
    val_list = total_list[train_len:]

    # 写入train.txt
    save_file_path = os.path.join(script_path, './train.txt')
    file_obj = open(save_file_path, 'w')
    for file in train_list:
        file_obj.write(file)
        if file != train_list[-1]:
            file_obj.write('\n')
    file_obj.close()

    # 写入val.txt
    save_file_path = os.path.join(script_path, './val.txt')
    file_obj = open(save_file_path, 'w')
    for file in val_list:
        file_obj.write(file)
        if file != val_list[-1]:
            file_obj.write('\n')
    file_obj.close()


