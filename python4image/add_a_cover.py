from PIL import Image, ImageDraw
import numpy as np
import os

# 指定要处理的目录和查找的关键字
directory = "../111"
search_keyword1 = "1.2m_2.5m"
search_keyword2 = "1.5m_2.5m"

# 循环遍历目录中的所有文件
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".JPG"):
        if search_keyword2 in filename:
            # 打开图像文件
            image_path = os.path.join(directory, filename)
            image = Image.open(image_path)
            pixels = image.load()

            # 获取图像大小
            width, height = image.size

            # 创建黑色色块
            h = height // 3
            w = width // 3

            # 从覆盖区域外的区域选择一个随机颜色
            reference_pos = (width - w - 20, height - h - 23)
            reference_color = pixels[reference_pos[0], reference_pos[1]]
            block = Image.new('RGB', (w, h))

            # 将黑色色块添加到右下角
            position = (width - w, height - h)
            image.paste(block, position)

            # 保存修改后的图像
            image.save(image_path)
