# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 00:22:32 2023

@author: eferlius
"""

import pandas as pd
import cv2
import os
import bikeTrackLib as bt
import basic
import numpy as np
from tqdm import tqdm
# import everything from the preparation script
import AAApreliminary as config

#%%
TEST_DATE = '20230104'
TACX_GARMIN = 'tacx'
assert TACX_GARMIN in ['tacx', 'garmin']
START_INDEX = 7235

def from_value_to_digits(value):
    values = []
    if value == 0:
        return [0]
    if value < 0:
        value = - value
    for i in range(int(np.ceil(np.log10(value)))):
        values.append(int(np.floor((value%(10**(i+1)))/(10**(i)))))
    values.reverse()
    return values
        
#%%
videoInputDir = config.DICT['DIR']['01_raw DIR'].replace('TEST_DATE', TEST_DATE)
files, dirs = basic.utils.find_files_and_dirs_in_dir(videoInputDir, 
listPartialName='-ext', listExt='.avi', printOutput = False)
video = files[-1]

csvInputDir = config.DICT['DIR']['csv dig extr DIR'].replace('TEST_DATE', TEST_DATE)
files, dirs = basic.utils.find_files_and_dirs_in_dir(csvInputDir, 
listPartialName='digitsIntervals', printOutput = False)
csvInput = files[-1]

imageOutputDir = config.DICT['DIR']['img DIR'].replace('TEST_DATE', TEST_DATE)
imageOutputDir = os.path.join(imageOutputDir, TACX_GARMIN)


print(basic.utils.count_files_in_dirs_inside_this_dir(imageOutputDir))

df = pd.read_csv(csvInput, header = None)

frameIndexes = df.index.values
frameValues = df[0].values
#%%
#exclude edges of transition
indexes = np.where(np.diff(frameValues) != 0)[0]

indexesToRemove = np.concatenate((indexes,indexes+1))
indexesToRemove.sort()

frameIndexes = np.delete(frameIndexes, indexesToRemove)
# frameValues = np.delete(frameValues, indexesToRemove)

toBeChecked = []

for frameIndex in tqdm(frameIndexes):
    if frameIndex >= START_INDEX:
        img = basic.imagelib.getFrameFromVideo(video, frameIndex)[:,:,0]
        #apply thresholding hence the saving in avi format compresses the video
        ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        
        frameValue = frameValues[frameIndex]
        digits = from_value_to_digits(frameValue)
        
        imagesDict = bt.digit.extr.isolateDigitTLBRprojectionInside(img, discValue= 1, 
                                                                 showImage = False)
        
        listImagesDictKeys = list(imagesDict.keys())
        listImagesDictValues = list(imagesDict.values())
        
        if len(listImagesDictKeys) != len(digits):
            # print('different len for {}'.format(frameIndex))
            toBeChecked.append(frameIndex)
            continue
        
        for coord, value, digit in zip(listImagesDictKeys, listImagesDictValues, digits):
        
            
            imgSaveName = "{:07d}".format(frameIndex)+coord+'.jpg'
            cv2.imwrite(os.path.join(imageOutputDir, str(digit), imgSaveName), value)
            
            if frameIndex == 55:
                basic.sound.playBeep()
                pass
    
    
    
    
    
    



