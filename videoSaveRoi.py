# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 09:37:55 2023

@author: eferlius
"""
import basic
import os
# import everything from the preparation script
import AAApreliminary as config

ROI_NAMES = ['tacx power', 'garmin speed', 'garmin heart rate', 'garmin cadence']
TEST_DATE_LIST = ['20221204','20221205','20221209','20221212','20221214','20230102']

for TEST_DATE in TEST_DATE_LIST:
    print(TEST_DATE)
    videoInputDir = config.DICT['DIR']['02_preproc DIR'].replace('TEST_DATE', TEST_DATE)
    files, dirs = basic.utils.find_files_and_dirs_in_dir(videoInputDir, 
    listPartialName='',printOutput = False)
    video = files[-1]
    videoName = os.path.split(video)[-1]
    
    csvOutputDir = config.DICT['DIR']['csv dig extr DIR'].replace('TEST_DATE', TEST_DATE)
    os.makedirs(csvOutputDir, exist_ok = True)
    
    csv = os.path.join(csvOutputDir,videoName.replace('.avi','-roi location.csv'))
    basic.utils.write_row_csv(csv, ['roiName', 'tl[0]', 'tl[1]', 'br[0]', 'br[1]'], mode = 'a')
    
    frame = basic.imagelib.getFrameFromVideo(video, 0, False, False)
    
    done = False
    
    while not done:
        tl, br = basic.imagelib.getCoords_user(frame, nPoints = 3, title = 'Tacx BASIC - ')
        print('tl = ' + str(tl))
        print('br = ' + str(br))
        
        roiName = basic.utils.chose_option_list(ROI_NAMES)
        
        newRow = [roiName, tl[0], tl[1], br[0], br[1]]
        
        basic.utils.write_row_csv(csv, newRow)
        
        done = basic.utils.chose_option_list([True, False])
    
    


