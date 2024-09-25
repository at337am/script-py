"""
脚本名称: rename_ir_jpg_to_png.py

功能概述:
该脚本用于递归地遍历指定目录及其子目录中的所有文件，将所有以 '_ir.jpg' 结尾的文件重命名为 '_ir.png'。此操作主要用于将红外图像文件的格式从 JPG 更改为 PNG，保持文件名的前缀不变。

使用方法:
在命令行中运行该脚本，并指定要处理的目录路径。例如：
    python3 rename_ir_jpg_to_png.py /path/to/directory

参数:
    /path/to/directory: 包含待重命名文件的目标目录路径。

注意事项:
1. 该脚本仅重命名文件，不对文件内容做任何更改。
"""

import os
import sys

def rename_ir_jpg_to_png(directory):
    """递归地将指定目录及其子目录中的所有 '_ir.jpg' 文件重命名为 '_ir.png'
    
    Args:
        directory (str): 要处理的根目录路径。
    """

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith("_ir.jpg"):
                input_path = os.path.join(root, filename)
                output_path = os.path.join(root, filename.replace("_ir.jpg", "_ir.png"))

                os.rename(input_path, output_path)
                print(f"Renamed: {input_path} -> {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 rename_ir_jpg_to_png.py /path/to/directory")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"The specified path is not a directory: {directory}")
        sys.exit(1)

    rename_ir_jpg_to_png(directory)
