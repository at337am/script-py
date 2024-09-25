import sys
import shutil

def copy_file_content(source_file, start_num, end_num):
    # 读取源文件内容
    try:
        with open(source_file, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"源文件 {source_file} 未找到.")
        return
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return

    # 生成指定范围内的文件
    for i in range(start_num, end_num + 1):
        target_file = f"{i}.txt"
        try:
            with open(target_file, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"已创建文件: {target_file}")
        except Exception as e:
            print(f"创建文件 {target_file} 时发生错误: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法: python script.py <源文件> <开始数字> <结束数字>")
        sys.exit(1)

    source_file = sys.argv[1]
    try:
        start_num = int(sys.argv[2])
        end_num = int(sys.argv[3])
    except ValueError:
        print("开始数字和结束数字必须是整数.")
        sys.exit(1)

    if start_num > end_num:
        print("开始数字必须小于或等于结束数字.")
        sys.exit(1)

    copy_file_content(source_file, start_num, end_num)
