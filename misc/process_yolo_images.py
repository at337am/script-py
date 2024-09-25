import cv2
import numpy as np
import os

# 主路径，所有子目录将从这个路径中读取
BASE_DIR = './data'

def read_yolo_label(yolo_file):
    print(f"Reading YOLO file: {yolo_file}")  # 添加调试信息
    with open(yolo_file, 'r') as f:
        lines = f.readlines()
        print(f"Lines read from file: {lines}")  # 添加调试信息
        if not lines:
            raise ValueError(f"File is empty: {yolo_file}")
        if len(lines) < 1:
            raise ValueError(f"File does not contain enough lines: {yolo_file}")
        try:
            label = [float(x) for x in lines[0].strip().split()]
        except ValueError as e:
            raise ValueError(f"Error converting file contents to float: {e} in file: {yolo_file}")
    return label

def process_image(image_path, yolo_label, output_rect_dir, output_cleaned_dir):
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"Image not found or could not be read: {image_path}")
        return

    img_height, img_width = image.shape[:2]

    # YOLO坐标转换为像素坐标
    x_center, y_center, bbox_width, bbox_height = yolo_label[1:]
    x_center_pixel = int(x_center * img_width)
    y_center_pixel = int(y_center * img_height)
    bbox_width_pixel = int(bbox_width * img_width)
    bbox_height_pixel = int(bbox_height * img_height)

    x_min = int(x_center_pixel - bbox_width_pixel / 2)
    y_min = int(y_center_pixel - bbox_height_pixel / 2)
    x_max = int(x_center_pixel + bbox_width_pixel / 2)
    y_max = int(y_center_pixel + bbox_height_pixel / 2)

    # 创建图像的副本用于清除处理
    cleaned_image = image.copy()

    # 在原始图像上绘制矩形框
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

    # 提取感兴趣区域 (ROI)
    roi = cleaned_image[y_min:y_max, x_min:x_max]
    if roi.size == 0:
        print(f"Invalid ROI extracted for {image_path}")
        return

    # 将ROI转换为灰度图像
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # 二值化处理
    threshold_value = 100
    _, thresholded = cv2.threshold(gray_roi, threshold_value, 255, cv2.THRESH_BINARY)

    # 应用形态学操作进行去噪处理
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    cleaned = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)

    # 将二值化的ROI转换回BGR（3通道）格式
    cleaned_bgr = cv2.cvtColor(cleaned, cv2.COLOR_GRAY2BGR)

    # 在cleaned_image中替换清理后的ROI
    cleaned_image[y_min:y_max, x_min:x_max] = cleaned_bgr

    # 确保输出目录存在
    if not os.path.exists(output_rect_dir):
        os.makedirs(output_rect_dir)
    if not os.path.exists(output_cleaned_dir):
        os.makedirs(output_cleaned_dir)

    # 保存带有矩形框的图像
    rect_image_path = os.path.join(output_rect_dir, os.path.basename(image_path))
    cv2.imwrite(rect_image_path, image)
    print(f"Processed image with rectangle saved at: {rect_image_path}")

    # 保存清理后的图像
    cleaned_image_path = os.path.join(output_cleaned_dir, "cleaned_" + os.path.basename(image_path))
    cv2.imwrite(cleaned_image_path, cleaned_image)
    print(f"Cleaned image saved at: {cleaned_image_path}")

def main():
    output_base_dir = './output'
    yolo_base_dir = './det'

    # 遍历 BASE_DIR 中的所有子目录
    subdirs = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]

    for subdir in subdirs:
        image_dir = os.path.join(BASE_DIR, subdir)
        yolo_dir = os.path.join(yolo_base_dir, subdir + '_det')  # 添加 '_det' 后缀
        output_rect_dir = os.path.join(output_base_dir, subdir, 'rect_images')
        output_cleaned_dir = os.path.join(output_base_dir, subdir, 'cleaned_images')

        yolo_files = sorted([f for f in os.listdir(yolo_dir) if f.endswith('.txt') and f != 'classes.txt'])

        for yolo_file in yolo_files:
            yolo_file_path = os.path.join(yolo_dir, yolo_file)

            image_name = os.path.splitext(yolo_file)[0]
            image_path_png = os.path.join(image_dir, image_name + '.png')
            image_path_jpg = os.path.join(image_dir, image_name + '.jpg')

            if os.path.exists(image_path_png):
                image_path = image_path_png
            elif os.path.exists(image_path_jpg):
                image_path = image_path_jpg
            else:
                print(f"No corresponding image found for YOLO file: {yolo_file}")
                continue

            yolo_label = read_yolo_label(yolo_file_path)
            process_image(image_path, yolo_label, output_rect_dir, output_cleaned_dir)

if __name__ == '__main__':
    main()
