"""
脚本名称: autopipe_beilun.py

功能概述:
该脚本用于自动执行一整套数据处理流程，包括解压缩数据文件、按时间戳分组、创建新目录并复制文件，以及对文件进行重命名。脚本主要用于处理以 ZIP 压缩格式存储的数据文件，将其解压后按照时间戳进行分组和组织，最终以更便于管理和分析的方式存储处理后的文件。

使用方法:
在命令行中运行该脚本，并指定数据源路径和输出路径。例如：
    python3 autopipe_beilun.py /path/to/data /path/to/output

参数:
    /path/to/data: 包含待处理的 ZIP 文件的源目录路径。
    /path/to/output: 处理后的文件将被复制到的目标目录路径。

主要处理步骤:
1. 解压缩源目录中的所有 ZIP 文件。
2. 根据文件名中的时间戳对解压后的文件进行分组。
3. 为每个分组创建新的目标目录并复制文件。
4. 对目标目录中的文件进行重命名。

注意事项:
1. 如果目标目录路径不存在，将会被自动创建。
2. 源目录中的 ZIP 文件将被解压到临时目录 'temp_unzipped' 中，该目录在处理完成后将被删除。
"""

import os
import sys
import shutil
from unzip_utils import unzip_allzipfiles
from time_based_file_splitter import resplit_catalog_bytimemark, create_new_catalog
from rename_filename_timestamp import rename_files_in_directory
from rename_ir_jpg_to_png import rename_ir_jpg_to_png
from rename_filename_point import rename_files_point_in_directory
from rename_ir_png_to_jpg import rename_ir_png_to_jpg

def auto_etl2_pipeline(srcpath, dstpath):
    """执行整个数据处理流程，包括解压、分组、复制及文件重命名
    
    Args:
        srcpath (str): 数据源目录路径，包含待处理的 ZIP 文件。
        dstpath (str): 目标目录路径，处理后的文件将存储在此目录下。
    """

    temp_directory = os.path.join(srcpath, 'temp_unzipped')
    os.makedirs(temp_directory, exist_ok=True)

    # 第一步：解压数据到临时目录
    unzip_allzipfiles(srcpath, temp_directory)
    
    # 对解压后的数据进行格式化   
    rename_files_point_in_directory(temp_directory)
    rename_ir_png_to_jpg(temp_directory)

    # 第二步：按时间戳分组
    groups = resplit_catalog_bytimemark(temp_directory)
    
    # 第三步：创建新目录并复制文件
    create_new_catalog(groups, temp_directory, dstpath)
    
    # 第四步：在目标目录中重命名文件
    rename_ir_jpg_to_png(dstpath)  # 将目标目录中的 '_ir.jpg' 文件重命名为 '_ir.png'
    rename_files_in_directory(dstpath)  # 进一步重命名文件，使其符合新的命名规范

    # 清理：删除临时目录
    shutil.rmtree(temp_directory)
    print(f"Cleaned up temporary directory: {temp_directory}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 autopipe_beilun.py /path/to/data /path/to/output")
        sys.exit(1)
    
    srcpath = sys.argv[1]
    dstpath = sys.argv[2]
    
    auto_etl2_pipeline(srcpath, dstpath)

