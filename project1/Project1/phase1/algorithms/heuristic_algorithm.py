import random

def heuristic_algorithm(social_network, initial_seeds, balanced_seeds, budget):
    selected_seeds = random.sample(balanced_seeds, min(budget, len(balanced_seeds)))
    total_reach = 0

    for seed in initial_seeds + selected_seeds:
        reach = simulate_diffusion(social_network, seed)
        total_reach += len(reach)

    return total_reach

def simulate_diffusion(social_network, seed):
    """模拟信息扩散的简单实现"""
    activated = set()
    to_activate = {seed}

    while to_activate:
        current = to_activate.pop()
        if current not in activated:
            activated.add(current)
            for neighbor in social_network.successors(current):
                if neighbor not in activated:
                    if random.random() < social_network[current][neighbor]['p1']:
                        to_activate.add(neighbor)

    return activated
