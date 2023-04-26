# -*- coding: utf-8 -*-
"""
digit extraction on image
"""
import cv2
import numpy as np
import basic.imagelib as imagelib

#%% ROI recognition
# to be implemented

#%% highlight digits on image
def fromBGR_RGBtoVLGRAY(img, imgFormat = 'BGR'):
    # check image format
    validImgFormats = ['BGR', 'RGB']
    assert imgFormat in validImgFormats, \
    f"imgFormat not valid, possible values are: {validImgFormats}"
    if imgFormat == 'BGR':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # conversion
    imgHSV2 = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)[:,:,2]
    imgLAB0 = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)[:,:,0]
    imgGRAY = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # use VLgray: V + L + gray: the most evident
    imgVLGRAY = np.nanmean((imgHSV2, imgLAB0, imgGRAY), axis = 0).astype(np.uint8)
    return imgVLGRAY.astype(np.uint8)

def extractDigitGaussianThreshold(img, imgFormat = 'BGR', h = 10, templateWindowSize=7,
                                  blockSize = 21, searchWindowSize=21, C = 0, 
                                  showImage = False, filt = False):
    imgVLGRAY = fromBGR_RGBtoVLGRAY(img, imgFormat)
    # not sure if denoising is a good idea
    if filt:
        imgFilt = cv2.fastNlMeansDenoising(imgVLGRAY, None, h, templateWindowSize, 
                                           searchWindowSize)
        imgRec = imgFilt
    else:
        imgRec = imgVLGRAY
    imgGauss = cv2.adaptiveThreshold(imgRec, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY_INV, blockSize, C)
    imgGauss = imagelib.subValues(imgGauss, trueValueIni = 255, 
                                  trueValueFin = [255,255,255], 
                                  falseValueFin = [0,0,0])
    if showImage:
        imagelib.plotImage(imgGauss, title = 'digit extracted with gaussian thresholding')
        
    return imgGauss.astype(np.uint8)

def extractDigitOtsuThreshold(img, imgFormat = 'BGR', kSize = (5,5), 
                              sigmaX = 0, sigmaY = 0, 
                              showImage = False, blur = False):
    imgVLGRAY = fromBGR_RGBtoVLGRAY(img, imgFormat)
    # not sure if blurring is a good idea
    if blur:
        imgBlur = cv2.GaussianBlur(imgVLGRAY,kSize,sigmaX,sigmaY)
        imgRec = imgBlur
    else:
        imgRec = imgVLGRAY
    ret, imgOtsu = cv2.threshold(imgRec, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    imgOtsu = imagelib.subValues(imgOtsu, trueValueIni = 255, 
                                 trueValueFin = [255,255,255], 
                                 falseValueFin = [0,0,0])
    if showImage:
        imagelib.plotImage(imgOtsu, title = 'digit extracted with otsu thresholding')
    return imgOtsu.astype(np.uint8)

def extractDigitKmeans(img, k = 3, showImage = False, highlightValue = [0,0,0]):
    '''
    Divides the image in k clusters according to the features given and returns
    an image with values [255,255,255] for the pixel corresponding to the cluster
    that has minimum distance with highlightValue and [0,0,0] for the others

    The features might be for example the RGB triplet but it's also possible 
    to use more features.
    For example, 
    the following code adds a 2 to every pixel
    img = np.dstack((img, np.ones(img.shape[0:-1])*2))
    while this one adds also the gray encoding
    img = np.dstack((img, cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)))

    Parameters
    ----------
    img : TYPE
        DESCRIPTION.
    showImage : TYPE, optional
        DESCRIPTION. The default is False.
    convertBGR2RGB : TYPE, optional
        DESCRIPTION. The default is False.
    k : TYPE, optional
        DESCRIPTION. The default is 3.
        

    Returns
    -------
    darkestClusterImg: img
        img with [255,255,255] corresponding to the cluster closer to highlightValue
        and [0,0,0] elsewhere

    '''
    if len(img.shape) == 2:
        nFeatures = 1
    else:
        nFeatures = img.shape[-1]

    if nFeatures > 3 and showImage:
        raise Exception("can't display image if nFeatures > 3")

    # reshape the image to a 2D array of pixels and 3 color values (RGB)
    pixel_values = img.reshape((-1, nFeatures))
    # convert to float
    pixel_values = np.float32(pixel_values)
    # define stopping criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 20, cv2.KMEANS_RANDOM_CENTERS)
    # convert back to 8 bit values
    centers = np.uint8(centers)
    # flatten the labels array
    labels = labels.flatten()
    # convert all pixels to the color of the centroids
    segmentedImg = centers[labels]
    # reshape back to the original image dimension
    segmentedImg = segmentedImg.reshape(img.shape)
    
    
    highlightValue = np.array(highlightValue)
    norms = []
    for center in centers:
        norms.append(np.linalg.norm(center - highlightValue))
    
    # find the index of the closest center to highlightValue
    highlightIndex = np.argmin(norms)
    
    highlightImg = imagelib.subValues(segmentedImg, centers[highlightIndex], \
                                      [255]*nFeatures, [0]*nFeatures).astype(np.uint8)

    if showImage:
        imagelib.plotImage(segmentedImg, title = 'digit extracted with kmeans - {} clusters'.format(k))
        imagelib.plotImage(highlightImg, title = 'digit extracted with kmeans - highlighted cluster')

    return (highlightImg, segmentedImg)

def extractDigitKmeansLoop(img, k = 3, showImage = False, highlightValue = [0,0,0], nIter = 3):
    for i in range(nIter):
        # run kmeans
        imgKmeans, _ = extractDigitKmeans(img, k, showImage, highlightValue)
        # get top left and bottom right of highlighted parts
        tl, br = imagelib.getTLBRprojection(imgKmeans, 0, showImage)
        # crop image
        img = imagelib.cropImageTLBR(img, tl, br, showImage)

    imgKmeans, segmentedImg = extractDigitKmeans(img, k, showImage, highlightValue)
    return (imgKmeans, segmentedImg)


#%% isolate each digit and return the cropped images
def isolateDigit(img, nrows = 1, ncols = 3, thresholdPerc = 0.05, showImage = False):
    dictCropped = imagelib.cropImageNRegions(img, nrows, ncols)
    dictIsolated = {}
    for key, value in dictCropped.items():
            if np.max(value) > 0 and np.nanmean(value)/np.max(value) >= thresholdPerc:
                tl, br = imagelib.getTLBRprojection(value[:,:,0], 0, showImage)
                dictIsolated[key] = imagelib.cropImageTLBR(value, tl, br, False).astype(np.uint8)
            else:
                dictIsolated[key] = None
    if showImage:
       imagelib.imagesDictInSubpplots(dictIsolated, False, False, nrows, ncols, mainTitle = 'digits isolated')
    return dictIsolated

def isolateDigitTLBRprojectionInside(img, discValue = 0, maxIntervalsX = 3, maxIntervalsY = 1, showImage = False):
    tl_list, br_list = imagelib.getTLBRprojectionInside(img, discValue, showImage, 
                                                        maxIntH = maxIntervalsY,
                                                        maxIntV = maxIntervalsX)
    dictIsolated = {}
    for tl, br in zip(tl_list, br_list):
        thisImg = imagelib.cropImageTLBR(img, tl, br)
        tl_list_this, br_list_this = imagelib.getTLBRprojectionInside(thisImg, discValue, showImage, 
                                                            maxIntH = 1,
                                                            maxIntV = 1)
        
        for tl_this, br_this in zip(tl_list_this, br_list_this):
            tl_tot, br_tot = imagelib.sumTLBR([tl, br], [tl_this, br_this])
            thisImg_this = imagelib.cropImageTLBR(img, tl_tot, br_tot)
            dictIsolated[str(tl_tot)+'-'+str(br_tot)] = thisImg_this
            
    if showImage:
       imagelib.imagesDictInSubpplots(dictIsolated, sharex = False, sharey = False, 
       mainTitle = 'digits isolated with internal TLBR detection')
    return dictIsolated




