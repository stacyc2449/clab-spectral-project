import math
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

#steps
# 1. obtain amplitude for each date, using bootstrapping
# 2. Use theta, iterating through values of p... which would be from 0 to 500, dt = 0.1?
# 3. In the A abd B formulas, w is the probability, or amplitude i guess
# ---- or should i combine all the probabilities to make a function of frequency first, then perform the analysis?
# 4. graph, look at where r is the most significant
# 5. Monte carlo simulations for comparison


#t_list would essentially be all the bootstrapped dates combined... right?
def circular(t_list, t_range):
    p_min, p_max, d_p = t_range
    p_list = np.arange(p_min, p_max, d_p)
    r_list = []
    
    for p in p_list:
        result_a = []
        result_b = []
        for t in t_list:
            theta = (2 * math.pi * t / p) % (2 * math.pi)
            a = math.cos(theta)
            b = math.sin(theta)
            result_a.append(a)
            result_b.append(b)
        a_ = sum(result_a) / len(t_list)
        b_ = sum(result_b) / len(t_list)
        r = math.sqrt(a**2 + b**2)
        r_list.append(r)

    plt.plot(r_list, p_list)    
        

def random_sampling(age, stdev, num):
    result = []
    A = stats.norm(age, stdev)
    for i in range(num):
        rand_samp = round(A.rvs(), 2)
        result.append(rand_samp)
    return result

# monte carlo simulations account for uncertainty
# returns list, that needs to be run through circular spectral analysis
def monte_carlo_simulation(years, std_dev, n_simulations=1000):
    simulated_intervals = []
    for _ in range(n_simulations):
        uncertain_years = years + np.random.normal(0, std_dev, size=len(years))
        shuffled_years = np.random.permutation(uncertain_years)
        shuffled_intervals = np.diff(np.sort(shuffled_years))
        simulated_intervals.extend(shuffled_intervals)
        pseudoList = np.insert(np.cumsum(np.random.permutation(simulated_intervals)), 0, 0)
    
    return pseudoList
