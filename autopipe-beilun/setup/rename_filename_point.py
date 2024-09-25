"""
脚本名称: rename_filename_timestamp.py

功能概述:
该脚本用于递归地遍历指定目录及其子目录中的所有文件，如果文件名符合特定的正则模式（前10位数字，跟随一个小数点和3位数字），将第一个小数点去掉。脚本适用于以特定数字和标识符命名的文件，如 '_ir' 或 '_vis' 类型的图像文件。

使用方法:
在命令行中运行该脚本，并指定要处理的目录路径。例如：
    python3 rename_filename_timestamp.py /path/to/directory

参数:
    /path/to/directory: 包含待重命名文件的目标目录路径。

匹配规则:
- 文件名应包含前10位数字、第11位小数点、后3位数字、类型标识（'ir' 或 'vis'），以及扩展名（'png' 或 'jpg'）。

注意事项:
1. 该脚本仅重命名文件，不对文件内容做任何更改。
2. 原文件名中的第一个小数点将被去掉，时间戳部分将被重新格式化。
"""

import os
import re
import sys

def rename_files_point_in_directory(directory_path):
    """递归地遍历指定目录及其子目录中的文件，重命名符合特定模式的文件
    
    Args:
        directory_path (str): 要处理的根目录路径。
    """

    # 正则表达式匹配文件名
    pattern = re.compile(r'^(\d{10})\.(\d{3})_(ir|vis)\.(png|jpg)$')
    
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            match = pattern.match(filename)
            if match:
                # 提取匹配的组
                prefix = match.group(1)  # 前10位数字
                suffix = match.group(2)  # 后3位数字部分
                file_type = match.group(3)  # 类型标识（ir或vis）
                extension = match.group(4)  # 文件扩展名（png或jpg）

                # 重新格式化文件名，去掉小数点
                new_filename = f"{prefix}{suffix}_{file_type}.{extension}"
                
                old_file_path = os.path.join(root, filename)
                new_file_path = os.path.join(root, new_filename)

                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {filename} -> {new_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 rename_filename_timestamp.py /path/to/directory")
        sys.exit(1)

    directory_path = sys.argv[1]

    if not os.path.isdir(directory_path):
        print(f"The specified path is not a directory: {directory_path}")
        sys.exit(1)

    rename_files_point_in_directory(directory_path)
