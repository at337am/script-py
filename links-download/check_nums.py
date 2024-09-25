import os
import sys

def need_nums(path="./links.txt"):
    with open(path) as fi:
        lines = fi.readlines()
    return lines

def check_nums(lines, directory="."):
    for line in lines:
        filename = line.split("?")[0].split("/")[-1]
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            print(line.strip())

if __name__ == "__main__":
    # 从命令行参数获取目录路径，如果没有提供则使用当前目录
    if len(sys.argv) < 2:
        print("Usage: python3 check_nums.py <directory_path>")
        sys.exit(1)
    
    directory = sys.argv[1]
    check_nums(need_nums(), directory=directory)
