import os
import re

log_file_path = './log/casebycase_xvits3frames_mixmodal_align1of2_olddataset.log2'
# 读取日志文件
with open(log_file_path, 'r') as log_file:
    log_lines = log_file.readlines()

# 创建一个字典，用于存储日期和对应的日志行
date_dict = {}

# 解析每一行日志
for line in log_lines:
    # 使用正则表达式匹配日期部分
    match = re.search(r'(\d{8}_\d+)', line)
    if match:
        date_key = match.group(1)  # 获取日期部分
        if date_key not in date_dict:
            date_dict[date_key] = {'neg': [], 'pos': []}  # 创建包含neg和pos的字典
        # 根据日志内容分类
        if 'neg' in line:
            date_dict[date_key]['neg'].append(line.strip())
        elif 'pos' in line:
            date_dict[date_key]['pos'].append(line.strip())

# 创建输出目录
output_directory = './log_tidy'
os.makedirs(output_directory, exist_ok=True)

# 为每个日期创建文件夹并写入日志行
for date_key, categories in date_dict.items():
    # 创建以日期命名的文件夹
    folder_name = os.path.join(output_directory, date_key)
    os.makedirs(folder_name, exist_ok=True)
    
    # 创建neg和pos的子目录
    neg_folder = os.path.join(folder_name, 'neg')
    pos_folder = os.path.join(folder_name, 'pos')
    os.makedirs(neg_folder, exist_ok=True)
    os.makedirs(pos_folder, exist_ok=True)

    # 写入neg日志
    if categories['neg']:
        neg_file_path = os.path.join(neg_folder, 'log.txt')
        with open(neg_file_path, 'w') as neg_file:
            for line in categories['neg']:
                neg_file.write(line + '\n')

    # 写入pos日志
    if categories['pos']:
        pos_file_path = os.path.join(pos_folder, 'log.txt')
        with open(pos_file_path, 'w') as pos_file:
            for line in categories['pos']:
                pos_file.write(line + '\n')

print("日志行已根据日期和类别（neg/pos）分类并保存到相应的文件夹中。")
