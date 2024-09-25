import cv2
import os
import argparse

# 创建ArgumentParser对象
parser = argparse.ArgumentParser(description="Extract frames from a video file using OpenCV")

# 添加命令行位置参数
parser.add_argument('video', type=str, help='Path to the input video file')
parser.add_argument('--output', type=str, default='frames_output', help='Directory to save the output frames')

# 解析命令行参数
args = parser.parse_args()

# 输入视频的路径
video_path = args.video  # 从命令行获取视频路径
output_folder = args.output  # 从命令行获取输出文件夹

# 如果输出文件夹不存在，则创建该文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 打开视频文件
cap = cv2.VideoCapture(video_path)

# 检查视频是否成功打开
if not cap.isOpened():
    print("Error: Cannot open video file.")
    exit()

# 获取视频的帧率
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Frames per second: {fps}")

# 初始化帧计数器
frame_count = 0

# 循环读取视频的每一帧
while True:
    ret, frame = cap.read()

    # 如果帧读取成功
    if ret:
        # 保存帧为图像文件
        frame_filename = os.path.join(output_folder, f'frame_{frame_count:04d}.jpg')  # 格式化文件名
        cv2.imwrite(frame_filename, frame)
        print(f"Saved: {frame_filename}")
        
        # 增加帧计数器
        frame_count += 1
    else:
        # 如果没有读取到帧（视频结束），退出循环
        break

# 释放视频捕获对象
cap.release()
print("All frames extracted successfully.")
