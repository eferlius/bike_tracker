# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 13:38:47 2022

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
import bikeTrackLib.screenMorphology as btsm

plt.close('all')
#%% get frame
videoDirectory = config.DICT['DIR']['0_raw videos DIR']

videos = basic.utils.findFileInDirectory(videoDirectory,'')
frame = bt.imagelib.getFrameFromVideo(videos[-1], 1713, True, True)

#%% crop frame
tl, br = bt.imagelib.getCoords_user(frame, nPoints = 3, title = 'Tacx BASIC - ')
print('tl = ' + str(tl))
print('br = ' + str(br))
#%%
# tl = [66, 339]
# br = [192, 400]

tl = [74, 346]
br = [188, 402]

debug = True
powerImg00 = bt.imagelib.cropImageTLBR(frame, tl, br, True)

powerImgKmeans = bt.digit.extractDigitKmeansLoop(powerImg00, 3, debug, 0)

dictIsolated = bt.digit.isolateDigitTLBRprojectionInside(powerImgKmeans, showImage = debug)


power = bt.digit.getValueOnDict7Segments(dictIsolated, minFill = 0.3, whRatioOne = 0.25, whRatioInvalid = 1, showImage = debug, printFilling = debug)
print(power)

power = bt.digit.getValueOnDictNN(dictIsolated)

print(power)
