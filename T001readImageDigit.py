# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 15:49:32 2022

@author: eferlius
"""
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import basic
# import everything from the preparation script
import AAApreliminary as config

IMG_PATH = r'G:\My Drive\python projects\bike tracker\Tests\20221214\03_analysis\images\tacx\0\0004590[177 350]-[207 397].jpg'
# load image
img = cv2.imread(IMG_PATH)

img = 255-img

basic.plots.pltsImg(img)
#%%
# lab
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
l,a,b = cv2.split(lab)

basic.plots.pltsImg([l,a,b])

# show
cv2.imshow("orig", img)

# closing operation
kernel = np.ones((2,2), np.uint8)

# threshold params
low = 100
high = 256
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
fig, ax = plt.subplots()
ax.imshow(thresh)
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
#%%
# from tensorflow.keras.datasets import mnist
# from tensorflow.keras.utils import to_categorical
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D
# from tensorflow.keras.layers import MaxPooling2D
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.layers import Flatten
# from tensorflow.keras.optimizers import SGD

# # load train and test dataset
# def load_dataset():
# 	# load dataset
# 	(trainX, trainY), (testX, testY) = mnist.load_data()
# 	# reshape dataset to have a single channel
# 	trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
# 	testX = testX.reshape((testX.shape[0], 28, 28, 1))
# 	# one hot encode target values
# 	trainY = to_categorical(trainY)
# 	testY = to_categorical(testY)
# 	return trainX, trainY, testX, testY

# # scale pixels
# def prep_pixels(train, test):
# 	# convert from integers to floats
# 	train_norm = train.astype('float32')
# 	test_norm = test.astype('float32')
# 	# normalize to range 0-1
# 	train_norm = train_norm / 255.0
# 	test_norm = test_norm / 255.0
# 	# return normalized images
# 	return train_norm, test_norm

# # define cnn model
# def define_model():
# 	model = Sequential()
# 	model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
# 	model.add(MaxPooling2D((2, 2)))
# 	model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
# 	model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
# 	model.add(MaxPooling2D((2, 2)))
# 	model.add(Flatten())
# 	model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
# 	model.add(Dense(10, activation='softmax'))
# 	# compile model
# 	opt = SGD(learning_rate=0.01, momentum=0.9)
# 	model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
# 	return model

# # run the test harness for evaluating a model
# def run_test_harness():
# 	# load dataset
# 	trainX, trainY, testX, testY = load_dataset()
# 	# prepare pixel data
# 	trainX, testX = prep_pixels(trainX, testX)
# 	# define model
# 	model = define_model()
# 	# fit model
# 	model.fit(trainX, trainY, epochs=10, batch_size=32, verbose=1)
# 	# save model
# 	model.save('final_model.h5')

# # entry point, run the test harness
# run_test_harness()
#%%
# make a prediction for a new image.
from numpy import argmax
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from keras.models import load_model

# model = load_model('final_model.h5')

# load and prepare the image
def load_image(filename):
	# load the image
	img = load_img(filename, color_mode = 'grayscale', target_size=(28, 28))
	# convert to array
	img = img_to_array(img)
	# reshape into a single sample with 1 channel
	img = img.reshape(1, 28, 28, 1)
	# prepare pixel data
	img = img.astype('float32')
	img = img / 255.0
	return img

# load an image and predict the class
def run_example(filename):
	# load the image
	img = load_image(filename)
	# load model
	model = load_model('final_model.h5')
	# predict the class
	predict_value = model.predict(img)
	digit = argmax(predict_value)
	print(digit)

# entry point, run the example
# run_example(os.path.join(IMG_DIR, '84garmin.jpg'))
