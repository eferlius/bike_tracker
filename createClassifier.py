# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 10:00:59 2022

@author: eferlius
"""
import os
import bikeTrackLib as bt
import pandas as pd
import basic
import numpy as np

from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.optimizers import SGD

import tensorflow as tf
import keras
import sklearn

# import everything from the preparation script
import AAApreliminary as config
#%% flags
TEST_DATE = '20230104'
TACX_GARMIN = 'tacx'
assert TACX_GARMIN in ['tacx', 'garmin']
N = -1

#%% functions
# define cnn model
def define_model():
 	model = Sequential()
 	model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
 	model.add(MaxPooling2D((2, 2)))
 	model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
 	model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
 	model.add(MaxPooling2D((2, 2)))
 	model.add(Flatten())
 	model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
 	model.add(Dense(10, activation='softmax'))
 	# compile model
 	opt = SGD(learning_rate=0.01, momentum=0.9)
 	model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
 	return model

#%% build directories
csvFileDir = config.DICT['DIR']['csv db DIR'].replace('TEST_DATE', TEST_DATE)
csvFilePath = os.path.join(csvFileDir, 'until{num}.csv'.format(num=N))

# #%% load and clean csv file
# colNames = ['frame', 'digit']
featColNames = ['f{:03d}'.format(i) for i in range(28*28)]
# colNames.extend(featColNames)
# df = pd.read_csv(csvFilePath, header = None, names = colNames, dtype = {'label':'str'})
df = pd.read_csv(csvFilePath, dtype = {'digit':'int'})

print(df['digit'].value_counts())
nsamples = min(df['digit'].value_counts())

merged_df = pd.concat([df.query("digit == {}".format(i)).sample(n=nsamples) for i in range(10)])

print(merged_df['digit'].value_counts())


#%% TRAINING
trainX = merged_df.loc[:,featColNames].values
trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
trainY = np.squeeze(merged_df.loc[:, 'digit'].values)
trainY = trainY.reshape(trainY.shape[0])
'''
# trainY = np.where(trainY == '0', 0, trainY)
# trainY = np.where(trainY == '1', 1, trainY)
# trainY = np.where(trainY == '2', 2, trainY)
# trainY = np.where(trainY == '3', 3, trainY)
# trainY = np.where(trainY == '4', 4, trainY)
# trainY = np.where(trainY == '5', 5, trainY)
# trainY = np.where(trainY == '6', 6, trainY)
# trainY = np.where(trainY == '7', 7, trainY)
# trainY = np.where(trainY == '8', 8, trainY)
# trainY = np.where(trainY == '9', 9, trainY)
# trainY = np.where(trainY == 'N', 10, trainY)
'''
trainY = to_categorical(trainY)

# # define model
# model = define_model()
# # fit model
# model.fit(trainX, trainY, epochs=10, batch_size=32, verbose=1)
# # save model
# model.save('m_tacx{}.h5'.format(N))



#%% TEST

model = keras.models.load_model('m_tacx-1.h5')
testX = df.loc[:,featColNames].values
testX = testX.reshape((testX.shape[0], 28, 28, 1))
testY = np.squeeze(df.loc[:, 'digit'].values)
testY = testY.reshape(testY.shape[0])
y_true = testY
testY = to_categorical(testY)

predict_value = model.predict(testX, verbose = 1)
digit = np.argmax(predict_value, axis = 1)
#%%
import sklearn.metrics

# cm = tf.math.confusion_matrix(testYforCM, digit)
cm =  sklearn.metrics.confusion_matrix(y_true, digit, normalize = 'true')
disp = sklearn.metrics.ConfusionMatrixDisplay(cm)

disp.plot()

#%% CHECK SINGLE ELEMENT

wrongPredIndexes = np.where(y_true - digit != 0)[0]

index = wrongPredIndexes[0]
index = 42782
img = df.iloc[index].loc[featColNames].values.reshape(28,28)
trueLab = y_true[index]
predLab = digit[index]
frame = df.iloc[index].loc['frame']

basic.plots.pltsImg(img, mainTitle = 'frame {} {} predicted as {}'.format(frame, trueLab, predLab))
     
