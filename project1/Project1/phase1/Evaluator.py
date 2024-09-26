import sys
import pandas as pd
import numpy as np
import networkx as nx
from algorithms.heuristic_algorithm import heuristic_algorithm
from algorithms.evolutionary_algorithm import evolutionary_algorithm

def load_social_network(file_path):
    """读取社交网络数据"""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    n, m = map(int, lines[0].strip().split())
    edges = []
    for line in lines[1:m + 1]:
        u, v, p1, p2 = map(float, line.strip().split())
        edges.append((int(u), int(v), p1, p2))
    
    G = nx.DiGraph()
    for u, v, p1, p2 in edges:
        G.add_edge(u, v, p1=p1, p2=p2)
    
    return G

def load_seed_sets(file_path):
    """读取种子集合"""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    k1, k2 = map(int, lines[0].strip().split())
    initial_seeds = [int(lines[i].strip()) for i in range(1, k1 + 1)]
    balanced_seeds = [int(lines[i].strip()) for i in range(k1 + 1, k1 + k2 + 1)]
    return initial_seeds, balanced_seeds

def main():
    # 解析命令行参数
    social_network_path = sys.argv[2]
    initial_seed_path = sys.argv[4]
    balanced_seed_path = sys.argv[6]
    budget = int(sys.argv[8])
    output_path = sys.argv[10]
    
    # 读取数据
    social_network = load_social_network(social_network_path)
    initial_seeds, balanced_seeds = load_seed_sets(initial_seed_path)
    
    # 调用算法
    result_heuristic = heuristic_algorithm(social_network, initial_seeds, balanced_seeds, budget)
    result_evolutionary = evolutionary_algorithm(social_network, initial_seeds, balanced_seeds, budget)

    # 计算最终目标值并输出
    objective_value = max(result_heuristic, result_evolutionary)
    with open(output_path, 'w') as f:
        f.write(str(objective_value))

if __name__ == "__main__":
    main()
