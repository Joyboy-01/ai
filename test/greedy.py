def heuristic_value(graph, current_seeds1, current_seeds2, node, campaign):
    if campaign == 1:
        new_seeds1 = current_seeds1 | {node}
        return expected_diffusion_value(graph, new_seeds1, current_seeds2) - expected_diffusion_value(graph, current_seeds1, current_seeds2)
    else:
        new_seeds2 = current_seeds2 | {node}
        return expected_diffusion_value(graph, current_seeds1, new_seeds2) - expected_diffusion_value(graph, current_seeds1, current_seeds2)

def greedy_best_first_search(graph, initial_seeds1, initial_seeds2, balanced_seeds1, balanced_seeds2, budget):
    current_seeds1 = set(balanced_seeds1)
    current_seeds2 = set(balanced_seeds2)
    remaining_budget = budget - len(current_seeds1) - len(current_seeds2)

    while remaining_budget > 0:
        best_node = None
        best_heuristic = -np.inf
        for node in set(graph.nodes) - current_seeds1 - current_seeds2:
            heuristic_1 = heuristic_value(graph, current_seeds1, current_seeds2, node, 1)
            if heuristic_1 > best_heuristic:
                best_heuristic = heuristic_1
                best_node = (node, 1)

            heuristic_2 = heuristic_value(graph, current_seeds1, current_seeds2, node, 2)
            if heuristic_2 > best_heuristic:
                best_heuristic = heuristic_2
                best_node = (node, 2)

        if best_node is None:
            break

        if best_node[1] == 1:
            current_seeds1.add(best_node[0])
        else:
            current_seeds2.add(best_node[0])

        remaining_budget -= 1

    return expected_diffusion_value(graph, initial_seeds1 | current_seeds1, initial_seeds2 | current_seeds2)
# def greedy_best_first_search(graph, initial_seeds1, initial_seeds2, budget, simulations=5):
#     S1 = set()
#     S2 = set()
#     best = 0
#     budget_left = budget
    
#     while budget_left > 0:
#         best_node = None
#         best_score = float('-inf')
#         best_set = None
#         sum1 = dict()
#         sum2 = dict()
#         for node in graph.nodes :
#             if node not in initial_seeds1 and node not in initial_seeds2 and node not in S1 and node not in S2 :
#                 sum1[node] = 0.0
#                 sum2[node] = 0.0
#         current_result = monte_carlo_simulation(graph, S1, S2, simulations)
#         for seed in graph.nodes:
#             if seed not in S1 and seed not in S2:
#                 temp_S1 = S1|{seed}
#                 result = monte_carlo_simulation(graph, temp_S1, S2, simulations)
#                 sum1[seed] = result - current_result
#                 temp_S2 = S2|{seed}
#                 result = monte_carlo_simulation(graph, S1, temp_S2, simulations)
#                 sum1[seed] = result - current_result
#         for node in graph.nodes:
#             if node not in initial_seeds1 and node not in initial_seeds2 and node not in S1 and node not in S2 :
#                 if sum1[node] > best_score:
#                     best_score = sum1[node]
#                     best_node = node
#                     best_set = 1
#                 if sum2[node] > best_score:
#                     best_score = sum2[node]
#                     best_node = node
#                     best_set = 2
#         if best_node is None:
#             break
#         if best_set == 1:
#             S1.add(best_node)
#             budget_left -= 1
#         else:
#             S2.add(best_node)
#             budget_left -= 1
#     best = monte_carlo_simulation(graph, initial_seeds1 | S1, initial_seeds2 | S2, simulations=1)
#     print(best)
#     return best,S1,S2
