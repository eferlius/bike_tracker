# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 23:00:00 2022

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
import skimage
import pandas as pd
# import everything from the preparation script
import AAApreliminary as config

TEST_DATE_LIST = ['20221204','20221205','20221209','20221212','20221214','20230102']
#%% flags
for TEST_DATE in TEST_DATE_LIST:
    print(TEST_DATE)
    # TEST_DATE = '20230102'
    SAVE_VIDEO = True
    PLAY_SOUND = False
    WRITE_CSV = True
    debug = False
    #%% build directories
    videoInputDir = config.DICT['DIR']['02_preproc DIR'].replace('TEST_DATE', TEST_DATE)
    files, dirs = basic.utils.find_files_and_dirs_in_dir(videoInputDir, 
    listPartialName='',printOutput = False)
    video = files[-1]
    videoName = os.path.split(video)[-1]
    
    videoOutputDir = config.DICT['DIR']['digit extr DIR'].replace('TEST_DATE', TEST_DATE)
    csvOutputDir = config.DICT['DIR']['csv dig extr DIR'].replace('TEST_DATE', TEST_DATE)
    os.makedirs(videoOutputDir, exist_ok = True)
    os.makedirs(csvOutputDir, exist_ok = True)
    
    csvRoiInfo = os.path.join(csvOutputDir,videoName.replace('.avi','-roi location.csv'))

    df = pd.read_csv(csvRoiInfo)
    
    for index, row in df.iterrows():
        name = row['roiName']
        tl = [row['tl[0]'],row['tl[1]']]
        br = [row['br[0]'],row['br[1]']]
        
    
        #%% saving initialization
        if SAVE_VIDEO:
            saveVideoName = videoName.replace('.avi',str(tl)+str(br)+'.avi')
            fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
            videoWriterK = cv2.VideoWriter(os.path.join(videoOutputDir, 
            saveVideoName.replace('.avi','-{}-kmeans.avi'.format(name))), fourcc, 
            30.0, (int(np.array(br[0]-tl[0])),int(np.array(br[1]-tl[1])*3)))
        
        if WRITE_CSV:
            csv = os.path.join(csvOutputDir,videoName+str(tl)+str(br)+'.csv')
            
            newRow = ['frame', 'tl', 'bl', 'br', 'tr']
            basic.utils.write_row_csv(csv, newRow, mode = 'w')
        
        #%% play video
        
        # Create a VideoCapture object and read from input file
        cap = cv2.VideoCapture(video)
        
        # Check if camera opened successfully
        if (cap.isOpened() == False):
            print("Error opening video file")
        
        # Read until video is completed
        totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        timer = basTim.Timer()
        for i in tqdm(range(totalFrames)):
        # for i in tqdm(range(10)):
        # while(cap.isOpened()):
             
        # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
        
                if i == -1:
                    debug = True
        
                try:
                    # crop on roi
                    img_rgb = basic.imagelib.cropImageTLBR(frame, tl, br, False)
                    
                    try:
                        h, w = img_rgb.shape
                    except:
                        h, w, d = img_rgb.shape
            
                    # k means for making the digits pop out
                    # returns image with [0,0,0] and [255,255,255]
                    img_highlight, segmentedImg = bt.digit.extr.extractDigitKmeansLoop(img_rgb, 
                    k=3, showImage=debug, nIter=0, highlightValue = [0,0,0])
                    
                    img_borderCorrected, borderCorrFlag = \
                        basic.imagelib.correctBorderAllCorners(img_highlight, trueValue = 255, 
                                                               replaceValue = 0, showPlot = debug)            
                    
                    img0_255 = img_borderCorrected[:,:,0]
                    
                    img = skimage.filters.rank.modal(img0_255, np.ones((5,5)))
                    
                    img = cv2.merge([img, img, img])
                    
                    imgForVideo = cv2.vconcat([img_rgb, img_highlight, img])
                    
                    # basic.plots.pltsImg([imgForVideo])                    
                    
                    if SAVE_VIDEO:
                        videoWriterK.write(imgForVideo)
                    if WRITE_CSV:
                        newRow = [i]
                        newRow.extend(borderCorrFlag)
                        basic.utils.write_row_csv(csv, newRow)
                    
                except:
                    print('error occurred in the loop at iteration {}'.format(i))
                    pass
        # Break the loop
            else:
                break
        
        # When everything done, release
        # the video capture object
        cap.release()
        if SAVE_VIDEO:
            videoWriterK.release()
        
        # Closes all the frames
        cv2.destroyAllWindows()
        
        # tell the user the elaboration is done with a sound signal
        if PLAY_SOUND:
            basic.sound.playFreq()
    


