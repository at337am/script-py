import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

def copy_folder(source_dir, dest_dir):

    # 确保目标父目录存在
    dest_parent_dir = os.path.dirname(dest_dir)
    if not os.path.exists(dest_parent_dir):
        os.makedirs(dest_parent_dir)

    # 执行复制操作
    try:
        shutil.copytree(source_dir, dest_dir)
        print(f"已复制: {source_dir} 到 {dest_dir}")
    except Exception as e:
        print(f"复制失败 {source_dir} 到 {dest_dir}: {e}")

def copy_folders_with_keyword(input_paths, output_path, keyword="pos", max_workers=4):
    """
    使用多线程递归搜索并复制包含指定关键字的文件夹，从多个输入路径到输出路径。

    :param input_paths: 要搜索的多个目录路径列表。
    :param output_path: 要复制文件夹的目标目录路径。
    :param keyword: 文件夹名称中要搜索的关键字，默认为 "pos"。
    :param max_workers: 最大线程数，默认为 4。
    """
    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 创建一个线程池执行器
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        # 遍历每个输入目录及其子目录
        for input_path in input_paths:
            for root, dirs, _ in os.walk(input_path):
                for dir_name in dirs:
                    # 检查文件夹名称是否包含指定的关键字
                    if keyword in dir_name:
                        source_dir = os.path.join(root, dir_name)
                        # 生成目标路径，保持原有的子目录结构
                        dest_dir = os.path.join(output_path, os.path.relpath(source_dir, input_path))

                        # 提交复制任务到线程池
                        futures.append(executor.submit(copy_folder, source_dir, dest_dir))

        # 等待所有任务完成
        for future in as_completed(futures):
            # 获取任务的结果（如果有异常，会在此抛出）
            future.result()

if __name__ == "__main__":
    # 从命令行参数获取输入路径
    if len(sys.argv) < 2:
        print("用法: python3 copy_folders_pos.py <输入路径1> <输入路径2> ...")
        sys.exit(1)

    # 获取所有输入路径作为列表
    input_paths = sys.argv[1:]  # 从命令行获取多个输入路径
    output_path = "./label_pos_output"  # 输出路径固定为当前目录下的 label_pos_output

    # 调用函数进行多线程复制操作
    copy_folders_with_keyword(input_paths, output_path, max_workers=4)
