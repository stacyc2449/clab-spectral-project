import spectral
import spherule_dist

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

snape_basalt = pd.read_csv('data/Organized Data - Snape et al., 2019.csv')  #apollo 11,12,14,15,17

long_change5 = pd.read_csv('data/Organized Data - Long et al., 2022.csv')   #chang'e 5
zellner_apollo = pd.read_csv('data/Organized Data - Zellner & Delano, 2015 (filtered).csv')  #apollo 14, 16, 17
norman_apollo_16 = pd.read_csv('data/Organized Data - Norman et al., 2019.csv')  #apollo 16
nguyen_apollo = pd.read_csv('data/Organized Data - Nguyen & Zellner, 2019 .csv')  #apollo 14, 16, 17
hui_apollo_16 = pd.read_csv('data/Organized Data - Hui, 2011.csv')  #apollo 16

nguyen_apollo = nguyen_apollo[nguyen_apollo.isin(['good']).any(axis=1)]

hui_apollo_16 = hui_apollo_16[(hui_apollo_16['FeO'] > 7.4) | (hui_apollo_16['K2O'] > 0.07)]

long_change5 = long_change5[~long_change5.isin(['na']).any(axis=1)]

# zellner_apollo = zellner_apollo[zellner_apollo['Absolute Model Age'] < 1500]


snape_ama = snape_basalt['Absolute Model Age'].to_list()
snape_2_stdev = snape_basalt['2 stdev'].to_list()

long_ama = long_change5['Absolute Model Age'].to_list()
long_1_stdev = long_change5['1 stdev'].to_list()

zellner_ama = zellner_apollo['Absolute Model Age'].to_list()
zellner_2_stdev = zellner_apollo['2 stdev'].to_list()

norman_ama = norman_apollo_16['Absolute Model Age'].to_list()
norman_2_stdev = norman_apollo_16['2 stdev'].to_list()

nguyen_ama = nguyen_apollo['Absolute Model Age'].to_list()
nguyen_2_stdev = nguyen_apollo['2 stdev'].to_list()

hui_ama = hui_apollo_16['Absolute Model Age'].to_list()
hui_1_stdev = hui_apollo_16['1 stdev'].to_list()

def create_t_list(ama, stdev, two_stdev=False, charred=False):
    t_list = []
    if len(ama) != len(stdev):
        print('two list lengths do not match.')
        return
    if two_stdev:
        stdev = [float(t / 2) for t in stdev]
    if charred:
        ama = [float(a) for a in ama]
        stdev = [float(s) for s in stdev]
    for i in range(len(ama)):
        temp_list = [ama[i], stdev[i]]
        t_list.append(temp_list)
    return t_list

snape_t_list = create_t_list(snape_ama, snape_2_stdev, True)
long_t_list = create_t_list(long_ama, long_1_stdev, charred=True)
zellner_t_list = create_t_list(zellner_ama, zellner_2_stdev, True)
norman_t_list = create_t_list(norman_ama, norman_2_stdev, True)
nguyen_t_list = create_t_list(nguyen_ama, nguyen_2_stdev, True)
hui_t_list = create_t_list(hui_ama, hui_1_stdev)



def run_spectral(t_list, t_list_no_stdev, min):
    period_range = [min, 500, 0.1]
    p_list = np.arange(min, 500, 0.1)
    new_t_list = []
    for t in t_list:
        age_set = spectral.random_sampling(t[0], t[1], 100)
        new_t_list.extend(age_set)
    real_r = spectral.circular(new_t_list, period_range)

    fifty = []
    ninety_five = []
    ninety_nine = []
    ninety_nine_nine = []
    for p in p_list:
        percentiles = spectral.pseudo_list_percentiles(t_list_no_stdev, spectral.make_pseudo_list_gamma, p)
        fifty.append(percentiles[0])
        ninety_five.append(percentiles[1])
        ninety_nine.append(percentiles[2])
        ninety_nine_nine.append(percentiles[3])

    plt.plot(p_list, real_r, marker=',', color='k')
    plt.plot(p_list, fifty, marker=',', color='blue')
    plt.plot(p_list, ninety_five, marker=',', color='cyan')
    plt.plot(p_list, ninety_nine, marker=',', color='orange')
    plt.plot(p_list, ninety_nine_nine, marker=',', color='red')
    plt.show()

def run_spectral_individual(t_list, period):
    # new_t_list = []
    # for t in t_list:
    #     age_set = spectral.random_sampling(t[0], t[1], 100)
    #     new_t_list.extend(age_set)
    spectral.sub_circular_plot(t_list, period)
    
    

def filter_list(data_list, threshold, max_age):
    for entry in reversed(range(len(data_list))):
        if data_list[entry][1] > threshold:
            data_list.pop(entry)
        if data_list[entry][0] > max_age:
            data_list.pop(entry)
    return data_list

def create_ama_list(filtered_list):
    ama_list = []
    for entry in filtered_list:
        ama_list.append(entry[0])
    return ama_list

def find_largest_interval(ama_list):
    ama_list.sort()
    largest_interval = 0
    for i in range(len(ama_list) - 1):
        if ama_list[i+1] - ama_list[i] > largest_interval:
            largest_interval = ama_list[i+1] - ama_list[i]
    return largest_interval

cum_t_list = long_t_list
cum_t_list.extend(zellner_t_list)
cum_t_list.extend(norman_t_list)
cum_t_list.extend(nguyen_t_list)
cum_t_list.extend(hui_t_list)


cum_ama = [float(t) for t in long_ama]
cum_ama.extend(zellner_ama)
cum_ama.extend(norman_ama)
cum_ama.extend(nguyen_ama)
cum_ama.extend(hui_ama)

# new_list = filter_list(cum_t_list, 100, 1700)
# new_ama = create_ama_list(new_list)
# largest_interval = find_largest_interval(snape_ama)
# print(largest_interval)
# #
# run_spectral(snape_t_list, snape_ama, 0.1)
run_spectral_individual(cum_ama, 310)

# spherule_dist.plot_gaussian(new_list)