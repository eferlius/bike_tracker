# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 15:49:32 2022

@author: eferlius
"""
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import functions as f
# import everything from the preparation script
import AAApreliminary as config


IMG_DIR =  config.DICT['DIR']['images DIR']
IMG_PATH =  os.path.join(IMG_DIR, 'display.jpg')

img_orig = cv2.imread(IMG_PATH)

tl = [686, 348]
lr = [758, 388]

# tl = [500, 500]
# lr = [600, 530]

img = img_orig[tl[1]:lr[1], tl[0]:lr[0],:]

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


fig, ax = plt.subplots()
ax.imshow(cv2.cvtColor(img_orig, cv2.COLOR_BGR2RGB))
ax.set_title('original image [RGB format created for the plot]')

image = cv2.adaptiveThreshold(img_gray, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,15,20)

image = img_hsv[:,:,2]


fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax1.imshow(img)
ax2.imshow(image)
ax1.set_title('original image')
ax2.set_title('image used for computation')


rows, cols = f.projection(image)
# rows, cols = 256 - rows, 256 - cols

fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.plot(rows,np.arange(0,len(rows)),'.-')
ax1.set_ylim(ax1.get_ylim()[::-1])
ax2.plot(cols,'.-')
ax1.set_title('rows')
ax2.set_title('cols')
ax1.grid(True)
ax2.grid(True)
