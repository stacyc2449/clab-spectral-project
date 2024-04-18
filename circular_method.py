import math
import numpy as np

#--------------------------------------------
# # Find vector length and angle from all dates in tlist

def circular(tlist, t_range):
    result = []
    tmin, tmax, dt = t_range
    
    for p in range(tmin, tmax+1, dt):
        theta = [2 * math.pi * t / p for t in tlist]
        a = sum(math.cos(t) for t in theta) / len(tlist)
        b = sum(math.sin(t) for t in theta) / len(tlist)
        r = math.sqrt(a**2 + b**2)
        
        if a != 0:
            tau = (p / (2. * math.pi)) * math.atan(b / a)
        else:
            tau = p / 4.  # a == 0, assume ArcTan[b/a] = Pi/2
        
        if a < 0:
            tau = (p / 2) + tau
        
        tau = tau % p
        result.append((p, r, a, b, tau))
    
    return result

#--------------------------------------------
# get the central result of the circular function and also for a whole bunch of random lists
# and then calculate the relevant percentile rankings at each test period

def markovPseudoTimeSeries(numSeries, dataList, t_range, makePseudoFn):
    tmin, tmax, dt = t_range
    centralResult = circular(dataList, [ tmin, tmax, dt])
    markovResults = [circular(makePseudoFn(dataList), [ tmin, tmax, dt]) for _ in range(numSeries)]

    # !!!
    # this next line probably needs work !!!
    # !!!
    markovPercentiles = [
        [np.percentile(result[:, :, 1], [50, 95, 99, 99.9]) for result in np.transpose(markovResults, (2, 0, 1))],
        [np.percentile(result[:, :, 2], [50, 95, 99, 99.9]) for result in np.transpose(markovResults, (2, 0, 1))],
        [np.percentile(result[:, :, 3], [50, 95, 99, 99.9]) for result in np.transpose(markovResults, (2, 0, 1))],
        [np.percentile(result[:, :, 4], [50, 95, 99, 99.9]) for result in np.transpose(markovResults, (2, 0, 1))]
    ]
    countList = [np.count_nonzero(result[:, 1] < centralResult[ii, 1]) for ii in range(len(centralResult))]
    countList = np.array(countList, dtype=float)
    markovPercentiles.insert(0, centralResult)
    markovPercentiles.append([countList] * 5)
    return markovPercentiles

#--------------------------------------------
# Now make candidate pseudo time series functions

# make a pseudo time series by assuming that the intervals between the data points are distributed according to a gamma function
def makePseudoListGamma(dataList):
    intervals = np.sort(dataList)[1:] - np.sort(dataList)[:-1]
    mean = np.mean(intervals)
    variance = np.var(intervals)
    alpha = mean**2 / variance
    beta = variance / mean
    pseudoList = np.cumsum(np.random.gamma(alpha, beta, len(dataList)))
    return pseudoList

# make a pseudo time series by randomly permuting the intervals between the data points
def makePseudoListPermutation(dataList):
    intervals = np.sort(dataList)[1:] - np.sort(dataList)[:-1]
    pseudoList = np.insert(np.cumsum(np.random.permutation(intervals)), 0, 0)
    return pseudoList

# make a pseudo time series by randomly selecting intervals from the data list with replacement
def makePseudoListIntervalsWithReplacement(dataList):
    intervals = np.sort(dataList)[1:] - np.sort(dataList)[:-1]
    pseudoList = np.insert(np.cumsum(np.random.choice(intervals, len(intervals))), 0, 0)
    return pseudoList

# make a pseudo time series assuming the n points are randomly distributed in the data interval.
def makePseudoListRandom(dataList):
    maxevent = max(dataList) * (1 + 1 / len(dataList))
    pseudolist = sorted(np.random.uniform(0, maxevent, len(dataList)))
    return pseudolist