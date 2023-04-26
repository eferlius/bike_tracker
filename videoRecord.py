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
# import everything from the preparation script
import AAApreliminary as config

#%%
thisMoment = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S')
videoName = 'test' + thisMoment

videoPath = os.path.join(config.DICT['DIR']['new rec DIR'], videoName+'.avi')
csvPath = os.path.join(config.DICT['DIR']['new rec DIR'], videoName+'.csv')

INTERVAL_WRITE_CSV = 30
# set the recording DURATION
DURATION = 5400 #seconds
LAP_DURATION = 150
WAIT_TIME = 10

timeArray = []

capture = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
videoWriter = cv2.VideoWriter(videoPath, fourcc, 30.0, (640,480))


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
        cv2.imshow('video', frame)
        videoWriter.write(frame)

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
        basic.sound.playFreq(startFreq = 500)
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
 
cv2.destroyAllWindows()
