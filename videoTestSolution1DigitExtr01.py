# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 23:00:00 2022

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
import bikeTrackLib.screenMorphology as btsm

#%% flags
SAVE_VIDEO = True
PLAY_SOUND = False
WRITE_CSV = True
#%% get frame
videoDirectory = config.DICT['DIR']['0_raw videos DIR']

video = basic.utils.findFileInDirectory(videoDirectory,'')[-1]
frame = bt.imagelib.getFrameFromVideo(video, 50000, False, False)

videoName = os.path.split(video)[-1]

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

#%% saving initialization
if SAVE_VIDEO:
    saveVideoName = videoName.replace('.avi',str(tl)+str(br)+'.avi')
    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    videoWriterK = cv2.VideoWriter(os.path.join(config.DICT['DIR']['1_digitExtract videos DIR'], saveVideoName.replace('.avi','-kmeans.avi')), fourcc, 30.0, (br[0]-tl[0],br[1]-tl[1]))

if WRITE_CSV:
   csvDirectory = config.DICT['DIR']['csv DIR']

   csv = os.path.join(csvDirectory,videoName+str(tl)+str(br)+'.csv')
#%% play video
watts = []

# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture(video)
 
# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video file")

 
# Read until video is completed
totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

debug = False

timer = basTim.Timer()
for i in tqdm(range(totalFrames)):
# for i in tqdm(range(1000)):
# while(cap.isOpened()):
     
# Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        if i == -1:
            debug = True

        tacxImg = bt.imagelib.cropImageTLBR(frame, tlt, brt, debug)
        # garminImg = bt.imagelib.cropImageTLBR(frame, tlg, brg, False)

        powerImg = bt.imagelib.cropImageTLBR(tacxImg, tlp, brp, debug)


        powerImgKmeans = bt.digit.extractDigitKmeans(powerImg, showImage = debug)

        dictIsolated = bt.digit.isolateDigit(powerImgKmeans, nrows = 1, ncols = 3, thresholdPerc = 0.1, showImage = debug)

        power = bt.digit.getValueOnDict7Segments(dictIsolated, minFill = 0.3, whRatioOne = 0.25, whRatioInvalid = 1, showImage = debug, printFilling = debug)

        watts.append(power)

        # font 
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(tacxImg, ("{:07d}:{:03d}".format(i,power)), (0,20), font, 0.5, (0,0,255), 1, cv2.LINE_AA)

        t = timer.elap(printTime = False)
        if SAVE_VIDEO:
            # videoWriterO.write(imgOtsu)
            videoWriterK.write(tacxImg)
        if WRITE_CSV:
            newRow = ["{:.4f}".format(t), power]
            basic.utils.writeCSV(csv, newRow)
        if debug:
            plt.close('all')
# Break the loop
    else:
        break

# When everything done, release
# the video capture object
cap.release()
if SAVE_VIDEO:
    videoWriterK.release()

# Closes all the frames
cv2.destroyAllWindows()

# tell the user the elaboration is done with a sound signal
if PLAY_SOUND:
    basic.utils.playSound()

watts = np.array(watts)
plt.figure()
plt.plot(watts,'.-')
print(watts.count(-1)/len(watts)*100)

watts = watts[watts != 3]
plt.figure()
plt.plot(watts,'.-')
