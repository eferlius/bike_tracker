# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 16:33:52 2022

@author: eferlius
"""

import cv2
import os
import time
import datetime
import bikeTrackLib as bt
import basic
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import basic.timer as basTim
import pandas as pd
# import everything from the preparation script
import AAApreliminary as config
import bikeTrackLib.screenMorphology as btsm

#%% flags
SAVE_VIDEO = False
PLAY_SOUND = False
WRITE_CSV = True
#%% get frame
csvDirectory = config.DICT['DIR']['csv DIR']
csvName = basic.utils.findFileInDirectory(csvDirectory,'')[0]

df = pd.read_csv(csvName, names = ['time', 'power'])
df.plot(grid = True, x = 'time')

plt.figure()
plt.plot(df['time'], df['power'], '.')
plt.grid(True)

plt.figure()
plt.plot(df['power'], '.')
plt.grid(True)
