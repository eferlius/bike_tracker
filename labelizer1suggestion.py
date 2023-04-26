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
TACX_GARMIN = 'tacx'
assert TACX_GARMIN in ['tacx', 'garmin']
debug = False
maxCounter = 22
startFrameNum = 6700
#%% build directories
videoInputDir = config.DICT['DIR']['02_preproc DIR'].replace('TEST_DATE', TEST_DATE)
files, dirs = basic.utils.find_files_and_dirs_in_dir(videoInputDir, printOutput = False)
video = files[-1]

imageOutputDir = config.DICT['DIR']['img DIR'].replace('TEST_DATE', TEST_DATE)
imageOutputDir = os.path.join(imageOutputDir, TACX_GARMIN)

#%% get frame
frame = basic.imagelib.getFrameFromVideo(video, 0, False, False)

videoName = os.path.split(video)[-1]

#%% model
model = tf.keras.models.load_model('m_tacx400.h5')

#%% crop frame
# tl, br = basic.imagelib.getCoords_user(frame, nPoints = 3, title = 'Tacx BASIC - ')
# print('tl = ' + str(tl))
# print('br = ' + str(br))

tl = [67, 342]
br = [218, 399]

#%% play video
# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture(video)

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video file")

# Read until video is completed
totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


counter = 0
for i in tqdm(range(totalFrames)):
# for i in tqdm(range(1)):
# while(cap.isOpened()):
    if i >= startFrameNum:
        counter += 1
        if counter >= maxCounter:
            basic.sound.playFreq(500, blockExec = True, duration = 0.7)
            counter = 0
    #Capture frame-by-frame
    
        ret, frame = cap.read()
        if ret == True:
        
            try:
                frame = basic.imagelib.getFrameFromVideo(video, i)
                # crop on roi
                img_rgb = basic.imagelib.cropImageTLBR(frame, tl, br, False)
        
                # k means for making the digits pop out
                # returns image with [0,0,0] and [255,255,255]
                img_highlight, segmentedImg = bt.digit.extr.extractDigitKmeansLoop(img_rgb, 
                k=3, showImage=debug, nIter=0, highlightValue = [0,0,0])
                
                img0_255 = img_highlight[:,:,0]
                
                img = skimage.filters.rank.modal(img0_255, np.ones((3,3)))
                
                img = basic.imagelib.correctBorder(img, 'tr', trueValue = 255, 
                replaceValue = 0, showPlot = debug)
        
                dictDigitsImg = bt.digit.extr.isolateDigitTLBRprojectionInside(img, 
                showImage = debug)
        
                
                listImagesDictKeys = list(dictDigitsImg.keys())
                listImagesDictValues = list(dictDigitsImg.values())
                
                for coord, value in zip(listImagesDictKeys, listImagesDictValues):
                    # find local tl
                    ini = coord.index('[') + 1
                    fin = coord.index(']')
                    tmp = coord[ini:fin]
                    tl_local = np.array(list(tmp.split(", "))).astype(int)
                    
                    # find local br
                    coord = coord[coord.index('-'):]
                    ini = coord.index('[') + 1
                    fin = coord.index(']')
                    tmp = coord[ini:fin]
                    br_local = np.array(list(tmp.split(", "))).astype(int)
                    
                    tl_tot = tl+tl_local
                    br_tot = tl+br_local
                    
                    guess, _ = bt.digit.recClass.detectDigitClass(value, model)
                    # guess = 6
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
                            if key == ord('ù'):
                                counter = 0
                            cv2.destroyWindow(imgName)
                            continue
                    imgSaveName = "{:07d}".format(i)+str(tl_tot)+'-'+str(br_tot)+'.jpg'
                    cv2.imwrite(os.path.join(imageOutputDir, char, imgSaveName), value)
                    # print(os.path.join(imageOutputDir, char, imgSaveName))
                    
            except:
                print('error occurred in the loop')
                pass
    # Break the loop
        else:
            break

# When everything done, release
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()

print(basic.utils.count_files_in_dirs_inside_this_dir(imageOutputDir))




