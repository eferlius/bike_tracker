# -*- coding: utf-8 -*-
import cv2
import numpy as np
from . import arrToTotal
import basic.imagelib as imagelib
#%% digit detection
class Segments:
    def __init__(self, minFill = 0.3, whRatioOne = 0.3, whRatioInvalid = 1):
        '''
        Create Segments for 7 segments display.

        Parameters
        ----------
        minFill : float [0..1]
            minimum percentage of pixels ON in the segment to consider the segment ON
        whRatioOne : float 
            if width/heigh < whRatioOne the number is automatically recognized as a 1
        whRatioInvalid : float
            if width/height > whRatioInvalid the image is automatically 
            considered invalid

        Returns
        -------
        None.

        '''
        # create a 7 seg model
        #   0
        # 3   5
        #   1
        # 4   6
        #   2

        # which segments are on
        self.flags = []
        # percentage of pixels that are ON for every segment
        self.filled = [0]*7

        self.minFill = minFill
        self.whRatioOne = whRatioOne
        self.whRatioInvalid = whRatioInvalid

        self.segments = []
        s0th = [[0.10, 0.90],  [0.00, 0.20]]  # 0 top horizontal
        s1mh = [[0.10, 0.90],  [0.40, 0.60]]  # 1 middle horizontal
        s2bh = [[0.10, 0.90],  [0.80, 1.00]]  # 2 bottom horizontal
        s3tl = [[0.00, 0.30],  [0.10, 0.45]]  # 3 top left
        s4bl = [[0.00, 0.30],  [0.55, 0.90]]  # 4 bottom left
        s5tr = [[0.70, 1.00],  [0.10, 0.45]]  # 5 top right
        s6br = [[0.70, 1.00],  [0.55, 0.90]]  # 6 bottom right
        self.segments.append(s0th)
        self.segments.append(s1mh)
        self.segments.append(s2bh)
        self.segments.append(s3tl)
        self.segments.append(s4bl)
        self.segments.append(s5tr)
        self.segments.append(s6br)

    # process an image and set flags
    def digest(self, img):
        # reset flags
        self.flags = []
        self.filled = [0]*7
        # check res to see if it's a one
        h, w = img.shape[:2]
        if w/h > self.whRatioInvalid:
            # set an invalid code: the two vertical left bands
            self.flags.append(3)
            self.flags.append(4)
            self.filled[3] = -1
            self.filled[4] = -1
        if w/h < self.whRatioOne:
            self.flags.append(5)
            self.flags.append(6)
            self.filled[5] = -1
            self.filled[6] = -1
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
            count = np.count_nonzero(img[yl:yh, xl:xh] == 255)
            if len(img.shape)>2:
                count /= img.shape[-1]
            self.filled[a] = count / (sh * sw)
            if count / (sh * sw) > self.minFill: # 0.5 is a sensitivity measure
                self.flags.append(a)

    def drawSegments(self, img):
        h, w = img.shape[:2]
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
            cv2.rectangle(img, (xl,yl),(xh,yh),(127,127,127),1)
        return img

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

def detectDigit7Segments(img, minFill = 0.3, whRatioOne = 0.3, 
                         whRatioInvalid = 1, showImage = False):
    #   0
    # 3   5
    #   1
    # 4   6
    #   2
    model = Segments(minFill, whRatioOne, whRatioInvalid)
    model.digest(img)
    fillingPercentage = model.filled
    number = model.getNum()
    # print(model.checkFilling(img))
    if showImage:
        img = model.drawSegments(img)
    else:
        img = None
    return number, fillingPercentage, img

def getValueOnDict7Segments(dictImages, minFill = 0.3, whRatioOne = 0.3, whRatioInvalid = 1, showImage = False, printFilling = False):
    if showImage:
        dictShow7Segm = {}

    # analyze each image in dictImages
    results = []
    for key, value in dictImages.items():
        if value is None:
            results.append(-1)
            if showImage:
                dictShow7Segm[key] = None
        else:
            try:
                number, filling, _ = detectDigit7Segments(value, minFill, whRatioOne, whRatioInvalid, False)
                results.append(number)
                if printFilling:
                    print(str(number) + ': ' + str(filling))
                if showImage:
                    dictShow7Segm[key] = detectDigit7Segments(value, minFill, whRatioOne, whRatioInvalid, True)[2]
            except:
                print('error occurred on getValueOnDict7Segments')

    total = arrToTotal.fromArrayOfDigitsToTotal(results)
    if showImage:
        imagelib.imagesDictInSubpplots(dictShow7Segm, nrows = 1, ncols = 3, sharex = False, sharey = False)
    return total
