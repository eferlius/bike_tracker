# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 23:05:31 2023

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
from tqdm import tqdm

# import everything from the preparation script
import AAApreliminary as config

TEST_DATE = '20230105'
TACX_GARMIN = 'tacx'
assert TACX_GARMIN in ['tacx', 'garmin']
model = tf.keras.models.load_model('m_tacx-1.h5')
for TEST_DATE in tqdm(['20230105','20230109','20230111','20230116','20230117','20230118']):
    #%% build directories
    csvFileDir = config.DICT['DIR']['csv db DIR'].replace('TEST_DATE', TEST_DATE)
    csvFilePath_nolab = os.path.join(csvFileDir, 'nolabels.csv')
    csvFilePath_digits = os.path.join(csvFileDir, 'digits.csv')
    
    #%% load and clean csv file
    featColNames = ['f{:03d}'.format(i) for i in range(28*28)]
    df = pd.read_csv(csvFilePath_nolab)
    
    #%% make predictions
    testX = df.loc[:,featColNames].values
    testX = testX.reshape((testX.shape[0], 28, 28, 1))
    
    predict_value = model.predict(testX, verbose = 1)
    digit = np.argmax(predict_value, axis = 1)
    
    predict_value_original = predict_value.copy()
    
    #%% write outcomes on a new df
    df_digits = df[['frame','tl c0','tl c1','br c0','br c1']].copy()
    df_digits['digit algo'] = np.argmax(predict_value, axis = 1)
    df_digits['digit gt'] = np.argmax(predict_value, axis = 1)
    df_digits['check'] = np.zeros((df.shape[0],1))
    df_digits['max predict'] = np.max(predict_value, axis = 1)
    
    for i in range(predict_value.shape[1]):
        df_digits['pred{:02d}'.format(i)] = predict_value[:,i]
        
    
    df_digits.to_csv(csvFilePath_digits, index = False)