import os

def find_empty_files(directory):
    """遍历目录，查找大小为0KB的文件并打印其路径"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) == 0:
                print(f"Empty file found: {file_path}")

if __name__ == "__main__":
    directory_path = './'  # 请将此处替换为你要遍历的目录路径
    find_empty_files(directory_path)
