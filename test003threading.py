# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 01:47:42 2022

@author: eferlius
"""
import threading
import time
import os
import basic.utils
# import everything from the preparation script
import AAApreliminary as config


#%% functions here
def fun1(maxValue):
    for i in range(maxValue):
        print(i)
        time.sleep(1)

def fun2(maxValue, char = 'a'):
    for i in range(maxValue):
        print(char)
        time.sleep(0.4)


maxValue = 10
x = threading.Thread(target=fun1, args = (maxValue,))
y = threading.Thread(target=fun2, args = (maxValue,'b'))

x.start()
y.start()


#%% plays sound while loop
basic.utils.playSound(duration = 2000)
for i in range(10):
    print(i)
    time.sleep(0.5)
#%% plays sound and then loop
basic.utils.playSound(waitExec = True)
for i in range(10):
    print(i)
    time.sleep(0.5)

#%% playVLC with return value
import basic.utils
audioDir = config.DICT['DIR']['audio DIR']
path = (os.path.join(audioDir,'tiStaShort.mp3'))
returnValue = basic.utils.playVLC(path, duration = -1, blockExec = False)
for i in range(10):
    print(i)
    time.sleep(0.5)

print(returnValue)
