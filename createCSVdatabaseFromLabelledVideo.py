# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 11:15:37 2023

@author: eferlius
"""

import cv2
import pandas as pd
import os
import time
import datetime
import bikeTrackLib as bt
import basic
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
# import basic.timer as basTim
# import skimage
# # make a prediction for a new image.
# from numpy import argmax
# from tensorflow.keras.utils import load_img
# from tensorflow.keras.utils import img_to_array
# from keras.models import load_model
# import random
# import everything from the preparation script
import AAApreliminary as config
#%% flags
TEST_DATE = '20230104'
TACX_GARMIN = 'tacx'
assert TACX_GARMIN in ['tacx', 'garmin']
N = -1
WRITE_ROW_EVERY = 10000
START_INDEX = -1
#%% functions
# load and prepare the image
# def load_image(filename):
#  	# load the image
#  	img = load_img(filename, color_mode = 'grayscale', target_size=(28, 28))
#  	# convert to array
#  	img = img_to_array(img)
#  	# reshape into a single sample with 1 channel
#  	img = img.reshape(1, 28, 28, 1)
#  	# prepare pixel data
#  	img = img.astype('float32')
#  	img = img / 255.0
#  	return img

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

#%% build directories
videoInputDir = config.DICT['DIR']['01_raw DIR'].replace('TEST_DATE', TEST_DATE)
files, dirs = basic.utils.find_files_and_dirs_in_dir(videoInputDir, 
listPartialName='-ext', listExt='.avi', printOutput = False)
video = files[-1]

csvInputDir = config.DICT['DIR']['csv dig extr DIR'].replace('TEST_DATE', TEST_DATE)
files, dirs = basic.utils.find_files_and_dirs_in_dir(csvInputDir, 
listPartialName='digitsIntervals', printOutput = False)
csvInput = files[-1]

csvFileDir = config.DICT['DIR']['csv db DIR'].replace('TEST_DATE', TEST_DATE)
csvFilePath = os.path.join(csvFileDir, 'until{num}.csv'.format(num=N))

df = pd.read_csv(csvInput, header = None)

frameIndexes = df.index.values
frameValues = df[0].values
#%%

newRow = ['frame', 'tl c0', 'tl c1', 'br c0', 'br c1', 'digit']
featColNames = ['f{:03d}'.format(i) for i in range(28*28)]
newRow.extend(featColNames)
# newRow.extend(['bookmark'])
basic.utils.write_row_csv(csvFilePath,newRow, mode = 'w')

#exclude edges of transition
indexes = np.where(np.diff(frameValues) != 0)[0]

indexesToRemove = np.concatenate((indexes,indexes+1))
indexesToRemove.sort()

frameIndexes = np.delete(frameIndexes, indexesToRemove)
# frameValues = np.delete(frameValues, indexesToRemove)

toBeChecked = []
rows = []
counter = -1
# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture(video)

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video file")

# Read until video is completed
totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


for i in tqdm(range(totalFrames)):
    ret, img = cap.read()
    img = img[:,:,0]
    if ret == True:
        if i in frameIndexes:
            frameIndex = i
            if frameIndex >= START_INDEX:
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
                    counter += 1
                    
                    # find local tl
                    ini = coord.index('[') + 1
                    fin = coord.index(']')
                    tmp = coord[ini:fin]
                    tl_tot = np.array(list(tmp.split(", "))).astype(int)
                    
                    # find local br
                    coord = coord[coord.index('-'):]
                    ini = coord.index('[') + 1
                    fin = coord.index(']')
                    tmp = coord[ini:fin]
                    br_tot = np.array(list(tmp.split(", "))).astype(int)
                    
                    
                    arr = bt.digit.recClass.fromImgToArr(value).reshape(28*28)
                    
                    newRow = [str(frameIndex), str(tl_tot[0]), str(tl_tot[1]), 
                                     str(br_tot[0]), str(br_tot[0]), str(digit)]
                    newRow.extend(arr.tolist())
                    rows.append(newRow)   
            
                    if counter >= WRITE_ROW_EVERY:
                        basic.utils.write_rows_csv(csvFilePath,rows)
                        counter = -1
                        rows = []  
                        basic.sound.playBeep()    
            
basic.utils.write_rows_csv(csvFilePath,rows)