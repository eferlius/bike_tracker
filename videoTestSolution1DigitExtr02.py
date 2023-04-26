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
import tensorflow as tf
# import everything from the preparation script
import AAApreliminary as config


#%% flags
TEST_DATE = '20221212'
SAVE_VIDEO = False
PLAY_SOUND = False
WRITE_CSV = False
debug = False
#%% build directories
videoInputDir = config.DICT['DIR']['02_preproc DIR'].replace('TEST_DATE', TEST_DATE)
files, dirs = basic.utils.find_files_and_dirs_in_dir(videoInputDir, 
listPartialName='',printOutput = False)
video = files[-1]

videoOutputDir = config.DICT['DIR']['digit extr DIR'].replace('TEST_DATE', TEST_DATE)

csvOutputDir = config.DICT['DIR']['csv dig extr DIR'].replace('TEST_DATE', TEST_DATE)

#%% model 
model = tf.keras.models.load_model('m_tacx1900.h5')
#%% get frame
frame = basic.imagelib.getFrameFromVideo(video, 0, False, False)
videoName = os.path.split(video)[-1]

#%% crop frame
# tl, br = basic.imagelib.getCoords_user(frame, nPoints = 3, title = 'Tacx BASIC - ')
# print('tl = ' + str(tl))
# print('br = ' + str(br))

tl = [116, 352]
br = [260, 407]

# tl = [472, 332]
# br = [557, 389]

# tl = [61, 335]
# br = [221, 404]

#%% saving initialization
if SAVE_VIDEO:
    saveVideoName = videoName.replace('.avi',str(tl)+str(br)+'.avi')
    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    videoWriterK = cv2.VideoWriter(os.path.join(videoOutputDir, 
    saveVideoName.replace('.avi','-kmeans.avi')), fourcc, 30.0, (br[0]-tl[0],br[1]-tl[1]))

if WRITE_CSV:
   csv = os.path.join(csvOutputDir,videoName+str(tl)+str(br)+'.csv')
#%% play video
watts = []

# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture(video)

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video file")

 
# Read until video is completed
totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

timer = basTim.Timer()
# for i in tqdm(range(totalFrames)):
for i in tqdm(range(1000)):
# while(cap.isOpened()):
     
# Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        if i == -1:
            debug = True

        try:
            # crop on roi
            img_rgb = basic.imagelib.cropImageTLBR(frame, tl, br, False)
    
            # k means for making the digits pop out
            # returns image with [0,0,0] and [255,255,255]
            img_highlight, segmentedImg = bt.digit.extr.extractDigitKmeansLoop(img_rgb, 
            k=3, showImage=debug, nIter=1, highlightValue = [0,0,0])
            
            img0_255 = img_highlight[:,:,0]
            
            img = skimage.filters.rank.modal(img0_255, np.ones((3,3)))
            
            img = basic.imagelib.correctBorder(img, 'tr', trueValue = 255, 
            replaceValue = 0, showPlot = debug)
    
            dictDigitsImg = bt.digit.extr.isolateDigitTLBRprojectionInside(img, 
            showImage = debug)

            # power = bt.digit.recSevSegmArea.getValueOnDict7Segments(dictDigitsImg, minFill = 0.3, 
            # whRatioOne = 0.25, whRatioInvalid = 1, showImage = debug, 
            # printFilling = debug)
            power, tmp = bt.digit.recClass.getValueOnDictClass(dictDigitsImg, model)
            # print(tmp)

            watts.append(power)
            
            # for debugging with video saving
            # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            
            imgForVideo = img_rgb.copy()
            # font 
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(imgForVideo, ("{:07d}:{:03d}".format(i,power)), (0,20), 
                        font, 0.25, (0,0,255), 1, cv2.LINE_AA)
    
            t = timer.elap(printTime = False)
            if SAVE_VIDEO:
                # videoWriterO.write(imgOtsu)
                videoWriterK.write(imgForVideo)
            if WRITE_CSV:
                newRow = [str(i), "{:.4f}".format(t), power]
                basic.utils.write_row_csv(csv, newRow)
            if debug:
                pass
               #  plt.close('all')
        except:
            print('error occurred in the loop')
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

watts = np.array(watts)
basic.plots.plts([[],[]],[watts, watts[watts != -1]], listOfkwargs = [{'linewidth':'0'}]*2)
print(np.count_nonzero(watts == -1)/len(watts)*100)

