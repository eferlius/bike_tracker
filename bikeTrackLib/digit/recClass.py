# -*- coding: utf-8 -*-
import numpy as np
import cv2
import tensorflow.keras.utils as tku
from . import arrToTotal

def loadImageToArr(filename, nrows = 28, ncols = 28):
    img = cv2.cvtColor(cv2.imread(filename),cv2.COLOR_BGR2GRAY)
    return fromImgToArr(img, nrows, ncols)

def fromImgToArr(img, nrows = 28, ncols = 28):
    img = cv2.resize(img.astype(float), (ncols, nrows))
    arr = np.asarray(img).reshape(1, ncols, nrows, 1).astype('float32')
    arr = np.where(arr>=np.max(arr)/2,1,0)
    return arr

def detDigFromArr(arr, model):
    predict_value = model.predict(arr, verbose = 0)
    digit = np.argmax(predict_value)
    return digit, predict_value
    
def detDigFromImg(img, model):
    arr = fromImgToArr(img)
    return detDigFromArr(arr, model)

def getValueOnDictClass(dictImages, model):
    # analyze each image in dictImages
    digits = []
    pred_values = []
    for key, value in dictImages.items():
        if value is None:
            digits.append(-1)
        else:
            try:
                digit, predict_value = detDigFromImg(value, model)
                digits.append(digit)
                pred_values.append(predict_value)
            except:
                print('error occurred on getValueOnDict7Segments')
    total = arrToTotal.fromArrayOfDigitsToTotal(digits) 
    pred_values.reverse()    
    return total,  pred_values

    
# predict_value = model.predict(img, verbose = 0)

if __name__ == '__main__':
    filename = r'G:\My Drive\python projects\bike tracker\Tests\20221214\03_analysis\images\tacx\5\0005004[180 349]-[203 396].jpg'
    img = tku.load_img(filename, color_mode = 'grayscale', target_size=(28, 28))
    
    img = cv2.cvtColor(cv2.imread(filename),cv2.COLOR_BGR2GRAY)
    tmp = fromImgToArr(img)


