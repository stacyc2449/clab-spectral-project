import math
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

#steps
# 1. obtain amplitude for each date
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
        r_list.append(sub_circular(t_list, p))

    #plt.plot(r_list, p_list)    
    return r_list   

def sub_circular(t_list, p):
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
    r = math.sqrt(a_**2 + b_**2)
    return r

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

# make pseudo list based on gamma function
# needs to be run through circular spectral analysis
def makePseudoListGamma(data_list):
    intervals = np.sort(data_list)[1:] - np.sort(data_list)[:-1]
    mean = np.mean(intervals)
    variance = np.var(intervals)
    k = mean**2 / variance
    theta = variance / mean
    pseudoList = np.cumsum(np.random.gamma(k, theta, len(data_list)))
    return pseudoList

def makePseudoListRandom(data_list):
    maxevent = max(data_list) * (1 + 1 / len(data_list))
    pseudolist = sorted(np.random.uniform(0, maxevent, len(data_list)))
    return pseudolist

#list put in is run 1000 times
def pseudo_list_percentiles(data_list, pseudo_fn, p): 
    r_list = []
    for i in range(1000):
        pseudo_list = pseudo_fn(data_list)
        r = sub_circular(pseudo_list, p)
        r_list.append(r)  

    return np.percentile(r_list, [50, 95, 99, 99.9])


def main(t_list, t_list_no_stdev):
    period_range = [0, 500, 0.1]
    p_list = np.arange(0, 500, 0.1)
    new_t_list = []
    for t in t_list:
        age_set = random_sampling(t_list[0], t_list[1], 1000)
        new_t_list.extend(age_set)
    real_r = circular(new_t_list, period_range)

    fifty = []
    ninety_five = []
    ninety_nine = []
    ninety_nine_nine = []
    for p in p_list:
        percentiles = pseudo_list_percentiles(t_list_no_stdev, makePseudoListGamma, p)
        fifty.append(percentiles[0])
        ninety_five.append(percentiles[1])
        ninety_nine.append(percentiles[2])
        ninety_nine_nine.append(percentiles[3])

    plt.plot(real_r, p_list, marker='-', color='k')
    plt.plot(fifty, p_list, marker='-', color='blue')
    plt.plot(ninety_five, p_list, marker='-', color='green')
    plt.plot(ninety_nine, p_list, marker='-', color='orange')
    plt.plot(ninety_nine_nine, p_list, marker='-', color='red')



