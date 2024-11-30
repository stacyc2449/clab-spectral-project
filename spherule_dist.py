import math
import numpy as np
import scipy
from scipy import stats
import matplotlib.pyplot as plt

def plot_gaussian(t_list):
    # x = 0
    # for i in range(len(t_list)):
    #     dist = np.random.normal(loc=t_list[i][0], scale=t_list[i][1], size=1000)
    # x = x + dist
    # plt.plot(x)

    # plt.show()
    pdf = []
    x_axis = np.arange(0, 5000, 1)
    for _ in range(len(x_axis)):
        pdf.append(0)
    for i in range(len(t_list)):
        for k in range(len(pdf)):
            pdf[k] = pdf[k] + stats.norm.pdf(x_axis, t_list[i][0], t_list[i][1])[k]

    plt.plot(x_axis, pdf)
    plt.show()