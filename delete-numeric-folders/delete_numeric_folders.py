import os
import shutil
import sys

def is_numeric_folder(name):
    """检查文件夹名是否为0-100之间的纯数字"""
    return name.isdigit() and 0 <= int(name) <= 100

def delete_numeric_folders(directory):
    """删除指定目录下名为0-100的纯数字文件夹"""
    deleted_count = 0
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path) and is_numeric_folder(item):
            try:
                shutil.rmtree(item_path)
                print(f"已删除文件夹: {item_path}")
                deleted_count += 1
            except Exception as e:
                print(f"删除文件夹 {item_path} 时出错: {str(e)}")
    
    return deleted_count

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python script.py <directory_path>")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"错误: {directory} 不是一个有效的目录")
        sys.exit(1)
    
    print(f"正在处理目录: {directory}")
    deleted = delete_numeric_folders(directory)
    print(f"操作完成。共删除了 {deleted} 个文件夹。")
