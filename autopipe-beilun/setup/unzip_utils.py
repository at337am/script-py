"""
脚本名称: unzip_utils.py

功能概述:
该脚本用于解压指定目录及其子目录下的所有 ZIP 文件，并递归解压解压过程中产生的 ZIP 文件。最终将所有解压后的内容存储在指定的临时目录中。

使用方法:
在命令行中运行该脚本，指定源目录和临时目录的路径。例如：
    python3 unzip_utils.py /path/to/source_directory /path/to/temp_directory

参数:
    /path/to/source_directory: 包含待解压 ZIP 文件的源目录路径。
    /path/to/temp_directory: 用于存放解压后内容的临时目录路径。

注意事项:
1. 脚本会递归解压所有 ZIP 文件，包括解压后产生的 ZIP 文件。
2. 解压完成后，临时目录中的 ZIP 文件将被删除，仅保留解压后的内容。
"""

import os
import glob
import subprocess
import sys

def unzip(zip_file, target_directory):
    """解压单个 ZIP 文件到目标目录。
    
    Args:
        zip_file (str): ZIP 文件的路径。
        target_directory (str): 解压后的内容存放的目标目录。
    """

    command = ['unzip', '-o', zip_file, '-d', target_directory]  # 使用 -o 选项覆盖现有文件
    try:
        subprocess.run(command, check=True)
        print(f"Unzipped: {zip_file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to unzip {zip_file}: {e}")

def unzip_allzipfiles(src_directory, temp_directory):
    """解压源目录中的所有 ZIP 文件，并递归解压临时目录中的 ZIP 文件。
    
    Args:
        src_directory (str): 包含待解压 ZIP 文件的源目录路径。
        temp_directory (str): 用于存放解压后内容的临时目录路径。
    """
    
    def process_zip_files(directory):
        """处理指定目录中的所有 ZIP 文件并解压到临时目录。
        
        Args:
            directory (str): 要处理的目录路径。
        """

        zip_files = glob.glob(os.path.join(directory, '**', '*.zip'), recursive=True)
        for zip_file in zip_files:
            unzip(zip_file, temp_directory)  # 解压 ZIP 文件到临时目录
            print(f"解压完成: {zip_file}")
    
    # 初次解压 src_directory 中的所有 .zip 文件
    process_zip_files(src_directory)

    # 递归解压临时目录中的 ZIP 文件，直到没有新的 ZIP 文件为止
    while True:
        zip_files_in_temp = glob.glob(os.path.join(temp_directory, '**', '*.zip'), recursive=True)
        if not zip_files_in_temp:
            break  # 如果没有新的 ZIP 文件，则终止递归
        for zip_file in zip_files_in_temp:
            unzip(zip_file, temp_directory)  # 解压找到的 ZIP 文件
            os.remove(zip_file)  # 解压后删除 ZIP 文件
            print(f"已删除: {zip_file}")
            
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 unzip_utils.py /path/to/source_directory /path/to/temp_directory")
        sys.exit(1)

    src_directory = sys.argv[1]  # 数据源目录
    temp_directory = sys.argv[2]  # 临时目录

    os.makedirs(temp_directory, exist_ok=True)

    unzip_allzipfiles(src_directory, temp_directory)
