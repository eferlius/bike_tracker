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
frame = bt.imagelib.getFrameFromVideo(videos[-1], 3131, True, True) #113
# frame = bt.imagelib.getFrameFromVideo(videos[-1], 1075, True, True) #75
# frame = bt.imagelib.getFrameFromVideo(videos[-1], 8907, True, True) #139 with strange 9
frame = bt.imagelib.getFrameFromVideo(videos[-1], 8908, True, True) #140 with strange 0
# frame = bt.imagelib.getFrameFromVideo(videos[-1], 8910, True, True) #140
# frame = bt.imagelib.getFrameFromVideo(videos[-1], 3061, True, True) #113
# frame = bt.imagelib.getFrameFromVideo(videos[-1], 8451, True, True) #130
# frame = bt.imagelib.getFrameFromVideo(videos[-1], 76801, True, True) #247 considered as 297
# frame = bt.imagelib.getFrameFromVideo(videos[-1], 9486, True, True) #149 considered as 299
frame = bt.imagelib.getFrameFromVideo(videos[-1], 50001, True, True) #144 considered as 299
# frame = bt.imagelib.getFrameFromVideo(videos[-1], 71497, True, True) #160 seen as 60
# frame = bt.imagelib.getFrameFromVideo(videos[-1], 28752, True, True) #160 seen as 60
# frame = bt.imagelib.getFrameFromVideo(videos[-1], 348, True, True) #160 seen as 60

#%% crop frame
tlt, brt = bt.imagelib.getCoords_user(frame, nPoints = 3, title = 'Tacx BASIC - ')
print('tl = ' + str(tlt))
print('br = ' + str(brt))
# tlt = [111, 149]
# brt = [299, 320]

tlp, brp = btsm.getTLBR(tlt, brt, 'Tacx BASIC', 'power')

# tlg, brg = bt.imagelib.getCoords_user(frame, nPoints = 2, title = 'Garmin - ')
# print('tl = ' + str(tlg))
# print('br = ' + str(brg))

tl = tlt
br = brt
# tl = tlg
# br = brg
#%%
debug = True
tacxImg = bt.imagelib.cropImageTLBR(frame, tlt, brt, debug)
# garminImg = bt.imagelib.cropImageTLBR(frame, tlg, brg, False)

powerImg = bt.imagelib.cropImageTLBR(tacxImg, tlp, brp, debug)

powerImgKmeans = bt.digit.extractDigitKmeans(powerImg, showImage = debug)

dictIsolated = bt.digit.isolateDigit(powerImgKmeans, nrows = 1, ncols = 3, thresholdPerc = 0.1, showImage = debug)

power = bt.digit.getValueOnDict7Segments(dictIsolated, minFill = 0.3, whRatioOne = 0.25, whRatioInvalid = 1, showImage = debug, printFilling = debug)

print(power)

# font 
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(tacxImg, ("{:03d}".format(power)), (0,20), font, 0.5, (0,0,255), 1, cv2.LINE_AA)

bt.imagelib.plotImage(tacxImg)
