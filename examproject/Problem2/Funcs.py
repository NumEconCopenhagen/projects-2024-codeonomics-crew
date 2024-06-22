import numpy as np
import scipy  




def sim_utility(par):
    '''Simulate utility'''
    np.random.seed(42)          # Set seed

    # Arrays to store utilities
    expected_utility = np.zeros((par.J))
    realised_utility = np.zeros((par.K, par.J))
    epsilon_storage = np.zeros((par.K, par.J))

    for k in range(par.K):      # Loop over simulations

        

        for j in range(par.J):  # Loop over careers

            # Calculate errors terms
            epsilon = np.random.normal(0, par.sigma)
            # Add epsilon to storage
            epsilon_storage[k, j] = epsilon

            # Calculate utility
            realised_utility[k, j] = par.v[j] + epsilon
            

    # Calculate mean of the epsilons:
    mean_epsilon = np.mean(epsilon_storage, axis=0)
    # Calculate expected utility
    for j in range(par.J):
        expected_utility[j] = par.v[j] + mean_epsilon[j]
    
    # Calculate average across realised utilities
    realised_utility_mean = np.mean(realised_utility, axis=0)

    return realised_utility, expected_utility, realised_utility_mean






