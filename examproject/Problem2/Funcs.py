import numpy as np
import scipy  




def sim_utility(par):
    '''Simulate utility'''
    np.random.seed(42)          # Set seed

    # Arrays to store utilities
    expected_utility = np.zeros((par.K, par.J))
    average_realised_utility = np.zeros((par.K, par.J))
    epsilon_diff = np.zeros((par.K, par.J))

    for k in range(par.K):      # Loop over simulations
        for j in range(par.J):  # Loop over careers

            # Calculate errors terms (both true and expected)
            epsilon = np.random.normal(0, par.sigma)
            mean_epsilon = 1/(k+1) * np.sum(epsilon)

            # Calculate utility
            average_realised_utility[k, j] = par.v[j] + epsilon
            expected_utility[k, j] = par.v[j] + mean_epsilon
        
            # Calculate difference between expected and realised error term
            epsilon_diff[k, j] = epsilon-mean_epsilon

    return average_realised_utility, expected_utility, epsilon_diff



