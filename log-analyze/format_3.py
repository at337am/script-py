import re
import os

# 要读取的父目录路径
parent_directory = './log_tidy'  # 根据实际路径修改

# 获取所有子文件夹名称
subdirectories = [d for d in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, d))]

output_path = './format_output'
os.makedirs(output_path, exist_ok=True)

# 循环处理每个子文件夹
for date in subdirectories:
    # 日志文件路径
    log_file_path = os.path.join(parent_directory, date, 'neg', 'log.txt')

    # 最终输出文件路径
    final_output_file_path = os.path.join(output_path, f"{date}_neg.txt")

    # 检查日志文件是否存在
    if not os.path.exists(log_file_path):
        print(f"日志文件 {log_file_path} 不存在，跳过。")
        continue

    # 读取日志文件
    with open(log_file_path, 'r', encoding='utf-8') as log_file:
        log_lines = log_file.readlines()

    # 创建一个列表存储提取的编号
    extracted_numbers = []

    # 解析每一行日志
    for line in log_lines:
        # 使用正则表达式提取编号
        match = re.search(r'_(\d+)\.png\.npy', line)
        if match:
            number = match.group(1)  # 获取编号部分
            extracted_numbers.append(int(number))  # 转换为整数

    # 根据差距分组
    grouped_numbers = []
    current_group = []

    for number in sorted(extracted_numbers):
        if not current_group:
            current_group.append(number)
        else:
            # 检查当前编号与组中最后一个编号的差距
            if number - current_group[-1] <= 20:
                current_group.append(number)
            else:
                # 结束当前组并开始新组
                if len(current_group) > 1:
                    grouped_numbers.append(f"{current_group[0]:04d} - {current_group[-1]:04d},")  # 添加逗号
                else:
                    grouped_numbers.append(f"{current_group[0]:04d},")  # 添加逗号
                current_group = [number]

    # 添加最后一组
    if current_group:
        if len(current_group) > 1:
            grouped_numbers.append(f"{current_group[0]:04d} - {current_group[-1]:04d},")  # 添加逗号
        else:
            grouped_numbers.append(f"{current_group[0]:04d},")  # 添加逗号

    # 将分组结果写入新的文件，添加换行符
    with open(final_output_file_path, 'w', encoding='utf-8') as final_output_file:
        for grouped in grouped_numbers:
            final_output_file.write(grouped + '\n')  # 每个分组后加换行符

    print(f"分组结果已保存到 {final_output_file_path} 文件中。")
