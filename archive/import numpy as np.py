import numpy as np
import matplotlib.pyplot as plt

# Sample set of years (you can replace this with your own data)
years = np.array([2001, 2005, 2010, 2015, 2020, 2023])

# Standard deviation for uncertainty in years (you can adjust this value)
std_dev = 1.0  # This represents the uncertainty in years

# Function to perform Monte Carlo simulation with uncertainty
def monte_carlo_simulation(years, std_dev, n_simulations=1000):
    simulated_intervals = []
    for _ in range(n_simulations):
        # Introduce uncertainty by adding normally distributed noise
        uncertain_years = years + np.random.normal(0, std_dev, size=len(years))
        shuffled_years = np.random.permutation(uncertain_years)
        shuffled_intervals = np.diff(np.sort(shuffled_years))
        simulated_intervals.extend(shuffled_intervals)
        pseudoList = np.insert(np.cumsum(np.random.permutation(simulated_intervals)), 0, 0)
    
    return pseudoList

# Run Monte Carlo simulation
n_simulations = 10000
simulated_intervals = monte_carlo_simulation(years, std_dev, n_simulations)

# Calculate the original intervals for comparison (with uncertainty)
uncertain_years = years + np.random.normal(0, std_dev, size=len(years))
intervals = np.diff(np.sort(uncertain_years))

# Plot the original intervals vs. simulated intervals
plt.figure(figsize=(14, 7))

plt.hist(simulated_intervals, bins=30, alpha=0.5, label="Simulated Intervals with Uncertainty")
plt.axvline(np.mean(intervals), color='r', linestyle='dashed', linewidth=2, label="Mean of Original Intervals with Uncertainty")
plt.axvline(np.median(intervals), color='g', linestyle='dashed', linewidth=2, label="Median of Original Intervals with Uncertainty")

plt.title(f"Monte Carlo Simulation of Intervals with Uncertainty ({n_simulations} Simulations)")
plt.xlabel("Interval (Years)")
plt.ylabel("Frequency")
plt.legend()

plt.show()