import argparse
import networkx as nx
import random
import numpy as np

# Simulated Annealing for Information Exposure Maximization with SAEDV and Heuristics
def simulated_annealing(graph, initial_seeds, budget, temperature=1000, cooling_rate=0.95, max_iterations=100):
    current_solution = list(initial_seeds)
    best_solution = list(current_solution)
    best_objective_value = evaluate_objective_saedv(graph, current_solution)

    for iteration in range(max_iterations):
        temperature *= cooling_rate
        if temperature <= 1e-3:
            break

        new_solution = neighbor_solution_heuristic(graph, current_solution, budget)
        new_objective_value = evaluate_objective_saedv(graph, new_solution)

        if new_objective_value > best_objective_value:
            best_solution = list(new_solution)
            best_objective_value = new_objective_value
        else:
            acceptance_probability = np.exp((new_objective_value - best_objective_value) / temperature)
            if random.random() < acceptance_probability:
                current_solution = list(new_solution)

    return best_solution

# Generate a neighbor solution using heuristic-based selection
def neighbor_solution_heuristic(graph, current_solution, budget):
    new_solution = list(current_solution)
    if len(new_solution) < budget:
        # Select a new node based on degree heuristic
        potential_nodes = [node for node in graph.nodes if node not in new_solution]
        new_node = max(potential_nodes, key=lambda x: graph.degree(x))
        new_solution.append(new_node)
    else:
        # Replace a node in the current solution with a high-degree node
        remove_idx = random.randint(0, len(new_solution) - 1)
        potential_nodes = [node for node in graph.nodes if node not in new_solution]
        new_node = max(potential_nodes, key=lambda x: graph.degree(x))
        new_solution[remove_idx] = new_node
    return new_solution

# Evaluate the objective value using Expected Diffusion Value (SAEDV)
def evaluate_objective_saedv(graph, seed_set):
    exposed_nodes = set(seed_set)
    for seed in seed_set:
        neighbors = set(graph.neighbors(seed))
        for neighbor in neighbors:
            if neighbor not in exposed_nodes:
                edge_weight = graph[seed][neighbor].get('weight', 1.0)
                if random.random() < edge_weight:
                    exposed_nodes.add(neighbor)
    return len(graph.nodes) - len(exposed_nodes)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--network_file", required=True, help="Absolute path of the social network file")
    parser.add_argument("-i", "--initial_seed_set", required=True, help="Absolute path of the initial seed set file")
    parser.add_argument("-b", "--budget", type=int, required=True, help="Budget for seed set size")
    parser.add_argument("-o", "--output", required=True, help="Output path for objective value")
    args = parser.parse_args()

    # Read the graph
    graph = nx.DiGraph()
    with open(args.network_file, 'r') as f:
        n, m = map(int, f.readline().split())
        for _ in range(m):
            u, v, p1, p2 = f.readline().split()
            graph.add_edge(int(u), int(v), weight=float(p1))

    # Read initial seed set
    with open(args.initial_seed_set, 'r') as f:
        k1, k2 = map(int, f.readline().split())
        initial_seeds = set(int(f.readline().strip()) for _ in range(k1 + k2))

    # Apply simulated annealing to find the best seed set
    best_seed_set = simulated_annealing(graph, initial_seeds, args.budget)

    # Write the result
    with open(args.output, 'w') as f:
        f.write(f"{evaluate_objective_saedv(graph, best_seed_set):.2f}\n")