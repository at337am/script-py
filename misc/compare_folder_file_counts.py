import os

def count_files_in_directory(directory):
    """计算指定目录下的文件数量（不包括子目录）"""
    return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])

def compare_ir_irstd_folders(directory):
    # 用于跟踪是否有文件数量不一致的情况
    all_match = True

    # 遍历指定目录及其所有子目录
    for root, dirs, files in os.walk(directory):
        for folder_name in dirs:
            if folder_name.startswith('ir_'):
                ir_folder_path = os.path.join(root, folder_name)
                # 构造对应的irstd_文件夹名
                irstd_folder_name = 'irstd_' + folder_name[3:]
                irstd_folder_path = os.path.join(root, irstd_folder_name)

                # 检查对应的irstd_文件夹是否存在
                if irstd_folder_name in dirs:
                    # 计算每个文件夹中的文件数量
                    ir_file_count = count_files_in_directory(ir_folder_path)
                    irstd_file_count = count_files_in_directory(irstd_folder_path)

                    # 比较文件数量
                    if ir_file_count != irstd_file_count:
                        print(f"文件数量不相同的文件夹: {ir_folder_path} 和 {irstd_folder_path}")
                        print(f"{ir_folder_path} 中有 {ir_file_count} 个文件")
                        print(f"{irstd_folder_path} 中有 {irstd_file_count} 个文件")
                        print("-" * 40)
                        all_match = False
                else:
                    print(f"没有找到对应的 {irstd_folder_path} 文件夹")
                    all_match = False

    # 如果所有文件夹的文件数量都相同，输出提示信息
    if all_match:
        print("所有匹配的文件夹中的文件数量都相同")

# 使用你的目录路径替换'your_directory_path'
compare_ir_irstd_folders('./tlq_01')