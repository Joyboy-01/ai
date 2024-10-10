import argparse
import networkx as nx
import random
#python IEMP_Heur.py -n ./data/dataset1.txt -i ./data/initial_seeds.txt -b ./data/balanced_seeds.txt -k 10
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

def monte_carlo_simulation(graph, seeds1, seeds2, simulations=1):
    total_exposure = 0
    for _ in range(simulations):
        exposed_nodes_1 = independent_cascade(graph, seeds1, "weight1")
        exposed_nodes_2 = independent_cascade(graph, seeds2, "weight2")
        total_exposure += len(graph.nodes) - len(exposed_nodes_1.symmetric_difference(exposed_nodes_2))
    return total_exposure / simulations

def greedy_best_first_search(graph, initial_seeds1, initial_seeds2, budget, simulations=5):
    S1 = set()
    S2 = set()
    best = 0
    budget_left = budget
  
    while budget_left > 0:
        best_node = None
        best_score = float('-inf')
        best_set = None
        sum1 = dict()
        sum2 = dict()
        for node in graph.nodes :
            if node not in initial_seeds1 and node not in initial_seeds2 and node not in S1 and node not in S2:
                sum1[node] = 0.0
                sum2[node] = 0.0
        current_result = monte_carlo_simulation(graph, S1, S2, simulations)
        for seed in graph.nodes:
            if seed not in S1 and seed not in S2:
                temp_S1 = S1|{seed}
                result = monte_carlo_simulation(graph, temp_S1, S2, simulations)
                sum1[seed] = result - current_result
                temp_S2 = S2|{seed}
                result = monte_carlo_simulation(graph, S1, temp_S2, simulations)
                sum1[seed] = result - current_result
        for node in graph.nodes:
            if node not in initial_seeds1 and node not in initial_seeds2 and node not in S1 and node not in S2:
                if sum1[node] > best_score:
                    best_score = sum1[node]
                    best_node = node
                    best_set = 1
                if sum2[node] > best_score:
                    best_score = sum2[node]
                    best_node = node
                    best_set = 2
        if best_node is None:
            break
        if best_set == 1:
            S1.add(best_node)
            budget_left -= 1
        else:
            S2.add(best_node)
            budget_left -= 1
    best = monte_carlo_simulation(graph, initial_seeds1 | S1, initial_seeds2 | S2, simulations)
    print(best)
    return best,S1,S2

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--network_file")
    parser.add_argument("-i", "--initial_seeds")
    parser.add_argument("-b", "--balanced_seeds")
    parser.add_argument("-k", "--budget", type=int)
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

    best,best_ranking1,best_ranking2 = greedy_best_first_search(graph, initial_seeds1,initial_seeds2, args.budget)

    combined_best_ranking = best_ranking1 | best_ranking2

    with open(args.balanced_seeds, 'w') as f:
        f.write(f"{len(best_ranking1)} {len(best_ranking2)}\n")
        f.write("\n".join(map(str, best_ranking1)) + "\n")
        f.write("\n".join(map(str, best_ranking2)) + "\n")
