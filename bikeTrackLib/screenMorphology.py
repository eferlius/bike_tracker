# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 23:05:34 2022

@author: eferlius
"""
import numpy as np
#%% create empty dictionary to store all the variables
DICT = {}
DICT['Tacx BASIC'] = {}
DICT['Tacx BASIC']['power'] = {}
DICT['Tacx BASIC']['power']['units'] = {}
DICT['Tacx BASIC']['power']['tens'] = {}
DICT['Tacx BASIC']['power']['hundreds'] = {}
DICT['Tacx BASIC']['elapsed time'] = {}


# respect to the square on the right corresponding to the screen and on the left
# on the left side of E of ETM
DICT['Tacx BASIC']['power']['tl down'] = 0.20
DICT['Tacx BASIC']['power']['tl right'] = 0.52
DICT['Tacx BASIC']['power']['br down'] = 0.80
DICT['Tacx BASIC']['power']['br right'] = 0.86

DICT['Tacx BASIC']['elapsed time']['tl down'] = 0
DICT['Tacx BASIC']['elapsed time']['tl right'] = 0
DICT['Tacx BASIC']['elapsed time']['br down'] = 0
DICT['Tacx BASIC']['elapsed time']['br right'] = 0

#%%
def getTLBR(tli, bri, device, measure):
    d = DICT[device][measure]
    tlf = []
    # tlf.append(int(np.floor(tli[0]+(-bri[0]+tli[0])*d['tl down'])))
    # tlf.append(int(np.floor(tli[1]+(-bri[1]+tli[1])*d['tl right'])))
    tlf.append(int(np.floor((bri[0]-tli[0])*d['tl down'])))
    tlf.append(int(np.floor((bri[1]-tli[1])*d['tl right'])))
    brf = []
    # brf.append(int(np.ceil(bri[0]+(-bri[0]+tli[0])*d['br down'])))
    # brf.append(int(np.ceil(bri[1]+(-bri[1]+tli[1])*d['br right'])))
    brf.append(int(np.ceil((bri[0]-tli[0])*d['br down'])))
    brf.append(int(np.ceil((bri[1]-tli[1])*d['br right'])))



    return tlf, brf
