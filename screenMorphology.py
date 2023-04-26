# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 21:55:32 2022

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
# import everything from the preparation script
import AAApreliminary as config

#%% flags
SAVE_VIDEO = False
PLAY_SOUND = False
#%% get frame
videoDirectory = config.DICT['DIR']['0_raw videos DIR']

video = basic.utils.findFileInDirectory(videoDirectory,'')[-1]
frame = bt.imagelib.getFrameFromVideo(video, 40000, False, False)

videoName = os.path.split(video)[-1]
#%% crop frame
tl0i = []
tl1i = []
br0i = []
br1i = []
tl0f = []
tl1f = []
br0f = []
br1f = []

for i in tqdm(range(10)):

    # tl = [112, 154]
    # br = [301, 322]
    tl, br = bt.imagelib.getCoords_user(frame, nPoints = 3)
    img = bt.imagelib.cropImageTLBR(frame, tl, br, False)

    tl0i.append(tl[0])
    tl1i.append(tl[1])
    br0i.append(br[0])
    br1i.append(br[1])

    # img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    
    tl, br = bt.imagelib.getCoords_user(img, nPoints = 2)
    img = bt.imagelib.cropImageTLBR(img, tl, br, False)

    tl0f.append(tl[0])
    tl1f.append(tl[1])
    br0f.append(br[0])
    br1f.append(br[1])


#%%
tl0im = np.nanmean(tl0i)
tl1im = np.nanmean(tl1i)
br0im = np.nanmean(br0i)
br1im = np.nanmean(br1i)
# tl0im = tl[0]
# tl1im = tl[1]
# br0im = br[0]
# br1im = br[1]

tl0fm = np.nanmean(tl0f)
tl1fm = np.nanmean(tl1f)
br0fm = np.nanmean(br0f)
br1fm = np.nanmean(br1f)

amp0 = br0im - tl0im
amp1 = br1im - tl1im

down_tl = tl0fm/amp0
right_tl = tl1fm/amp1

down_br = br0fm/amp0
right_br = br1fm/amp1
