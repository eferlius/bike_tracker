# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 17:23:58 2023

@author: eferlius
"""

import cv2
import os
import time
import datetime
import basic
import bikeTrackLib as bt
import numpy as np
import matplotlib.pyplot as plt
import bikeTrackLib.blocksTraining as btbt
# import everything from the preparation script
import AAApreliminary as config

#%%
thisMoment = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S')
videoName = 'test' + thisMoment

videoPath = os.path.join(config.DICT['DIR']['new rec DIR'], videoName+'.avi')
videoPathExtr = os.path.join(config.DICT['DIR']['new rec DIR'], videoName+'-extr.avi')
csvPath = os.path.join(config.DICT['DIR']['new rec DIR'], videoName+'.csv')
trainingCSVPath = os.path.join(config.DICT['DIR']['new rec DIR'], videoName+'-protocol.csv')

INTERVAL_WRITE_CSV = 30
# set the recording DURATION
DURATION = 0 #seconds
LAP_DURATION = 180
WAIT_TIME = 60

#%% define training

blockTime = 300
training = btbt.Training()



training.addBlock(blockTime, 150)
# training.addBlock(blockTime, 180)
# training.addBlock(blockTime, 200)
# training.addBlock(blockTime, 190)
# training.addBlock(blockTime, 210)
# training.addBlock(blockTime, 200)
# training.addBlock(blockTime, 220)
# training.addBlock(blockTime, 200)
# training.addBlock(blockTime, 210)
# training.addBlock(blockTime, 190)
# training.addBlock(blockTime, 200)
# training.addBlock(blockTime, 180)
# training.addBlock(blockTime, 200)
# training.addBlock(blockTime, 190)
# training.addBlock(blockTime, 210)
# training.addBlock(blockTime, 200)
# training.addBlock(blockTime, 220)
# training.addBlock(blockTime, 200)
# training.addBlock(blockTime, 210)
# training.addBlock(blockTime, 190)
# training.addBlock(blockTime, 200)
# training.addBlock(blockTime, 180)
# training.addBlock(120, 200)
# training.addBlock(120, 220)
# training.addBlock(120, 240)
# training.addBlock(120, 220)
# training.addBlock(120, 200)
# training.addBlock(120, 180)

for i in range(6):
        training.addBlock(30, 270)
        training.addBlock(150, 150)
        
# training.addBlock(120, 180)
# training.addBlock(120, 200)
# training.addBlock(120, 220)
# training.addBlock(120, 240)
# training.addBlock(120, 220)
# training.addBlock(120, 200)
# training.addBlock(120, 180)
training.addBlock(blockTime, 150)

training.create()
training.plotTraining()
training.to_csv(trainingCSVPath)
DURATION = training.tot_duration
# training.plotTraining()
print(DURATION/60)

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
plt.close('all')

timer = basic.timer.Timer() # to count the total time
lapTimer = basic.timer.Timer() # to monitor the laps
csvTimer = basic.timer.Timer() # to decide when to write on the csv file

counter = 0
elapsed = 0
oldBlockIndex = 0

font = cv2.FONT_HERSHEY_SIMPLEX

while (elapsed < DURATION):
    
    ret, frame = capture.read()
     
    if ret:
        counter+=1
        # cv2.imshow('video', frame)
        videoWriter.write(frame)
        
        elapsed = timer.elap(printTime=False)
        csvTime = csvTimer.elap(printTime=False)
        timeArray.append([elapsed])
        
        power, elapsed_this_block, left_this_block, left_total, blockIndex = training.checkBlock(elapsed)
        
        if oldBlockIndex != blockIndex:
            oldBlockIndex = blockIndex
            basic.sound.playFreq(startFreq = 1000)
            
        try:
            # crop on roi
            img_rgb = basic.imagelib.cropImageTLBR(frame, tl, br, False)
    
            # k means for making the digits pop out
            # returns image with [0,0,0] and [255,255,255]
            img_highlight, segmentedImg = bt.digit.extr.extractDigitKmeansLoop(img_rgb, 
            k=3, showImage=False, nIter=0, highlightValue = [0,0,0])
            
            # basic.imagelib.rescaleToMaxPixel(img_highlight, 1000)
            videoWriterExtr.write(img_highlight)
            
            vrCopy = basic.imagelib.rescaleToMaxPixel(img_highlight, 1500)
            
            y_coord = int(vrCopy.shape[0]/7)
            
            
            cv2.putText(vrCopy, ("{:06.2f}W".format(power)), 
                        (0,y_coord), font, 4, (0,0,255), 12, cv2.LINE_AA)
            cv2.putText(vrCopy, ("{:06.2f}s".format(elapsed_this_block)), 
                        (0,3*y_coord), font, 4, (0,0,255), 12, cv2.LINE_AA)
            cv2.putText(vrCopy, ("{:06.2f}s".format(left_this_block)), 
                        (0,5*y_coord), font, 4, (0,0,255), 12, cv2.LINE_AA)
            cv2.imshow('video', vrCopy)
            
        except:
            pass

    # press esc to exit
    if cv2.waitKey(1) == 27:
        break

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
