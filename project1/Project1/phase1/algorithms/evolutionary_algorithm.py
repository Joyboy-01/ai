import random

def evolutionary_algorithm(social_network, initial_seeds, balanced_seeds, budget):
    population_size = 10
    generations = 20
    population = [random.sample(balanced_seeds, min(budget, len(balanced_seeds))) for _ in range(population_size)]
    
    for _ in range(generations):
        scores = [evaluate_solution(social_network, initial_seeds, individual) for individual in population]
        best_individual = population[scores.index(max(scores))]
        population = evolve_population(population, best_individual, budget)

    return evaluate_solution(social_network, initial_seeds, best_individual)

def evaluate_solution(social_network, initial_seeds, solution):
    """评估解的有效性"""
    total_reach = 0
    for seed in initial_seeds + solution:
        reach = simulate_diffusion(social_network, seed)
        total_reach += len(reach)
    return total_reach

def evolve_population(population, best_individual, budget):
    """简单的种群进化策略"""
    new_population = [best_individual]
    while len(new_population) < len(population):
        parent1, parent2 = random.sample(population, 2)
        child = list(set(parent1).union(set(parent2)))
        random.shuffle(child)
        new_population.append(child[:budget])
    return new_population
