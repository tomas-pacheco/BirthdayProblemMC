# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 22:31:17 2021

@author: Tomas Pacheco
"""

# First I calculate the probability that at least two people share their birthday
# within a group of 30 people. The procedure is replicated 10.000 times in order 
# to calculate the probability.

import random
from collections import Counter

days = list(range(1, 366))
times = []
it_times = range(0,10000)

for i in it_times:
    sample = random.choices(days, k = 30)
    reps = list(dict(Counter(sample)).values())
    for i in reps:
        if i > 1:
            times.append(1)
            break
        else:
            continue

prob = len(times)/len(it_times)
print(f"La probabilidad es {prob}.")


# Here I replicate the procedure explained before 1000 times so I can construct
# the density of the probability with a kernel.

import statistics
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

days = list(range(1, 366))
proba = []
repsl = 100
people = 30

for i in range(0,repsl):
    times = []
    it_times = range(0,10000)
    for i in it_times:
        sample = random.choices(days, k = people)
        reps = list(dict(Counter(sample)).values())
        for i in reps:
            if i > 1:
                times.append(1)
                break
            else:
                continue
    proba.append(len(times)/len(it_times))       


density = stats.kde.gaussian_kde(proba)
m = statistics.mean(proba)
x = np.arange(min(proba)-0.01, max(proba)+0.01, .001)
plt.plot(x, density(x))
plt.vlines(m, 0, max(density(x))+5, colors = "red")
plt.text((statistics.mean(proba)+max(proba))/2, max(density(x))/2, f'mean = {m}')
plt.title(f'{repsl} reps with {people} people ')
plt.show()

# Finally, we study how does the probability evolve when we augment the 
# number of people in the 'reunion'.


cardinal = list(range(1,61))
prob_cardinal = []
days = list(range(1, 366))

for j in cardinal:
    proba = []
    repsl = 100
    people = j

    for i in range(0,repsl):
        times = []
        it_times = range(0,10000)
        for i in it_times:
            sample = random.choices(days, k = people)
            reps = list(dict(Counter(sample)).values())
            for i in reps:
                if i > 1:
                    times.append(1)
                    break
                else:
                    continue
        proba.append(len(times)/len(it_times))    
    prob_cardinal.append(statistics.mean(proba))
    print(j)

plt.plot(cardinal, prob_cardinal)
plt.xlabel("People in the 'reunion'")
plt.ylabel('Probability')
plt.title('Probability that at least two people share their birthday')


# Linear regression with the data.

import statsmodels.api as sm

x, y = np.array(cardinal), np.array(prob_cardinal)

x = sm.add_constant(x)
model = sm.OLS(y, x)
results = model.fit()
print(results.summary())
