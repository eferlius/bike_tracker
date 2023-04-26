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
# import everything from the preparation script
import AAApreliminary as config

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

tl, br = basic.imagelib.getCoords_user(frame, nPoints = 3, title = 'Tacx BASIC - ')
print('tl = ' + str(tl))
print('br = ' + str(br))

timer = basic.timer.Timer() # to count the total time
lapTimer = basic.timer.Timer() # to monitor the laps
csvTimer = basic.timer.Timer() # to decide when to write on the csv file

counter = 0
elapsed = 0

while True:
    counter+=1
    ret, frame = capture.read()
     
    if ret:
        # cv2.imshow('video', frame)

        try:
            # crop on roi
            img_rgb = basic.imagelib.cropImageTLBR(frame, tl, br, False)
    
            # k means for making the digits pop out
            # returns image with [0,0,0] and [255,255,255]
            img_highlight, segmentedImg = bt.digit.extr.extractDigitKmeansLoop(img_rgb, 
            k=3, showImage=False, nIter=0, highlightValue = [0,0,0])
            
            basic.imagelib.rescaleToMaxPixel(img_highlight, 1000)

            cv2.imshow('video', basic.imagelib.rescaleToMaxPixel(img_highlight, 1000))

        except:
            pass

    laptime = lapTimer.elap(printTime=False)
    elapsed = timer.elap(printTime=False)
    csvTime = csvTimer.elap(printTime=False)
    timeArray.append([elapsed])
    
    # press esc to exit
    if cv2.waitKey(1) == 27:
        break


basic.sound.playFreq()
elapsed = timer.stop()
print('{c:.0f} frames in {e:.2f} seconds'.format(c=counter, e=elapsed))
print('{f:.2f} Hz'.format(f=(counter/elapsed)))

capture.release()
 
cv2.destroyAllWindows()
