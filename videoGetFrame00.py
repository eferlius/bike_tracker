# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 13:48:49 2022

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
import basic.timer as basTim
# import everything from the preparation script
import AAApreliminary as config
#%% get frame

videoDirectory = config.DICT['DIR']['0_raw videos DIR']

videos = basic.utils.findFileInDirectory(videoDirectory,'')
frame = bt.imagelib.getFrameFromVideo(videos[-1], 3131, True, True)

#%% crop frame
# tl, br = bt.imagelib.getTLBR_user(frame)

# print('tl = ' + str(tl))
# print('br = ' + str(br))

tl = [152, 238]
br = [267, 298]

# crop frame
img = bt.imagelib.cropImageTLBR(frame, tl, br, True, True)

#%% denoinsing operations
timer = basTim.Timer()

# denoising
imgfilt = cv2.fastNlMeansDenoisingColored(img, None, h=10, hColor=10, templateWindowSize=7, searchWindowSize=21)
timer.lap(lap_name = 'fastDenoising')

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.imshow(img)
ax1.set_title('original')
ax2 = fig.add_subplot(212)
ax2.imshow(imgfilt)
ax2.set_title('filtered')

img = imgfilt

#%% digit extraction with kmeans
# when using kmeans, don't use denoising
timer.lap(printTime = False)
_ = bt.digit.extractDigitKmeans(img, 3, True)
_ = timer.lap(lap_name = 'kmeans orig')
# _ = bt.digit.extractDigitKmeans(imgfilt, True, k = 3)
# _ = timer.lap(lap_name = 'kmeans filt')

#%% digit extraction with channels
# check which transformations are better
imgDict = bt.imagelib.getImagesDictBasicTransform(imgfilt, showImage = True)

imgHSV2 = imgDict['HSV ch2']
imgLAB0 = imgDict['LAB ch0']
imgGRAY = imgDict['gray']
# use VLgray: V + L + gray: the most evident
imgDict['VLgray'] = np.nanmean((imgHSV2, imgLAB0, imgGRAY), axis = 0).astype(np.uint8)

bt.imagelib.imagesDictInSubpplots(imgDict)

# apply gaussian thresholding
imagesDictGaussian = {}
for key, value in imgDict.items():
    if key not in ['RGB', 'HSV', 'LAB']: # exlcude images with three channels
        imagesDictGaussian[key] = cv2.adaptiveThreshold(value, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,51,0)

bt.imagelib.imagesDictInSubpplots(imagesDictGaussian, ncols = 3, mainTitle = 'adaptive threshold')

# apply otsu thresholding
imagesDictOtsu = {}
for key, value in imgDict.items():
    if key not in ['RGB', 'HSV', 'LAB']: # exlcude images with three channels
        ret, imagesDictOtsu[key] = cv2.threshold(value,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

bt.imagelib.imagesDictInSubpplots(imagesDictOtsu, ncols = 3, mainTitle = 'otsu threshold')

#%%
imgKmeans = bt.digit.extractDigitKmeans(img, 3, True)

bt.imagelib.projection(imgKmeans, True)

detachImagesDict = bt.imagelib.cropImageNRegions(imgKmeans, nrows = 1, ncols = 3, showImage = True)


#%%
# # make a prediction for a new image.
# from numpy import argmax
# # from keras.preprocessing.image import load_img
# from tensorflow.keras.utils import load_img
# # from keras.preprocessing.image import img_to_array
# from tensorflow.keras.utils import img_to_array
# from keras.models import load_model

# tl, br = bt.imagelib.getTLBR_user(bestImage)
# # crop frame
# imageForPrediction = bt.imagelib.cropImage(bestImage, tl, br, True, True)

# model = load_model('final_model.h5')

# imageForPrediction = cv2.resize(imageForPrediction, (28,28)).astype(np.uint8)
# # imageForPrediction =  cv2.cvtColor(imageForPrediction, cv2.COLOR_RGB2GRAY)
# print(imageForPrediction.shape)

# bt.imagelib.plotImage(imageForPrediction)

# # convert to array
# imageForPrediction = img_to_array(imageForPrediction)
# # reshape into a single sample with 1 channel
# imageForPrediction = imageForPrediction.reshape(1, 28, 28, 1)
# # prepare pixel data
# imageForPrediction = imageForPrediction.astype('float32')

# # bt.imagelib.plotImage(imageForPrediction)

# # predict the class
# predict_value = model.predict(255-imageForPrediction)
# if  np.count_nonzero(predict_value>0) > 1:
#     digit = -1
# else:
#     digit = argmax(predict_value)
# print(digit)
