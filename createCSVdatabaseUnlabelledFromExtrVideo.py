# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 15:39:47 2023

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
TEST_DATE = '20230105'
TACX_GARMIN = 'tacx'
assert TACX_GARMIN in ['tacx', 'garmin']
N = -1
WRITE_ROW_EVERY = 10000
START_INDEX = -1

for TEST_DATE in ['20230105','20230109','20230111','20230116','20230117','20230118']:
    #%% build directories
    videoInputDir = config.DICT['DIR']['01_raw DIR'].replace('TEST_DATE', TEST_DATE)
    files, dirs = basic.utils.find_files_and_dirs_in_dir(videoInputDir, printOutput = False, listPartialName='-ext', listExt = '.avi')
    video = files[-1]
    
    imageOutputDir = config.DICT['DIR']['img DIR'].replace('TEST_DATE', TEST_DATE)
    imageOutputDir = os.path.join(imageOutputDir, TACX_GARMIN)
    
    csvFileDir = config.DICT['DIR']['csv db DIR'].replace('TEST_DATE', TEST_DATE)
    csvFilePath = os.path.join(csvFileDir, 'nolabels.csv')
    
    #%% get frame
    frame = basic.imagelib.getFrameFromVideo(video, 0, False, False)
    
    videoName = os.path.split(video)[-1]
    #%% 
    newRow = ['frame', 'tl c0', 'tl c1', 'br c0', 'br c1']
    featColNames = ['f{:03d}'.format(i) for i in range(28*28)]
    newRow.extend(featColNames)
    # newRow.extend(['bookmark'])
    basic.utils.write_row_csv(csvFilePath,newRow, mode = 'w')
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(video)
    
    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video file")
    
    # Read until video is completed
    totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    toBeChecked = []
    rows = []
    counter = -1
    
    frameIndexes = np.arange(totalFrames)
    
    for i in tqdm(range(totalFrames)):
        ret, img = cap.read()
        img = img[:,:,0]
        if ret == True:
            if i in frameIndexes:
                try:
                    frameIndex = i
                    if frameIndex >= START_INDEX:
                        #apply thresholding hence the saving in avi format compresses the video
                        ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
                        
                        imagesDict = bt.digit.extr.isolateDigitTLBRprojectionInside(img, discValue= 1, 
                                                                                 showImage = False)
                        listImagesDictKeys = list(imagesDict.keys())
                        listImagesDictValues = list(imagesDict.values())
                        
                        for coord, value in zip(listImagesDictKeys, listImagesDictValues):
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
                                             str(br_tot[0]), str(br_tot[0])]
                            newRow.extend(arr.tolist())
                            rows.append(newRow)   
                    
                            if counter >= WRITE_ROW_EVERY:
                                basic.utils.write_rows_csv(csvFilePath,rows)
                                counter = -1
                                rows = []  
                                basic.sound.playBeep()  
                except:
                    toBeChecked.append(i)
                    pass
                
    basic.utils.write_rows_csv(csvFilePath,rows)
    
    # When everything done, release
    # the video capture object
    cap.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()




