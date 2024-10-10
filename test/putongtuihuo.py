import argparse
import networkx as nx
import random
import numpy as np
import math

# Monte Carlo simulation to estimate influence spread
def simulate_influence(graph, seeds, iterations=1000):
    total_spread = 0
    for _ in range(iterations):
        activated = set(seeds)
        new_activated = set(seeds)

        while new_activated:
            current_activated = set()
            for node in new_activated:
                for neighbor in graph.successors(node):
                    if neighbor not in activated:
                        edge_data = graph.get_edge_data(node, neighbor)
                        prob = edge_data['weight1']
                        if random.random() <= prob:
                            current_activated.add(neighbor)
            new_activated = current_activated
            activated.update(new_activated)

        total_spread += len(activated)

    # Return average spread across simulations
    return total_spread / iterations

# Simulated annealing algorithm to optimize seed selection
def simulated_annealing(graph, initial_seeds, balanced_seeds, budget, initial_temp=1000, cooling_rate=0.99, iterations=1000):
    # Start with a random selection of seeds from the combined initial and balanced seeds
    combined_seeds = list(initial_seeds.union(balanced_seeds))
    
    # Ensure the number of selected seeds is within the budget
    if len(combined_seeds) > budget:
        current_solution = set(random.sample(combined_seeds, budget))
    else:
        current_solution = set(combined_seeds)
    
    # Calculate the initial influence spread
    current_spread = simulate_influence(graph, current_solution)
    
    best_solution = current_solution
    best_spread = current_spread
    temperature = initial_temp

    for iteration in range(iterations):
        # Generate a neighbor solution by randomly replacing one seed node
        neighbor_solution = current_solution.copy()
        if len(combined_seeds) > budget:
            # Randomly replace one node in the current solution with another from combined_seeds
            node_to_remove = random.choice(list(neighbor_solution))
            node_to_add = random.choice([node for node in combined_seeds if node not in neighbor_solution])
            neighbor_solution.remove(node_to_remove)
            neighbor_solution.add(node_to_add)

        # Calculate the influence spread of the neighbor solution
        neighbor_spread = simulate_influence(graph, neighbor_solution)
        
        # Determine if we accept the neighbor solution
        if neighbor_spread > current_spread:
            current_solution = neighbor_solution
            current_spread = neighbor_spread
        else:
            # Accept worse solution with a probability that decreases as temperature decreases
            delta = neighbor_spread - current_spread
            acceptance_prob = math.exp(delta / temperature)
            if random.random() < acceptance_prob:
                current_solution = neighbor_solution
                current_spread = neighbor_spread

        # Update best solution if the current one is better
        if current_spread > best_spread:
            best_solution = current_solution
            best_spread = current_spread

        # Cool down the temperature
        temperature *= cooling_rate

    return best_solution, best_spread


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--network_file")
    parser.add_argument("-i", "--initial_seeds")
    parser.add_argument("-b", "--balanced_seeds")
    parser.add_argument("-k", "--budget", type=int)
    parser.add_argument("-o", "--output")
    args = parser.parse_args()

    # Load the graph from file
    graph = nx.DiGraph()
    with open(args.network_file, 'r') as f:
        n, m = map(int, f.readline().split())
        for _ in range(m):
            u, v, p1, p2 = f.readline().split()
            u, v = int(u), int(v)
            p1, p2 = float(p1), float(p2)
            graph.add_edge(u, v, weight1=p1, weight2=p2)
            graph.add_edge(v, u, weight1=p2, weight2=p1)

    # Load initial seeds
    with open(args.initial_seeds, 'r') as f:
        k1, k2 = map(int, f.readline().split())
        initial_seeds = set(int(f.readline().strip()) for _ in range(k1 + k2))

    # Load balanced seeds
    with open(args.balanced_seeds, 'r') as f:
        k1, k2 = map(int, f.readline().split())
        balanced_seeds = set(int(f.readline().strip()) for _ in range(k1 + k2))

    # Run simulated annealing to optimize seed selection
    best_seeds, best_spread = simulated_annealing(graph, initial_seeds, balanced_seeds, args.budget)

    # Write the result to the output file
    with open(args.output, 'w') as f:
        f.write(f"Best Spread: {best_spread:.2f}\n")
        f.write(f"Selected Seeds: {', '.join(map(str, best_seeds))}\n")
