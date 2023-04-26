# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 15:55:20 2023

@author: eferlius
"""

import os
import bikeTrackLib as bt
import pandas as pd
import basic
import numpy as np
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
import time
import datetime

# import everything from the preparation script
import AAApreliminary as config

TEST_DATE = '20230118'
TACX_GARMIN = 'tacx'
assert TACX_GARMIN in ['tacx', 'garmin']
MAX_TIME_CSV_SAVING = 180

#%% build directories
csvFileDir = config.DICT['DIR']['csv db DIR'].replace('TEST_DATE', TEST_DATE)
csvFilePath_nolab = os.path.join(csvFileDir, 'nolabels.csv')
csvFilePath_digits = os.path.join(csvFileDir, 'digits.csv')

featColNames = ['f{:03d}'.format(i) for i in range(28*28)]


df_nolab = pd.read_csv(csvFilePath_nolab)
df_digits = pd.read_csv(csvFilePath_digits)

df_digits_sorted = df_digits.sort_values('max predict')
df_digits_sorted.hist('max predict', bins = 1000)
basic.plots.plts([],df_digits_sorted['max predict'].values)


#%%
def ask_value_img(img, i, precValue):
    done = False
    while not done:
        
        img_rgb = cv2.merge([img*255]*3)
    
        valueRescaled = basic.imagelib.rescaleToMaxPixel(img_rgb, 1000)
    
        vrCopy = valueRescaled.copy()
    
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(vrCopy, ("{:03.0f}".format(precValue)), (0,int(vrCopy.shape[0]/2)), 
                    font, 5, (255,0,0), 10, cv2.LINE_AA)
        
        
        # user inserts value of the frame
        # - enter -> same value as before
        # - digits -> new value
        # - backspace -> show previous frame
        while True:
            done = False
            try:
                cv2.destroyWindow(imgName)
            except:
                pass
            imgName = 'frame {}'.format(i)
            cv2.imshow(imgName, vrCopy)
            
            key = cv2.waitKey(0)
            if key == ord('\r'): 
                # if enter, keep the same value as before
                done = True
                value = precValue
                cv2.destroyWindow(imgName)
                break
            elif key in [ord(str(_)) for _ in range(10)]:
                # if a value between 0 and 9 starts to read it from the keyboard
                digits = []
                while key != ord('\r'): # enter to finish
                    try:
                        digits.append(int(chr(key)))
                    except:
                        print('cannot convert character to int')
                    print('{}: {}'.format(i,digits))
                    key = cv2.waitKey(0)
                    
                    if key == ord('\b'):
                        print('backspace press, digits reset')
                        digits = []
                        key = ord('0')
                    
                value = 0
                for d,j in zip(digits,range(len(digits))):
                    value += d*10**(len(digits)-1-j) 
                print('{}: {}'.format(i,value))
                done = True
                cv2.destroyWindow(imgName)
                break
            elif key == ord('ù'):
                value = np.nan
                done = True
                cv2.destroyWindow(imgName)
                break
            # elif key == ord('\b'):
            #     i-=1
            #     cv2.destroyWindow(imgName)
            #     break
            else:
                cv2.destroyWindow(imgName)
                continue
        
    return value, i

#%%
csvTimer = basic.timer.Timer()


for i in df_digits_sorted.index.values:
    img = df_nolab.iloc[i].loc[featColNames].values.reshape(28,28).astype(np.uint8)
    digit = int(df_digits.iloc[i].loc['digit algo'])
    pred = df_digits.iloc[i].loc['max predict']
    
    if pred > 0.999:
    
        print("[{}]: {} ({})".format(i,digit, pred))
        
        
        value, _ = ask_value_img(img, i, digit)
        
        if value == 999:
            break
        
        idx = i
        df_digits['digit gt'][idx] = value
        
        if csvTimer.elap(printTime = False)>MAX_TIME_CSV_SAVING:
            csvTimer.reset()
            basic.sound.playBeep()
            print('saving csv...')
            thisMoment = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S')
            csvDigitsPath = os.path.join(csvFileDir, 'digits check until {}, {}.csv'.format(i,thisMoment))
            df_digits.to_csv(csvDigitsPath)
            print('saving complete')
        
print('saving csv...')
thisMoment = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S')
csvDigitsPath = os.path.join(csvFileDir, 'digits check until {}, {}.csv'.format(i,thisMoment))
df_digits.to_csv(csvDigitsPath)
print('saving complete')
    
    # plt.close('all')
    
#%%

    
    