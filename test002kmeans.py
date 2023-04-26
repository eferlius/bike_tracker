# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 00:01:01 2022

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
import basic.timer as basTim
# import everything from the preparation script
import AAApreliminary as config
#%% get frame

videoDirectory = config.DICT['DIR']['0_raw videos DIR']

videos = basic.utils.findFileInDirectory(videoDirectory,'')
frame = bt.imagelib.getFrameFromVideo(videos[-1], 1100, False, True)

#%% crop frame
# tl, br = bt.imagelib.getTLBR_user(frame)

# print('tl = ' + str(tl))
# print('br = ' + str(br))

# tl = [440, 401]
# br = [471, 445]

# tl = [81, 253]
# br = [182, 304]
tl = [158, 245]
br = [267, 297]

# crop frame
img = bt.imagelib.cropImageTLBR(frame, tl, br, False, True)

_ = bt.digit.extractDigitKmeans(img, k = 3, showImage = True)
