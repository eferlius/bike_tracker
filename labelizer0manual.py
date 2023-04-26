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
# import everything from the preparation script
import AAApreliminary as config
import skimage

#%% flags
TEST_DATE = '20221214'
TACX_GARMIN = 'tacx'
assert TACX_GARMIN in ['tacx', 'garmin']
debug = False
#%% build directories
videoInputDir = config.DICT['DIR']['02_preproc DIR'].replace('TEST_DATE', TEST_DATE)
files, dirs = basic.utils.find_files_and_dirs_in_dir(videoInputDir, printOutput = False)
video = files[-1]

imageOutputDir = config.DICT['DIR']['img DIR'].replace('TEST_DATE', TEST_DATE)
imageOutputDir = os.path.join(imageOutputDir, TACX_GARMIN)

#%% get frame
frame = basic.imagelib.getFrameFromVideo(video, 0, False, False)

videoName = os.path.split(video)[-1]

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

for i in tqdm(range(totalFrames)):
# for i in tqdm(range(1)):
# while(cap.isOpened()): 
# Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        try:
            # crop on roi
            img_rgb = basic.imagelib.cropImageTLBR(frame, tl, br, False)
    
            # k means for making the digits pop out
            # returns image with [0,0,0] and [255,255,255]
            img_highlight, segmentedImg = bt.digit.extractDigitKmeansLoop(img_rgb, 
            k=3, showImage=debug, nIter=0, highlightValue = [0,0,0])
            
            img0_255 = img_highlight[:,:,0]
            
            img = skimage.filters.rank.modal(img0_255, np.ones((3,3)))
            
            img = basic.imagelib.correctBorder(img, 'tr', trueValue = 255, 
            replaceValue = 0, showPlot = debug)
    
            dictDigitsImg = bt.digit.isolateDigitTLBRprojectionInside(img, 
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
                
                valueRescaled = basic.imagelib.rescaleToMaxPixel(value, 1000)
                while True:
                    imgName = 'press the corrispondent digit, [n] if no digit'
                    cv2.imshow(imgName, valueRescaled)
                    key = cv2.waitKey(0)
                    
                    if key in [ord(str(i)) for i in range(10)] or key == ord('n'): # enter key
                        char = chr(key)
                        # print(char +' pressed')
                        cv2.destroyWindow(imgName)
                        break
                    else:
                        cv2.destroyWindow(imgName)
                        continue
                imgSaveName = "{:07d}".format(i)+str(tl_tot)+'-'+str(br_tot)+'.jpg'
                cv2.imwrite(os.path.join(imageOutputDir, char, imgSaveName), value)
                
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




