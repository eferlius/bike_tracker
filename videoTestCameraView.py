# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:15:12 2022

@author: eferlius
"""

import cv2

capture = cv2.VideoCapture(0)
while (True):
    ret, frame = capture.read()
     
    if ret:
        cv2.imshow('video', frame)
    # press esc to exit
    if cv2.waitKey(1) == 27:
        break

capture.release()
cv2.destroyAllWindows()
