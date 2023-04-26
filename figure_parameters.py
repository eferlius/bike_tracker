# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 15:21:05 2023

@author: eferlius
"""

import matplotlib.pyplot as plt
#%% plot configurations
plt.rcParams["figure.figsize"] = plt.rcParamsDefault["figure.figsize"]
plt.rcParams["figure.figsize"] = (24,10)

# paper format
plt.rc('font', size=22) # for main title in subplots
plt.rc('axes', titlesize=22) # for each axes title in subplots
plt.rc('axes', labelsize=18)
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
plt.rcParams.update({'font.size': 18})

# # poster format
# plt.rc('font', size=26) # for main title in subplots
# plt.rc('axes', titlesize=26) # for each axes title in subplots
# plt.rc('axes', labelsize=22)
# plt.rc('xtick', labelsize=22)
# plt.rc('ytick', labelsize=22)
# plt.rcParams.update({'font.size': 22})

# presentation format
plt.rc('font', size=28) # for main title in subplots
plt.rc('axes', titlesize=28) # for each axes title in subplots
plt.rc('axes', labelsize=24)
plt.rc('xtick', labelsize=24)
plt.rc('ytick', labelsize=24)
plt.rcParams.update({'font.size': 24})


# presentation format
plt.rc('font', size=50) # for main title in subplots
plt.rc('axes', titlesize=50) # for each axes title in subplots
plt.rc('axes', labelsize=40)
plt.rc('xtick', labelsize=32)
plt.rc('ytick', labelsize=32)
plt.rcParams.update({'font.size': 50})