# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:15:12 2022

@author: eferlius
"""

import cv2
import os
import time
import datetime
import basic
import bikeTrackLib as bt
import numpy as np
import bikeTrackLib.blocksTraining as btbt
# import everything from the preparation script
import AAApreliminary as config

#%%
thisMoment = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S')
videoName = 'test' + thisMoment

videoPath = os.path.join(config.DICT['DIR']['new rec DIR'], videoName+'.avi')
videoPathExtr = os.path.join(config.DICT['DIR']['new rec DIR'], videoName+'-extr.avi')
csvPath = os.path.join(config.DICT['DIR']['new rec DIR'], videoName+'.csv')

INTERVAL_WRITE_CSV = 30
# set the recording DURATION
DURATION = 7200 #seconds
LAP_DURATION = 180
WAIT_TIME = 60

#%% define training
wu = btbt.Block(300,150)
s1 = btbt.Block(180,180)
s2 = btbt.Block(180,200)
s3 = btbt.Block(180,190)
s4 = btbt.Block(180,210)
s5 = btbt.Block(180,190)
s6 = btbt.Block(180,200)
s7 = btbt.Block(180,180)
cd = btbt.Block(300,150)

listOfBlocks = [wu,s1,s2,s3,s4,s5,s6,s7,cd]

training = btbt.Training(listOfBlocks)

training.plotTraining()

#%%
timeArray = []

capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read()
    if ret:
        try:
            cv2.imshow('video', frame)
        except:
            pass
    # press esc to exit
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()

ret, frame = capture.read()
tl, br = basic.imagelib.getCoords_user(frame, nPoints = 3, title = 'Tacx BASIC - ')
print('tl = ' + str(tl))
print('br = ' + str(br))

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
videoWriter = cv2.VideoWriter(videoPath, fourcc, 30.0, (640,480))
videoWriterExtr = cv2.VideoWriter(videoPathExtr, fourcc, 30.0, ((int(np.array(br[0]-tl[0])),int(np.array(br[1]-tl[1])))))

basic.countdown.Countdown(WAIT_TIME)

timer = basic.timer.Timer() # to count the total time
lapTimer = basic.timer.Timer() # to monitor the laps
csvTimer = basic.timer.Timer() # to decide when to write on the csv file

counter = 0
elapsed = 0

while (elapsed < DURATION):
    counter+=1
    ret, frame = capture.read()
     
    if ret:
        # cv2.imshow('video', frame)
        videoWriter.write(frame)

        try:
            # crop on roi
            img_rgb = basic.imagelib.cropImageTLBR(frame, tl, br, False)
    
            # k means for making the digits pop out
            # returns image with [0,0,0] and [255,255,255]
            img_highlight, segmentedImg = bt.digit.extr.extractDigitKmeansLoop(img_rgb, 
            k=3, showImage=False, nIter=0, highlightValue = [0,0,0])
            
            # basic.imagelib.rescaleToMaxPixel(img_highlight, 1000)

            cv2.imshow('video', basic.imagelib.rescaleToMaxPixel(img_highlight, 1000))
            videoWriterExtr.write(img_highlight)

        except:
            pass

    laptime = lapTimer.elap(printTime=False)
    elapsed = timer.elap(printTime=False)
    csvTime = csvTimer.elap(printTime=False)
    timeArray.append([elapsed])
    
    # press esc to exit
    if cv2.waitKey(1) == 27:
        break

    if laptime > LAP_DURATION:
        lapTimer.reset()
        basic.sound.playFreq(startFreq = 1000)
        
    if csvTime > INTERVAL_WRITE_CSV:
        # basic.sound.playFreq(startFreq = 500)
        basic.utils.write_rows_csv(csvPath, timeArray, mode = 'a')
        csvTimer.reset()
        timeArray = []
        

# write the last rows of timeArray
basic.utils.write_rows_csv(csvPath, timeArray, mode = 'a')

basic.sound.playFreq()
elapsed = timer.stop()
print('{c:.0f} frames in {e:.2f} seconds'.format(c=counter, e=elapsed))
print('{f:.2f} Hz'.format(f=(counter/elapsed)))

capture.release()
videoWriter.release()
videoWriterExtr.release()
 
cv2.destroyAllWindows()
