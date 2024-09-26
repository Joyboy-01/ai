import numpy as np

def heuristic_algorithm(social_network, initial_seeds, balanced_seeds, budget):
    # Initialize seed sets
    S1 = []
    S2 = []

    remaining_budget = budget

    # Define a function to compute the expected gain for adding a seed
    def compute_gain(seed, campaign):
        # Placeholder for gain calculation logic
        # Use the diffusion model to estimate the gain of adding 'seed' to campaign 'c1' or 'c2'
        # This could involve simulating the diffusion process based on the social network
        return np.random.uniform(0, 1)  # Replace with actual gain calculation

    while remaining_budget > 0:
        best_gain = -1
        best_seed = None
        best_campaign = None

        # Evaluate adding each seed for both campaigns
        for seed in social_network.nodes:
            if seed not in initial_seeds and seed not in S1 and seed not in S2:
                gain_c1 = compute_gain(seed, 'c1')
                gain_c2 = compute_gain(seed, 'c2')

                if gain_c1 > best_gain:
                    best_gain = gain_c1
                    best_seed = seed
                    best_campaign = 'c1'
                if gain_c2 > best_gain:
                    best_gain = gain_c2
                    best_seed = seed
                    best_campaign = 'c2'

        if best_seed is not None:
            if best_campaign == 'c1':
                S1.append(best_seed)
            else:
                S2.append(best_seed)
            remaining_budget -= 1  # Assuming each seed costs 1 unit

    return S1, S2

def compute_gain(seed, campaign):
    # Placeholder for the actual implementation of the gain calculation
    # This should evaluate how much additional exposure the campaign gains from this seed
    return np.random.uniform(0, 1)  # Replace with your actual gain calculation logic
