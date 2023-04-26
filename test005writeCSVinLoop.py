# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 15:32:55 2022

@author: eferlius
"""

import basic
import basic.timer as basTim
import os
from tqdm import tqdm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

fileName = os.path.join(os.getcwd(), 'test.csv')
maxValues = 1000000
#%% with csv writing
# quite long
timer = basTim.Timer()
for i in tqdm(range(maxValues)):
    newRow = [timer.lap(printTime = False)]
    basic.utils.writeCSV(fileName, newRow)
timer.stop()
#%%
df = pd.read_csv(fileName, names = ['time'])
df.plot(grid = True)
times = df['time']

#%% with list append
# incredibly fast
timesList = []
timer = basTim.Timer()
for i in tqdm(range(maxValues)):
    timesList.append(timer.lap(printTime = False))
timer.stop()
#%%
times = timesList
#%% plots and result
means = []
# averagig
step = 50
for i in np.arange(0, maxValues, step):
    means.append(np.nanmean(times[i:i+step-1]))

plt.figure()
plt.plot(means)
