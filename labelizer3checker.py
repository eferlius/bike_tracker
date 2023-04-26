# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 23:30:11 2023

@author: eferlius
"""

import basic
import os
import pandas as pd
import basic
import cv2
import numpy as np
from tqdm import tqdm
import time
import datetime
import pandas as pd
import csv
# import everything from the preparation script
import AAApreliminary as config

ROI_NAMES = ['tacx power', 'garmin speed', 'garmin heart rate', 'garmin cadence']
TEST_DATE_LIST = ['20221204','20221205','20221209','20221212','20221214','20230102', '20230104']

STEP = 24
MAX_TIME_CSV_SAVING = 60


TEST_DATE =  TEST_DATE_LIST[-1]
ROI_NAME = ROI_NAMES[0]

#%% build directories
videoInputDir = config.DICT['DIR']['02_preproc DIR'].replace('TEST_DATE', TEST_DATE)
videoInputDir = config.DICT['DIR']['01_raw DIR'].replace('TEST_DATE', TEST_DATE)
files, dirs = basic.utils.find_files_and_dirs_in_dir(videoInputDir, 
listPartialName='-extr',printOutput = False)
video = files[-1]
videoName = os.path.split(video)[-1]

# get first frame to check dimension
cap = cv2.VideoCapture(video)
# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video file")  
ret, frame = cap.read()
valueRescaled = basic.imagelib.rescaleToMaxPixel(frame, 1000)
h, w, _ = valueRescaled.shape


videoOutputDir = config.DICT['DIR']['digit extr DIR'].replace('TEST_DATE', TEST_DATE)
os.makedirs(videoOutputDir, exist_ok = True)

csvInputDir = config.DICT['DIR']['csv dig extr DIR'].replace('TEST_DATE', TEST_DATE)
files, dirs = basic.utils.find_files_and_dirs_in_dir(csvInputDir, 
listPartialName='digitsIntervals', printOutput = False)
csvInput = files[-1]


fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
videoWriter = cv2.VideoWriter(os.path.join(videoOutputDir,videoName), fourcc, 30.0, (w,h))



#%%
try:
    data = pd.read_csv(csvInput, header = None)
    values = data.iloc[:,0].values
    # values = values.reshape(len(values),1)
except:
    pass
cap.release()
cap = cv2.VideoCapture(video)
for counter in tqdm(range(len(values))):
    try: 
        ret, frame = cap.read()
         
        if ret:
            valueRescaled = basic.imagelib.rescaleToMaxPixel(frame, 1000)
    
            vrCopy = valueRescaled.copy()
    
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(vrCopy, ("{:07d}:{:03.0f}".format(counter, values[counter])), (0,int(vrCopy.shape[0]/2)), 
                        font, 2, (255,0,0), 4, cv2.LINE_AA)
            
            videoWriter.write(vrCopy)
    except:
        pass
    
cap.release()
videoWriter.release()


        
    