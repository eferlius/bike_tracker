# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 16:40:00 2023

@author: eferlius
"""
import basic.timer as bt
import matplotlib.pyplot as plt
import numpy as np
import csv
import time

def fix_step(start, stop, step):
    ''' returns step with the correct sign to go from start to stop'''
    return abs(step)*int((stop-start)/abs((stop-start)))
    
class Block:
    
    def __init__(self, duration, param):
        self.duration = duration
        self.param = param
    
class Training:
    
    def __init__(self, listOfBlocks = None):
        if listOfBlocks:
            self.listOfBlocks = listOfBlocks
            self.create()
        else: # use addBlock and create function 
            self.listOfBlocks = []
            pass
        
    def create(self):
        self.switch_times = []
        self.params = []
        start = 0
        for block in self.listOfBlocks:
            self.switch_times.extend([start])
            start+=block.duration
            self.params.extend([block.param]) 
        self.switch_times.extend([start])
        
        self.switch_times = np.array(self.switch_times)
        self.params = np.array(self.params)
        self.tot_duration = self.switch_times[-1]
        self.created = True
        
    def addBlock(self, duration, param):
        self.listOfBlocks.append(Block(duration, param)) 
        
    def addBlocksRamp(self, duration, start, stop, step):
        '''
        Creates a ramp with blocks of duration going in order:
            - start
            - start + step
            - start + 2*step
            ...
            - stop - step
            - stop     

        Parameters
        ----------
        duration : TYPE
            DESCRIPTION.
        start : TYPE
            DESCRIPTION.
        stop : TYPE
            DESCRIPTION.
        step : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        step = fix_step(start,stop,step)
        for value in np.arange(start, stop, step):
            self.listOfBlocks.append(Block(duration, value))
        if value != stop:
            self.listOfBlocks.append(Block(duration, stop))
            
    def addBlocksPyramids(self, duration, start, stop, step):
        step = fix_step(start,stop,step)
        self.addBlocksRamp(duration, start, stop,  step)
        self.addBlocksRamp(duration, stop-step, start, -step)
            
    def addBlocksRampUpDown(self, duration, start, stop, step):
        '''
        Creates a ramp with blocks of duration going in order:
            - start
            - start + step
            - start + step - step/2
            - start + 2*step
            - start + 2*step - step/2
            ...
            - stop - step/2
            - stop - step
            - stop        
            
        Parameters
        ----------
        duration : TYPE
            DESCRIPTION.
        start : TYPE
            DESCRIPTION.
        stop : TYPE
            DESCRIPTION.
        step : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        step = fix_step(start,stop,step)
        for value in np.arange(start, stop-step/2, step/2):
            if value == start:
                self.listOfBlocks.append(Block(duration, value))
            if value != start and value != stop:
                self.listOfBlocks.append(Block(duration, value+step/2))
                self.listOfBlocks.append(Block(duration, value))
        self.listOfBlocks.append(Block(duration, stop))
        
    def addBlocksPyramidsUpDown(self, duration, start, stop, step):
        step = fix_step(start,stop,step)
        self.addBlocksRampUpDown(duration, start, stop, step)
        self.addBlock(duration, stop-step)
        self.addBlocksRampUpDown(duration, stop-step/2, start, -step)
        
    def addBlocksInterval(self, n, int_duration, int_value, tot_duration, rest_value, startImmediately = False):
        rest_duration = tot_duration - int_duration
        if not startImmediately:
            self.listOfBlocks.append(Block(tot_duration, rest_value))
        for i in range(n):
            self.listOfBlocks.append(Block(int_duration, int_value))
            self.listOfBlocks.append(Block(rest_duration, rest_value))
                
    # def start(self):
    #     trainingTimer = bt.Timer.timer(self.listOfBlocks[0].duration)
        
    def plotTraining(self, ax = None):
        if ax:
            ax.stairs(self.params, np.array(self.switch_times)/60, fill = True)
        else:            
            plt.figure()
            plt.stairs(self.params, np.array(self.switch_times)/60, fill = True)
            plt.grid()
        
    # def showTraining(self):
    #     plt.ion()
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111)
    #     ax.stairs(self.params, np.array(self.switch_times)/60, fill = True)
    #     line1, = ax.plot([0,0],[0,np.max(self.params)])
    #     plt.grid()
    #     t = bt.Timer()
    #     print(self.tot_duration)
    #     while t.elap(printTime=False) < self.tot_duration:
    #         # param, elapsed_this_block, left_this_block, left_total, blockIndex = self.checkBlock(t.elap(printTime=False))
    #         line1.set_xdata([t.elap(printTime=False)/60]*2)
    #         fig.canvas.draw()
    #         fig.canvas.flush_events()
    #         time.sleep(0.2)
    #     plt.close('all')    
        
    def checkBlock(self, elapsedTime):
        '''
        Given the elapsed time, returns 
        param, elapsed_this_block, left_this_block, left_total, index

        Parameters
        ----------
        elapsedTime : TYPE
            DESCRIPTION.

        Returns
        -------
        param : TYPE
            DESCRIPTION.
        elapsed_this_block : TYPE
            DESCRIPTION.
        left_this_block : TYPE
            DESCRIPTION.
        left_total : TYPE
            DESCRIPTION.
        index : TYPE
            DESCRIPTION.

        '''
        index = np.where(self.switch_times<elapsedTime)[0][-1]
        if index < len(self.params):
            param = self.params[index]
            elapsed_this_block = elapsedTime-self.switch_times[index]
            left_this_block = self.switch_times[index+1] - elapsedTime
            left_total = self.switch_times[-1] - elapsedTime
        else:
            param, elapsed_this_block, left_this_block, left_total = 0,0,0,0
        return (param, elapsed_this_block, left_this_block, left_total, index)
    
    def to_csv(self, CSVfilePath):
        if not self.created:
            self.create
        
        rows = []
        rows.append(['start time [s]', 'param [ ]'])
        for p, st in zip(np.append(self.params,0), self.switch_times):
            #            np.append to get also the last switch times
            rows.append([st, p])
        
        f = open(CSVfilePath, mode = 'w', encoding='UTF8', newline='')
        writer = csv.writer(f)
        writer.writerows(rows)
        f.close()
        

        


        
