# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 15:40:32 2022

@author: eferlius

configuration file containing costants and all the rest
"""
import os

#%% create empty dictionary to store all the variables
DICT = {}

#%% directories
DICT['DIR'] = {}
DICT['DIR']['new rec DIR'] = r'Tests\new recordings'
DICT['DIR']['test DIR'] = r'Tests\TEST_DATE'
DICT['DIR']['01_raw DIR'] = r'01_raw'
DICT['DIR']['02_preproc DIR'] = r'02_preprocessing'
DICT['DIR']['03_analysis DIR'] = r'03_analysis'
DICT['DIR']['img DIR'] = r'03_analysis\images'
DICT['DIR']['img tacx DIR'] = r'03_analysis\images\tacx'
DICT['DIR']['img garm DIR'] = r'03_analysis\images\garmin'
DICT['DIR']['csv dig extr DIR'] = r'03_analysis\digit extraction csv'
DICT['DIR']['csv db DIR'] =  r'03_analysis\csv database'
DICT['DIR']['digit extr DIR'] = r'03_analysis\digit extraction videos'

# join all directories with test directory
tmp = {}
for path in DICT['DIR']:
    if not 'test' in path and not 'new' in path:
        tmp[path] = os.path.join(DICT['DIR']['test DIR'], DICT['DIR'][path])
    else:
        tmp[path] = DICT['DIR'][path]
DICT['DIR'] = tmp

#%% automatically creating the absolute path for every path
# select where are all the files saved in (...)
DICT['DIR']['ABS DIR'] = os.path.split(os.getcwd())[0]

# make all the path absolutes
tmp = {}
for path in DICT['DIR']:
    if not 'ABS' in path:
        tmp[path] = os.path.join(DICT['DIR']['ABS DIR'], DICT['DIR'][path])
    else:
        tmp[path] = DICT['DIR'][path]
DICT['DIR'] = tmp
