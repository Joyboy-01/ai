import sys
import pandas as pd
import numpy as np
import networkx as nx

# Import your algorithms
from algorithms.heuristic_algorithm import heuristic_algorithm
from algorithms.evolutionary_algorithm import evolutionary_algorithm

#python Evaluator.py -n ./data/social_network.txt -i ./data/initial_seeds.txt -b ./data/balanced_seeds.txt -k 10 -o ./output/output.txt

def load_social_network(file_path):
    """Load the social network data from a file."""
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

def load_seed_set(file_path):
    """Load the seed set from a file."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    k1, k2 = map(int, lines[0].strip().split())
    seeds = [int(lines[i].strip()) for i in range(1, k1 + 1)]
    return seeds

def main():
    social_network_path = sys.argv[2]
    initial_seed_path = sys.argv[4]
    balanced_seed_path = sys.argv[6]
    budget = int(sys.argv[8])
    output_path = sys.argv[10]
    
    social_network = load_social_network(social_network_path)
    
    initial_seeds = load_seed_set(initial_seed_path)
    balanced_seeds = load_seed_set(balanced_seed_path)

    result_heuristic = heuristic_algorithm(social_network, initial_seeds, balanced_seeds, budget)
    result_evolutionary = evolutionary_algorithm(social_network, initial_seeds, balanced_seeds, budget)

    objective_value = max(result_heuristic, result_evolutionary)
    with open(output_path, 'w') as f:
        f.write(str(objective_value))

if __name__ == "__main__":
    main()
