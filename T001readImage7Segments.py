# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 15:49:32 2022

@author: eferlius
"""
import os
import cv2
import matplotlib.pyplot as plt
# import everything from the preparation script
import AAApreliminary as config




IMG_DIR =  config.DICT['DIR']['images DIR']
IMG_PATH =  os.path.join(IMG_DIR, 'display.jpg')

img = cv2.imread(IMG_PATH)

# fig, ax = plt.subplots()
# ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# ax.set_title('original image [RGB format created for the plot]')


# def onclick(event):
#    print([event.xdata, event.ydata])
# # Bind the button_press_event with the onclick() method
# fig.canvas.mpl_connect('button_press_event', onclick)

tl = [686, 348]
lr = [758, 388]



# fig, ax = plt.subplots()
# ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# ax.set_title('original image [RGB format created for the plot]')
# ax.set_xlim(tl[0], lr[0])
# ax.set_ylim(lr[1], tl[1])


import numpy as np

class Segments:
    def __init__(self):
        # create a 7seg model
        self.flags = []
        self.segments = []
        s0th = [[0, 1.0],    [0, 0.1]]    # 0 top horizontal
        s1mh = [[0, 1.0],    [0.45, 0.55]]# 1 middle horizontal
        s2bh = [[0, 1.0],    [0.9, 1.0]]  # 2 bottom horizontal
        s3tl = [[0, 0.2],   [0, 0.5]]     # 3 top left
        s4bl = [[0, 0.2],   [0.5, 1.0]]   # 4 bottom left
        s5tr = [[0.8, 1.0], [0, 0.5]]     # 5 top right
        s6br = [[0.8, 1.0], [0.5, 1.0]]   # 6 bottom right
        self.segments.append(s0th)
        self.segments.append(s1mh)
        self.segments.append(s2bh)
        self.segments.append(s3tl)
        self.segments.append(s4bl)
        self.segments.append(s5tr)
        self.segments.append(s6br)

    # process an image and set flags
    def digest(self, number):
        # reset flags
        self.flags = []

        # check res to see if it's a one
        h, w = number.shape[:2]
        if w < 0.5 * h:
            self.flags.append(5)
            self.flags.append(6)
            return

        # check for segments
        for a in range(len(self.segments)):
            seg = self.segments[a]
            # get bounds
            xl, xh = seg[0]
            yl, yh = seg[1]
            # convert to pix coords
            xl = int(xl * w)
            xh = int(xh * w)
            yl = int(yl * h)
            yh = int(yh * h)
            sw = xh - xl
            sh = yh - yl
            # check
            count = np.count_nonzero(number[yl:yh, xl:xh] == 255)
            if count / (sh * sw) > 0.5: # 0.5 is a sensitivity measure
                self.flags.append(a)

    # returns the stored number (stored in self.flags)
    def getNum(self):
        # hardcoding outputs
        if self.flags == [0,2,3,4,5,6]:
            return 0
        if self.flags == [5,6]:
            return 1
        if self.flags == [0,1,2,4,5]:
            return 2
        if self.flags == [0,1,2,5,6]:
            return 3
        if self.flags == [1,3,5,6]:
            return 4
        if self.flags == [0,1,2,3,6]:
            return 5
        if self.flags == [0,1,2,3,4,6]:
            return 6
        if self.flags == [0,5,6]:
            return 7
        if self.flags == [0,1,2,3,4,5,6]:
            return 8
        if self.flags == [0,1,2,3,5,6]:
            return 9
        # ERROR
        return -1


import cv2
import numpy as np
# from segments import Segments

# load image
img = cv2.imread(IMG_PATH)

# crop
img = img[tl[1]:lr[1], tl[0]:lr[0],:]

# lab
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
l,a,b = cv2.split(lab)

# show
cv2.imshow("orig", img)

# closing operation
kernel = np.ones((2,2), np.uint8)

# threshold params
low = 100
high = 150
iters = 3

# make copy
copy = l.copy()

# threshold
thresh = cv2.inRange(copy, low, high)

# dilate
for a in range(iters):
    thresh = cv2.dilate(thresh, kernel)

# erode
for a in range(iters):
    thresh = cv2.erode(thresh, kernel)

# show image
cv2.imshow("thresh", thresh)
cv2.imwrite("threshold.jpg", thresh)

# start processing
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# draw
for contour in contours:
    cv2.drawContours(img, [contour], 0, (0,255,0), 3)

# get res of each number
bounds = []
h, w = img.shape[:2]
for contour in contours:
    left = w
    right = 0
    top = h
    bottom = 0
    for point in contour:
        point = point[0]
        x, y = point
        if x < left:
            left = x
        if x > right:
            right = x
        if y < top:
            top = y
        if y > bottom:
            bottom = y
    tl = [left, top]
    br = [right, bottom]
    bounds.append([tl, br])

# crop out each number
cuts = []
number = 0
for bound in bounds:
    tl, br = bound
    cut_img = thresh[tl[1]:br[1], tl[0]:br[0]]
    cuts.append(cut_img)
    number += 1
    cv2.imshow(str(number), cut_img)

# font 
font = cv2.FONT_HERSHEY_SIMPLEX

# create a segment model
model = Segments()
index = 0
for cut in cuts:
    # save image
    # cv2.imwrite(str(index) + "_" + str(number) + ".jpg", cut)

    # process
    model.digest(cut)
    number = model.getNum()
    print(number)
    cv2.imshow(str(index), cut)

    # draw and save again
    h, w = cut.shape[:2]
    drawn = np.zeros((h, w, 3), np.uint8)
    drawn[:, :, 0] = cut
    drawn = cv2.putText(drawn, str(number), (10,30), font, 1, (0,0,255), 2, cv2.LINE_AA)
    cv2.imwrite("drawn" + str(index) + "_" + str(number) + ".jpg", drawn)
    
    index += 1
    # cv2.waitKey(0)


# show
cv2.imshow("contours", img)
# cv2.imwrite("contours.jpg", img)
cv2.waitKey(0)
