# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 17:23:58 2023

@author: eferlius
"""

# import cv2
import keyboard
import os
import time
import datetime
import basic
import numpy as np
import matplotlib.pyplot as plt
import bikeTrackLib.blocksTraining as btbt
# import pyautogui
import ctypes
# import everything from the preparation script
import AAApreliminary as config
import figure_parameters

ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)

#%%
thisMoment = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S')
videoName = 'test' + thisMoment

csvPath = os.path.join(config.DICT['DIR']['new rec DIR'], videoName+'.csv')
trainingCSVPath = os.path.join(config.DICT['DIR']['new rec DIR'], videoName+'-protocol speed.csv')

WAIT_TIME = 60
WORKING_FREQ = 5

#%% define training

blockTime = 180
training = btbt.Training()

training.addBlocksRamp(30, 20, 27, 1)

training.addBlocksPyramidsUpDown(blockTime, 27, 34, 3)


training.addBlocksRamp(30, 27, 20, 1)

training.create()
print(training.tot_duration/60)
#training.plotTraining()


#%%
training.to_csv(trainingCSVPath)
#%%
plt.close('all')
plt.ion()
fig = plt.figure()
fig.suptitle('countdown started, get ready')
plt.pause(0.1)

times = []
basic.countdown.Countdown(WAIT_TIME)

timer = basic.timer.Timer() # to count the total time
screen_saver_timer = basic.timer.Timer()

counter = 0
elapsed = 0
oldBlockIndex = 0

# plt.ion()
# fig = plt.figure()
fig.suptitle('press esc to exit', fontsize= 10)
ax = fig.add_subplot(111)
training.plotTraining(ax)
ax.grid()
line1, = ax.plot([0,0],[0,np.max(training.params)], linewidth = 3, linestyle='--', markersize=10, marker = 'o')


while (elapsed < training.tot_duration):
    counter+=1
    
    elapsed = timer.elap(printTime=False)
    
    power, elapsed_this_block, left_this_block, left_total, blockIndex = training.checkBlock(elapsed)
    
    if oldBlockIndex != blockIndex:
        oldBlockIndex = blockIndex
        basic.sound.playFreq(startFreq = 1000)
        
    # power, elapsed_this_block, left_this_block, left_total, blockIndex = self.checkBlock(t.elap(printTime=False))
    line1.set_xdata([elapsed/60]*2)
    ax.set_title("{:05.2f} km/h [{:06.2f}s - {:06.2f}s]".format(power, elapsed_this_block, left_this_block))
    fig.canvas.draw()
    fig.canvas.flush_events()
    try:
        time.sleep(1/WORKING_FREQ-(timer.elap(printTime=False)-elapsed))
    except:
        pass
    
    if keyboard.is_pressed("esc"):
        plt.close('all')
        break 
    times.append(timer.lap(printTime = False))
    
    # if screen_saver_timer.lap(printTime = False)>AVOID_SCREEN_SAVER_TIME:
    #     screen_saver_timer.reset()
    #     pyautogui.press('volumedown')
    #     pyautogui.press('volumeup')
            
ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
basic.sound.playFreq(startFreq = 1500)
elapsed = timer.stop()

basic.plots.plts([],[times])
plt.pause(0.1)
print('{c:.0f} frames in {e:.2f} seconds'.format(c=counter, e=elapsed))
print('{f:.2f} Hz'.format(f=(counter/elapsed)))

_ = input('press any key to close')
