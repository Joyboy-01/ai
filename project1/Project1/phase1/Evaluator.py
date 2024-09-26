import sys
import pandas as pd
from algorithms.heuristic_algorithm import heuristic_algorithm
from algorithms.evolutionary_algorithm import evolutionary_algorithm

def main():
    # 解析命令行参数
    social_network_path = sys.argv[2]
    initial_seed_path = sys.argv[4]
    balanced_seed_path = sys.argv[6]
    budget = int(sys.argv[8])
    output_path = sys.argv[10]
    
    # 读取数据
    # TODO: 读取社交网络和种子集合
    # social_network = ...
    # initial_seeds = ...
    # balanced_seeds = ...

    # 调用算法
    result_heuristic = heuristic_algorithm(social_network, initial_seeds, balanced_seeds, budget)
    result_evolutionary = evolutionary_algorithm(social_network, initial_seeds, balanced_seeds, budget)

    # 计算最终目标值并输出
    objective_value = max(result_heuristic, result_evolutionary)
    with open(output_path, 'w') as f:
        f.write(str(objective_value))

if __name__ == "__main__":
    main()
