# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 00:07:44 2022

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
import tensorflow as tf
# import everything from the preparation script
import AAApreliminary as config
import skimage

#%% flags
TEST_DATE = '20221214'
TACX_GARMIN = 'tmp'
assert TACX_GARMIN in ['tacx', 'garmin', 'tmp']
debug = False
REMOVE_FILE = True
N_LAST_FILES = 5
#%% build directories
videoInputDir = config.DICT['DIR']['02_preproc DIR'].replace('TEST_DATE', TEST_DATE)
files, dirs = basic.utils.find_files_and_dirs_in_dir(videoInputDir, printOutput = False)
video = files[-1]

imageDir = config.DICT['DIR']['img DIR'].replace('TEST_DATE', TEST_DATE)
imageInputDir = os.path.join(imageDir, 'tmp', 'to be checked')
imageInputDir = os.path.join(imageDir, 'tacx', 'N')
imageOutputDir = os.path.join(imageDir, 'tacx')

#%% model
model = tf.keras.models.load_model('m_tacx540.h5')

listOfLastFiles = [[]]*(N_LAST_FILES-1) # circular memory storing the

# for directory in basic.utils.list_dirs_in_this_dir(imageInputDir):
for directory in [imageInputDir]:
    files = basic.utils.list_files_in_this_dir(directory)
    totalFrames = len(files)
    for filename in tqdm(files):
        
        # load img from file
        value = cv2.cvtColor(cv2.imread(filename),cv2.COLOR_BGR2GRAY)
         
        guess, _ = bt.digit.recClass.detDigFromImg(value, model)
        valueRescaled = basic.imagelib.rescaleToMaxPixel(value, 1000)
        vrCopy = valueRescaled.copy()
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(vrCopy, ("{:02d}".format(guess)), (0,int(vrCopy.shape[0]/2)), 
                    font, 5, (127), 10, cv2.LINE_AA)
                    
        while True:
            imgName = 'press the corrispondent digit, [n] if no digit'
            cv2.imshow(imgName, vrCopy)
            key = cv2.waitKey(0)
            if key in [ord(str(i)) for i in range(10)] or key == ord('n') or key == ord('\r'): # enter key
                if key == ord('\r'):
                    if guess != 10:
                        char = str(guess)
                    elif guess == 10:
                        char = 'N'
                else:
                    char = chr(key)
                # print(char +' pressed')
                cv2.destroyWindow(imgName)
                break
            else:
                if key == ord('d'):
                    for _ in listOfLastFiles:                        
                        print(_)
                cv2.destroyWindow(imgName)
                continue
            
            
        # FIRST REMOVE FILE AND THEN SAVE IT, OTHERWISE, IF SAME FOLDER, IT'S LOST
        if REMOVE_FILE:
            os.remove(filename)
        imgSaveName = os.path.split(filename)[1]
        cv2.imwrite(os.path.join(imageOutputDir, char, imgSaveName), value)
        listOfLastFiles.append(os.path.join(imageOutputDir, char, imgSaveName))
        listOfLastFiles = listOfLastFiles[-N_LAST_FILES:]
        

        # print(os.path.join(imageOutputDir, char, imgSaveName))

print(basic.utils.count_files_in_dirs_inside_this_dir(imageOutputDir))




