import os
import sys

def split_file(input_file, lines_per_file=20):
    """
    将输入文件拆分成多个文件，每个文件包含指定数量的行，使用UTF-8编码。
    
    参数:
    input_file (str): 需要拆分的输入文件路径。
    lines_per_file (int): 每个拆分文件的最大行数，默认为20。
    """
    
    # 创建用于存放拆分结果的目录。如果目录已存在，则不会出错。
    output_dir = 'split_result'
    os.makedirs(output_dir, exist_ok=True)

    # 读取输入文件的所有行，使用UTF-8编码
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 计算输入文件的总行数
    total_lines = len(lines)
    # 计算需要拆分成多少个文件
    num_files = (total_lines + lines_per_file - 1) // lines_per_file  # 使用整数除法向上取整

    for i in range(num_files):
        # 计算当前拆分文件的起始行和结束行
        start_index = i * lines_per_file
        end_index = min(start_index + lines_per_file, total_lines)
        # 生成拆分文件的名称
        output_file = os.path.join(output_dir, f'split_link_{i+1}.txt')
        
        # 将当前文件的行写入拆分文件，使用UTF-8编码
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(lines[start_index:end_index])

        # 输出拆分文件创建成功的信息
        print(f'Created: {output_file}')

if __name__ == "__main__":
    # 检查命令行参数是否正确
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python split_links.py <input_file> [lines_per_file]")
        sys.exit(1)

    # 获取输入文件的路径
    input_filename = sys.argv[1]
    
    # 检查输入文件是否存在
    if not os.path.isfile(input_filename):
        print(f"Error: File '{input_filename}' not found.")
        sys.exit(1)

    # 获取每个拆分文件的最大行数，如果未提供则默认为20
    lines_per_file = 20
    if len(sys.argv) == 3:
        try:
            lines_per_file = int(sys.argv[2])
            if lines_per_file <= 0:
                raise ValueError("The number of lines per file must be a positive integer.")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    # 调用函数进行文件拆分
    split_file(input_filename, lines_per_file)
