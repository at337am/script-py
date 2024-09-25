"""
脚本名称: time_based_file_splitter.py

功能概述:
该脚本用于处理图像文件，按时间戳将文件分组，并将每组文件复制到新的目录中。主要功能包括：
1. 从文件名中提取时间戳。
2. 根据时间戳将文件分组，每组文件的时间戳差异不超过指定的阈值。
3. 为每个分组创建新的目录，并将文件复制到相应的目录中。

使用方法:
在命令行中运行该脚本，指定源目录和目标目录的路径。例如：
    python3 time_based_file_splitter.py /path/to/source_directory /path/to/destination_directory

参数:
    /path/to/source_directory: 包含待处理文件的源目录路径。
    /path/to/destination_directory: 处理后文件保存到的目标目录路径。

注意事项:
1. 源目录中的文件必须符合命名约定，例如包含时间戳信息。
2. 如果目标目录路径不存在，将会被自动创建。
"""

import os
import shutil
import glob
from datetime import datetime

def get_file_timemark(elem):
    """从文件路径中提取时间戳。
    
    Args:
        elem (str): 文件路径。
        
    Returns:
        int: 从文件名中提取的时间戳。
    """
    
    file_name = os.path.basename(elem)
    
    timemark_str = file_name.split('_')[0]
    
    try:
        timemark = int(timemark_str)
    except ValueError:
        raise ValueError(f"无法从文件名 '{file_name}' 中提取有效的时间戳")
    
    return timemark

def resplit_catalog_bytimemark(source_dirs, delta_t=5*1000):
    """按时间戳对文件进行分组。
    
    根据时间戳将文件分组，每组中的文件时间戳之差不超过 delta_t 毫秒。
    
    Args:
        source_dirs (str): 包含源文件的目录路径。
        delta_t (int): 时间戳差异的阈值，默认为5000毫秒。
        
    Returns:
        list: 包含按时间戳分组的文件路径的列表，每个分组是一个文件路径列表。
    """

    vis_alldir = list(glob.iglob(f'{source_dirs}/**/*_vis.jpg', recursive=True))
    ir_alldir = list(glob.iglob(f'{source_dirs}/**/*_ir.jpg', recursive=True))

    # 在排序前确保两个目录长度相等
    if len(vis_alldir) != len(ir_alldir):
        print("Warning: The number of visible and infrared images do not match.")

    vis_alldir.sort(key=get_file_timemark)
    ir_alldir.sort(key=get_file_timemark)

    compare_t = None
    newall_dirs_resplit, newone_dir = [], []

    for vis_1, ir_1 in zip(vis_alldir, ir_alldir):
        vis_1_t = get_file_timemark(vis_1)
        ir_1_t = get_file_timemark(ir_1)

        # print(vis_1_t)
        # print(ir_1_t)
        
        if vis_1_t != ir_1_t:
            print(f"Mismatch found:")
            print(f"  Visible file: {vis_1} (timestamp: {vis_1_t})")
            print(f"  Infrared file: {ir_1} (timestamp: {ir_1_t})")

            # 提示用户是否跳过该 visible 文件
            user_input = input("Do you want to skip this visible file and continue? (yes/no): ").strip().lower()
            if user_input == 'yes':
                vis_index += 1
                continue
            else:
                raise ValueError("File timestamps do not match and the user chose not to skip.")
        

        #    # 提示用户是否跳过此文件
        #    user_input = input("Do you want to skip this file pair? (yes/no): ").strip().lower()
        #    if user_input == 'yes':
        #        continue
        #    else:
        #        raise ValueError("File timestamps do not match and the user chose not to skip.")

        if compare_t is None or (vis_1_t - compare_t) > delta_t:
            if newone_dir:  # 仅在 newone_dir 不为空时添加到 newall_dirs_resplit
                newall_dirs_resplit.append(newone_dir)
            compare_t = vis_1_t
            newone_dir = [vis_1, ir_1]
        else:
            newone_dir.append(vis_1)
            newone_dir.append(ir_1)
            compare_t = vis_1_t
        
    if newone_dir:  # 末尾可能还会有未添加的 newone_dir
        newall_dirs_resplit.append(newone_dir)

    return newall_dirs_resplit

def create_new_catalog(groups, src_directory, dst_directory):
    """为每个分组创建新目录，并将文件复制到新目录中。
    
    Args:
        groups (list): 按时间戳分组的文件路径列表。
        src_directory (str): 源目录路径。
        dst_directory (str): 目标目录路径。
    """

    for index, group in enumerate(groups):
        # 获取组内第一个和最后一个文件的时间戳
        # start_time = datetime.fromtimestamp(get_file_timemark(group[0]) / 1000.0)
        # end_time = datetime.fromtimestamp(get_file_timemark(group[-1]) / 1000.0)
        
        # 格式化时间段为目录名的一部分
        # time_period = f"{start_time.strftime('%Y%m%d_%H%M%S')}_to_{end_time.strftime('%Y%m%d_%H%M%S')}"
        # new_directory = os.path.join(dst_directory, f"{index}_{time_period}")  # 新目录路径
        new_directory = os.path.join(dst_directory, f"{index}")  # 新目录路径

        os.makedirs(new_directory, exist_ok=True)
        
        for elem in group:
            # 复制文件到新目录
            file_name = os.path.basename(elem)
            shutil.copy2(elem, os.path.join(new_directory, file_name))
            print(f"Copied: {elem} to {new_directory}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python3 time_based_file_splitter.py /path/to/source_directory /path/to/destination_directory")
        sys.exit(1)

    src_directory = sys.argv[1]  # 获取源目录路径
    dst_directory = sys.argv[2]  # 获取目标目录路径

    if not os.path.isdir(src_directory):
        print(f"The specified source path is not a directory: {src_directory}")
        sys.exit(1)

    if not os.path.isdir(dst_directory):
        print(f"The specified destination path is not a directory: {dst_directory}")
        sys.exit(1)

    # 按时间戳分组文件
    groups = resplit_catalog_bytimemark(src_directory)
    
    # 创建新目录并复制文件
    create_new_catalog(groups, src_directory, dst_directory)

    print("Process completed successfully.")
