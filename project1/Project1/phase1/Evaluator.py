import argparse
import networkx as nx
import random
import numpy as np
#python Evaluator.py -n ./data/dataset1.txt -i ./data/initial_seeds.txt -b ./data/balanced_seeds.txt -k 10 -o ./output.txt
def independent_cascade(graph, seeds, weight_key):
    reached = set(seeds)
    vis = [False] * n

    def dfs_visit(node):
        vis[node] = True
        for neighbor in graph[node]: 
            if not vis[neighbor]: 
                weight = graph[node][neighbor][weight_key]
                rand = random.random()
                if rand < weight:
                    reached.add(neighbor)
                    dfs_visit(neighbor) 
                else:
                    reached.add(neighbor)

    for seed in seeds:
        if not vis[seed]:
            dfs_visit(seed)

    return reached

       

def monte_carlo_simulation(graph, seeds1, seeds2, simulations=1000):
    total_exposure = 0
    for _ in range(simulations):
        exposed_nodes_1 = independent_cascade(graph, seeds1, "weight1")
        exposed_nodes_2 = independent_cascade(graph, seeds2, "weight2")
        total_exposure += len(graph.nodes) - len(exposed_nodes_1.symmetric_difference(exposed_nodes_2))
    return total_exposure / simulations

def greedy_best_first_search(graph, initial_seeds1, initial_seeds2, balanced_seeds1, balanced_seeds2, budget):
    current_seeds1 = set(balanced_seeds1)
    current_seeds2 = set(balanced_seeds2)
    remaining_budget = budget - len(current_seeds1) - len(current_seeds2)

    while remaining_budget > 0:
        best_node = None
        best_spread = -np.inf
        for node in set(graph.nodes) - current_seeds1 - current_seeds2:
            new_seeds1 = current_seeds1 | {node}
            spread = monte_carlo_simulation(graph, initial_seeds1 | new_seeds1, initial_seeds2 | current_seeds2)
            if spread > best_spread:
                best_spread = spread
                best_node = (node, 1)

            new_seeds2 = current_seeds2 | {node}
            spread = monte_carlo_simulation(graph, initial_seeds1 | current_seeds1, initial_seeds2 | new_seeds2)
            if spread > best_spread:
                best_spread = spread
                best_node = (node, 2)

        if best_node is None:
            break

        if best_node[1] == 1:
            current_seeds1.add(best_node[0])
        else:
            current_seeds2.add(best_node[0])

        remaining_budget -= 1

    return monte_carlo_simulation(graph, initial_seeds1 | current_seeds1, initial_seeds2 | current_seeds2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--network_file")
    parser.add_argument("-i", "--initial_seeds")
    parser.add_argument("-b", "--balanced_seeds")
    parser.add_argument("-k", "--budget", type=int)
    parser.add_argument("-o", "--output")
    args = parser.parse_args()

    graph = nx.DiGraph()
    with open(args.network_file, 'r') as f:
        n, m = map(int, f.readline().split())
        for _ in range(m):
            u, v, p1, p2 = f.readline().split()
            u, v = int(u), int(v)
            p1, p2 = float(p1), float(p2)
            graph.add_edge(u, v, weight1=p1, weight2=p2)

    with open(args.initial_seeds, 'r') as f:
        k1, k2 = map(int, f.readline().split())
        initial_seeds1 = set(int(f.readline().strip()) for _ in range(k1))
        initial_seeds2 = set(int(f.readline().strip()) for _ in range(k2))


    with open(args.balanced_seeds, 'r') as f:
        k1, k2 = map(int, f.readline().split())
        balanced_seeds1 = set(int(f.readline().strip()) for _ in range(k1))
        balanced_seeds2 = set(int(f.readline().strip()) for _ in range(k2))

    best_spread = greedy_best_first_search(graph, initial_seeds1, initial_seeds2, balanced_seeds1, balanced_seeds2, args.budget)

    with open(args.output, 'w') as f:
        f.write(f"{best_spread:.2f}\n")