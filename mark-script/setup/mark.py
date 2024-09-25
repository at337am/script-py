import os
import shutil
import sys
import re
from concurrent.futures import ThreadPoolExecutor
import time

def timing_decorator(func):
    """
    装饰器，用于统计函数的执行时间。
    
    参数:
    func (function): 需要统计执行时间的函数。
    
    返回:
    function: 包装后的函数。
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录开始时间
        result = func(*args, **kwargs)
        end_time = time.time()    # 记录结束时间
        execution_time = end_time - start_time
        print(f"脚本执行时间: {execution_time:.4f} 秒")
        return result
    return wrapper

def copy_file(src_file, dst_file):
    shutil.copy(src_file, dst_file)
    print(f"已复制 {os.path.basename(src_file)} 到 {os.path.dirname(dst_file)}")

@timing_decorator
def process_images(src_dir, date, start_frame=None, end_frame=None):
    output_base_dir = './labeled_data'
    os.makedirs(output_base_dir, exist_ok=True)
    
    sub_dirs = ['ir', 'irstd']
    norm_src_dir = os.path.normpath(src_dir).split('_')[0]

    with ThreadPoolExecutor() as executor:
        for sub_dir in sub_dirs:
            src_sub_dir = os.path.join(src_dir, sub_dir)
            if not os.path.exists(src_sub_dir):
                print(f"目录 {src_sub_dir} 不存在。")
                continue

            if start_frame is not None and end_frame is not None:
                target_sub_dir_pos = os.path.join(output_base_dir, f"{sub_dir}_pos_{date}_{norm_src_dir}")
                target_sub_dir_neg = os.path.join(output_base_dir, f"{sub_dir}_neg_{date}_{norm_src_dir}")
                os.makedirs(target_sub_dir_pos, exist_ok=True)
                os.makedirs(target_sub_dir_neg, exist_ok=True)
            else:
                target_sub_dir_neg = os.path.join(output_base_dir, f"{sub_dir}_neg_{date}_{norm_src_dir}")
                os.makedirs(target_sub_dir_neg, exist_ok=True)

            pattern = re.compile(r'^(\d{4})\.png$')
            futures = []
            for filename in os.listdir(src_sub_dir):
                match = pattern.match(filename)
                if match:
                    frame_number = int(match.group(1))
                    src_file = os.path.join(src_sub_dir, filename)
                    
                    if start_frame is not None and end_frame is not None:
                        if start_frame <= frame_number <= end_frame:
                            dst_file = os.path.join(target_sub_dir_pos, filename)
                        else:
                            dst_file = os.path.join(target_sub_dir_neg, filename)
                    else:
                        dst_file = os.path.join(target_sub_dir_neg, filename)
                    
                    futures.append(executor.submit(copy_file, src_file, dst_file))
            
            # 等待所有线程完成
            for future in futures:
                future.result()

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print("用法: python script.py <源目录> <日期> [开始帧] [结束帧]")
        print("例如: python script.py ./0816-1 20240827 6400 6800")
        print("参数说明:")
        print("  <源目录> : 要处理的图片所在的目录路径，应该包含 'ir' 和 'irstd' 子目录。")
        print("  <日期> : 日期参数，将用于输出目录命名。")
        print("  [开始帧] : 从哪个帧开始作为正样本的起始帧（可选）。")
        print("  [结束帧] : 到哪个帧结束作为正样本的结束帧（可选）。")
        sys.exit(1)

    source_directory = sys.argv[1]
    date = sys.argv[2]
    start_frame = int(sys.argv[3]) if len(sys.argv) > 3 else None
    end_frame = int(sys.argv[4]) if len(sys.argv) > 4 else None

    process_images(source_directory, date, start_frame, end_frame)
