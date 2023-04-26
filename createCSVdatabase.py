# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 09:23:17 2022

@author: eferlius

From all the images in the subfolders, creates a database
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
import skimage
# make a prediction for a new image.
from numpy import argmax
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from keras.models import load_model
import random
# import everything from the preparation script
import AAApreliminary as config
#%% flags
TEST_DATE = '20230104'
TACX_GARMIN = 'tacx'
assert TACX_GARMIN in ['tacx', 'garmin']
N = -1
#%% functions
# load and prepare the image
def load_image(filename):
 	# load the image
 	img = load_img(filename, color_mode = 'grayscale', target_size=(28, 28))
 	# convert to array
 	img = img_to_array(img)
 	# reshape into a single sample with 1 channel
 	img = img.reshape(1, 28, 28, 1)
 	# prepare pixel data
 	img = img.astype('float32')
 	img = img / 255.0
 	return img

#%% build directories
videoInputDir = config.DICT['DIR']['02_preproc DIR'].replace('TEST_DATE', TEST_DATE)
files, dirs = basic.utils.find_files_and_dirs_in_dir(videoInputDir, printOutput = False)
video = files[-1]

imageOutputDir = config.DICT['DIR']['img DIR'].replace('TEST_DATE', TEST_DATE)
imageOutputDir = os.path.join(imageOutputDir, TACX_GARMIN)

csvFileDir = config.DICT['DIR']['csv db DIR'].replace('TEST_DATE', TEST_DATE)
csvFilePath = os.path.join(csvFileDir, 'until{num}.csv'.format(num=N))

print(basic.utils.count_files_in_dirs_inside_this_dir(imageOutputDir))
#%% loop with csv writing
for folder in (basic.utils.list_dirs_in_this_dir(imageOutputDir)):
    folderName = os.path.split(folder)[1]
    listOfFiles = basic.utils.list_files_in_this_dir(folder)
    random.shuffle(listOfFiles)
    try:
        for counter in tqdm(range(N)):
            file = listOfFiles[counter]
            frameNum = os.path.split(file)[1][0:7]
            if N > 0:
                if counter > N:
                    break
            else:
                floatArr = load_image(file).reshape(28*28)
                intArr = np.where(floatArr>=0.5,1,0)
                newRow = intArr.tolist()
                newRow.insert(0,folderName)
                newRow.insert(0,frameNum)
                
            basic.utils.write_row_csv(csvFilePath,newRow)
    except:
        print('\nreached max of {count} elements in {fName}'.format(count = counter,fName = folderName))
            
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        