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

#%% functions
def ask_value(i, video, precValue):
    done = False
    while not done:
        frame = basic.imagelib.getFrameFromVideo(video, i)
        # crop on roi
        # img_rgb = basic.imagelib.cropImageTLBR(frame, tl, br, False)

        img_rgb = frame.copy()
    
        valueRescaled = basic.imagelib.rescaleToMaxPixel(img_rgb, 1000)
    
        vrCopy = valueRescaled.copy()
    
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(vrCopy, ("{:03.0f}".format(precValue)), (0,int(vrCopy.shape[0]/2)), 
                    font, 5, (255,0,0), 10, cv2.LINE_AA)
        
        
        # user inserts value of the frame
        # - enter -> same value as before
        # - digits -> new value
        # - backspace -> show previous frame
        while True:
            done = False
            try:
                cv2.destroyWindow(imgName)
            except:
                pass
            imgName = 'frame {}'.format(i)
            cv2.imshow(imgName, vrCopy)
            
            key = cv2.waitKey(0)
            if key == ord('\r'): 
                # if enter, keep the same value as before
                done = True
                value = precValue
                cv2.destroyWindow(imgName)
                break
            elif key in [ord(str(_)) for _ in range(10)]:
                # if a value between 0 and 9 starts to read it from the keyboard
                digits = []
                while key != ord('\r'): # enter to finish
                    try:
                        digits.append(int(chr(key)))
                    except:
                        print('cannot convert character to int')
                    print('{}: {}'.format(i,digits))
                    key = cv2.waitKey(0)
                    
                    if key == ord('\b'):
                        print('backspace press, digits reset')
                        digits = []
                        key = ord('0')
                    
                value = 0
                for d,j in zip(digits,range(len(digits))):
                    value += d*10**(len(digits)-1-j) 
                print('{}: {}'.format(i,value))
                done = True
                cv2.destroyWindow(imgName)
                break
            elif key == ord('ù'):
                value = np.nan
                done = True
                cv2.destroyWindow(imgName)
                break
            elif key == ord('\b'):
                i-=1
                cv2.destroyWindow(imgName)
                break
            else:
                cv2.destroyWindow(imgName)
                continue
        
    return value, i

#%% build directories
videoInputDir = config.DICT['DIR']['02_preproc DIR'].replace('TEST_DATE', TEST_DATE)
videoInputDir = config.DICT['DIR']['01_raw DIR'].replace('TEST_DATE', TEST_DATE)
files, dirs = basic.utils.find_files_and_dirs_in_dir(videoInputDir, 
listPartialName='-extr',printOutput = False)
video = files[-1]
videoName = os.path.split(video)[-1]

videoOutputDir = config.DICT['DIR']['digit extr DIR'].replace('TEST_DATE', TEST_DATE)
csvOutputDir = config.DICT['DIR']['csv dig extr DIR'].replace('TEST_DATE', TEST_DATE)
os.makedirs(videoOutputDir, exist_ok = True)
os.makedirs(csvOutputDir, exist_ok = True)

csvRoiInfo = os.path.join(csvOutputDir,videoName.replace('.avi','-roi location.csv'))

#%%
# df = pd.read_csv(csvRoiInfo)

# for index, row in df.iterrows():
#     if row['roiName'] == ROI_NAME:
#         tl = [row['tl[0]'],row['tl[1]']]
#         br = [row['br[0]'],row['br[1]']]
#         break

# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture(video)

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video file")

# Read until video is completed
totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# totalFrames = 10

values = np.ones((totalFrames,1))*-1

files, dirs = basic.utils.find_files_and_dirs_in_dir(csvOutputDir, 
listPartialName='-extr-digitsIntervals',printOutput = False)

try:
    data = pd.read_csv(files[-1], header = None)
    values = data.iloc[:,0].values
    values = values.reshape(len(values),1)

except:
    pass

maxLen = totalFrames
# get the first two values
start = 0
end = STEP
value = 0
value, idx = ask_value(start, video, value)
values[idx] = value
value, idx = ask_value(end, video, value)
values[idx] = value

countLoop = 0
csvTimer = basic.timer.Timer()
while len(np.where(values == -1)[0])>=0: 
    countLoop+=1
    # index the values that are already recognized
    knownIndexes = np.where(values != -1)[0]
    # recognize the corresponding values
    knownValues = values[knownIndexes]
    
    # show them 
    # for idx, val in zip(knownIndexes, np.squeeze(knownValues).astype(int)):
    #     print('{:03.0f}: {:03.0f}'.format(idx, val))  
    # print('-'*10)
        
    if len(np.where(values == -1)[0])==0:
        break
    
    # identify only the indexes that are not consecutive
    knownNotConsecIndexes = np.append(knownIndexes[np.where(np.diff(knownIndexes)>1)[0]],knownIndexes[-1])
    # the analysis should start from the first not consecutive index
    start = knownNotConsecIndexes[0]
    
    # if there is another index further on, it's necessary to know what there is in between
    if len(knownNotConsecIndexes)>1:
        end = knownNotConsecIndexes[1]
        # if the values are the same, in fill in between with the same value
        if values[start] == values[end]:
            values[start:end] = values[start]
        # if the values are different, ask for a value in the middle (to the user)
        else:
            i = min(start+int((end-start)/2), maxLen-1)  
            value, idx = ask_value(i, video, value)
            values[idx] = [value]
            
    # if there isn't  another index, it's necessary to move forward 
    # of STEP elements and ask for the value (to the user)
    else:  
        i = min(start+STEP, maxLen-1) 
        value, idx = ask_value(i, video, value)
        values[idx] = [value]
    
    if csvTimer.elap(printTime = False)>MAX_TIME_CSV_SAVING:
        csvTimer.reset()
        basic.sound.playBeep()
        print('saving csv...')
        thisMoment = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S')
        csvDigitsPath = os.path.join(csvOutputDir,videoName.replace('.avi','-digitsIntervals{}.csv'.format(thisMoment)))
        basic.utils.write_rows_csv(csvDigitsPath, values)
        print('saving complete')

    print('loop executed: {:04d}, i: {:06d}/{} [{:03.0f}%]'.format(countLoop, i, maxLen, i/maxLen*100))
        
print('saving csv...')
thisMoment = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S')
csvDigitsPath = os.path.join(csvOutputDir,videoName.replace('.avi','-digitsIntervals{}.csv'.format(thisMoment)))
basic.utils.write_rows_csv(csvDigitsPath, values)
print('saving complete')
        
    