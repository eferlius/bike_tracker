# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 13:14:38 2022

@author: eferlius

To test the popping out of digits on the region of interest
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
frame = bt.imagelib.getFrameFromVideo(video, 0, False, True)

videoName = os.path.split(video)[-1]

#%% crop frame
tl, br = bt.imagelib.getCoords_user(frame, nPoints = 2)

# print('tl = ' + str(tl))
# print('br = ' + str(br))

tl = [152, 238]
br = [267, 298]

# tl = [81, 253]
# br = [182, 304]

# tl = [75, 248]
# br = [189, 311]
#%%
if SAVE_VIDEO:
    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    videoWriterG = cv2.VideoWriter(os.path.join(config.DICT['DIR']['1_digitExtract videos DIR'], videoName+'-gauss.avi'), fourcc, 30.0, (br[0]-tl[0],br[1]-tl[1]))
    videoWriterO = cv2.VideoWriter(os.path.join(config.DICT['DIR']['1_digitExtract videos DIR'], videoName+'-otsu.avi'), fourcc, 30.0, (br[0]-tl[0],br[1]-tl[1]))
    videoWriterK = cv2.VideoWriter(os.path.join(config.DICT['DIR']['1_digitExtract videos DIR'], videoName+'-kmeans.avi'), fourcc, 30.0, (br[0]-tl[0],br[1]-tl[1]))


#%% play video

# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture(video)
 
# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video file")
 
# Read until video is completed
totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
for i in tqdm(range(totalFrames)):
# for i in tqdm(range(100)):
# while(cap.isOpened()):
     
# Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        img = bt.imagelib.cropImageTLBR(frame, tl, br, False)

        imgGauss = bt.digit.extractDigitGaussianThreshold(img)
        imgOtsu = bt.digit.extractDigitOtsuThreshold(img)
        imgKmeans = bt.digit.extractDigitKmeans(img)


        if SAVE_VIDEO:
            videoWriterG.write(imgGauss)
            videoWriterO.write(imgOtsu)
            videoWriterK.write(imgKmeans)

# Break the loop
    else:
        break
 
# When everything done, release
# the video capture object
cap.release()
if SAVE_VIDEO:
    videoWriterG.release()
    videoWriterO.release()
    videoWriterK.release()

# Closes all the frames
cv2.destroyAllWindows()

# tell the user the elaboration is done with a sound signal
if PLAY_SOUND:
    basic.utils.playSound()
