import os
import re
from PIL import Image, ImageDraw, ImageFont

image_data_path = 'C:/loading/task-runtime/log-analyze/data/20240828'

parent_directory = './log_tidy'  # 根据实际路径修改

# 获取所有子文件夹名称
subdirectories = [d for d in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, d))]

for date in subdirectories:
    log_file_path = './log_tidy/{}/pos/log.txt'.format(date)  # 日志文件路径
    image_directory = '{}/ir_pos_{}'.format(image_data_path, date)  # 存放图像的目录
    text_to_add = "漏报"

    output_path = './insert_text_output'
    os.makedirs(output_path, exist_ok=True)
    output_file_path = os.path.join(output_path, f"{date}_pos.txt")

    # 检查日志文件是否存在
    if not os.path.exists(log_file_path):
        print(f"日志文件 {log_file_path} 不存在，跳过该日期：{date}")
        continue  # 跳过该日期

    # 从日志中提取PNG编号
    png_numbers = []
    with open(log_file_path, 'r', encoding='utf-8') as log_file:  # 确保以utf-8读取日志
        for line in log_file:
            match = re.search(r'_(\d+)\.png\.npy', line)
            if match:
                png_number = match.group(1)
                png_numbers.append(png_number)

    # 在图像中添加文字
    with open(output_file_path, 'w', encoding='utf-8') as output_file:  # 使用utf-8写入输出文件
        for png_number in png_numbers:
            image_path = os.path.join(image_directory, f"{png_number}.png")

            if os.path.exists(image_path):
                # 打开图像
                with Image.open(image_path) as img:
                    draw = ImageDraw.Draw(img)

                    # 获取图像尺寸
                    width, height = img.size
                    
                    # 选择字体和大小（如果需要自定义字体，可以指定字体路径）
                    font_size = 60
                    try:
                        font = ImageFont.truetype("msyh.ttc", font_size)
                    except IOError:
                        font = ImageFont.load_default()
                    
                    # 计算文本边界框
                    text_bbox = draw.textbbox((0, 0), text_to_add, font=font)
                    text_width = text_bbox[2] - text_bbox[0]  # 右边界 - 左边界
                    text_height = text_bbox[3] - text_bbox[1]  # 下边界 - 上边界

                    # 计算文本位置（居中）
                    text_x = (width - text_width) / 2
                    text_y = (height - text_height) / 2

                    # 在图像上添加文本
                    draw.text((text_x, text_y), text_to_add, fill="red", font=font)

                    # 保存修改后的图像
                    img.save(image_path)

                # 写入输出文件
                output_file.write(f"在图像 {png_number}.png 中添加了文字：'{text_to_add}'\n")
                print(f"在图像 {png_number}.png 中添加了文字：'{text_to_add}'")
            else:
                output_file.write(f"图像 {png_number}.png 不存在，跳过。\n")
                print(f"图像 {png_number}.png 不存在，跳过。")
