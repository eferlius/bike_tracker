# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 01:51:22 2023

@author: eferlius
"""
import numpy as np

LENGTH = 200
values = np.array([-1]*LENGTH)

#%% functions
def ask_value(i):
    done = False
    while not done:
        try:
            ans = int(input('insert value for {} element: '.format(i)))
            done = True
        except:
            print('not valid insert')
    return ans


STEP = 12


#%%
maxLen = len(values)
# get the first two values
start = 0
end = STEP
values[start] = ask_value(start)
values[end] = ask_value(end)

while len(np.where(values == -1)[0])>=0: 
    
    # index the values that are already recognized
    knownIndexes = np.where(values != -1)[0]
    # recognize the corresponding values
    knownValues = values[knownIndexes]
    
    # show them 
    for idx, val in zip(knownIndexes, knownValues):
        print('{:03d}: {:03d}'.format(idx, val))  
    print('-'*10)
        
    if len(np.where(values == -1)[0])==0:
        break
    
    # identify only the indexes that are not consecutive
    knownNotConsecIndexes = np.append(knownIndexes[np.where(np.diff(knownIndexes)>1)[0]],knownIndexes[-1])
    # the analysis should start from the first not consecutive index
    start = knownNotConsecIndexes[0]
    
    # if there is another index further on, it's necessary to know what there is in between
    if len(knownNotConsecIndexes)>1:
        end = knownNotConsecIndexes[1]
        # if the values are the same, in fill in between with the same value
        if values[start] == values[end]:
            values[start:end] = values[start]
        # if the values are different, ask for a value in the middle (to the user)
        else:
            i = min(start+int((end-start)/2), maxLen-1)  
            values[i] = ask_value(i)
            
    # if there isn't  another index, it's necessary to move forward 
    # of STEP elements and ask for the value (to the user)
    else:  
        i = min(start+STEP, maxLen-1) 
        values[i] = ask_value(i)
        
