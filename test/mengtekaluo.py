import numpy as np
import random

# 示例的社会网络图表示（邻接表）
network = {
    0: [1, 2],
    1: [3],
    2: [3],
    3: [4],
    4: []
}

# 节点数量
V = len(network)

# 随机生成的二进制向量，表示 S1 和 S2
# 二进制向量的前半部分表示 S1，后半部分表示 S2
x = np.random.choice([True, False], size=2 * V)

# 生成 S1 和 S2
def get_seed_sets(x, V):
    S1 = [i for i in range(V) if x[i]]          # 前半部分是 S1
    S2 = [i for i in range(V) if x[i + V]]      # 后半部分是 S2
    return S1, S2

# 独立级联模型下的信息传播模拟
def simulate_spread(S, network, prob=0.5):
    activated = set(S)  # 已激活的节点集合
    newly_activated = set(S)  # 本轮激活的节点集合
    
    while newly_activated:
        new_nodes = set()
        for node in newly_activated:
            for neighbor in network[node]:
                if neighbor not in activated and random.random() < prob:
                    new_nodes.add(neighbor)
        activated.update(new_nodes)
        newly_activated = new_nodes
    
    return activated

# 蒙特卡洛模拟信息传播效果
def monte_carlo_simulation(S1, S2, network, num_simulations=100, prob=0.5):
    total_spread_S1 = 0
    total_spread_S2 = 0
    
    for _ in range(num_simulations):
        spread_S1 = simulate_spread(S1, network, prob)
        spread_S2 = simulate_spread(S2, network, prob)
        
        total_spread_S1 += len(spread_S1)
        total_spread_S2 += len(spread_S2)
    
    avg_spread_S1 = total_spread_S1 / num_simulations
    avg_spread_S2 = total_spread_S2 / num_simulations
    
    # 这里可以计算传播的平衡性指标，比如 S1 和 S2 传播结果的交集、差集等
    return avg_spread_S1, avg_spread_S2

# 主函数
if __name__ == "__main__":
    # 获取 S1 和 S2
    S1, S2 = get_seed_sets(x, V)
    
    # 输出 S1 和 S2
    print(f"Seed set S1: {S1}")
    print(f"Seed set S2: {S2}")
    
    # 执行蒙特卡洛模拟
    avg_spread_S1, avg_spread_S2 = monte_carlo_simulation(S1, S2, network, num_simulations=100, prob=0.5)
    
    # 输出模拟结果
    print(f"Average spread of S1: {avg_spread_S1}")
    print(f"Average spread of S2: {avg_spread_S2}")

