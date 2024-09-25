import numpy as np
import time

def cpu_performance_test(matrix_size=3000, iterations=20):
    """
    测试 CPU 性能的函数，基于大规模矩阵的浮点运算。
    :param matrix_size: 矩阵大小（默认为1000x1000矩阵）
    :param iterations: 迭代次数（默认为10次）
    :return: 运行的总时间
    """
    # 创建两个随机的矩阵
    A = np.random.rand(matrix_size, matrix_size)
    B = np.random.rand(matrix_size, matrix_size)
    
    # 开始计时
    start_time = time.time()
    
    # 进行多次矩阵乘法
    for i in range(iterations):
        np.dot(A, B)
    
    # 结束计时
    end_time = time.time()
    
    total_time = end_time - start_time
    print(f"CPU Performance Test completed in {total_time:.4f} seconds")
    return total_time

# 调用函数进行性能测试
cpu_performance_test()
