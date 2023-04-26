# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 15:40:42 2022

@author: eferlius
"""

import basic as b
import basic.plots as bp
import numpy as np

x1 = np.arange(0,10,1)
y1 = np.arange(0,20,2)

x2 = np.arange(0,100,0.5)
y2 = np.arange(0,100,0.5)

# bp.drawInPlot([None,x2], [y1,y2])
fig, ax = bp.drawInPlot([x1],[y1], mainTitle = 'test')
ax.set_xlabel('time [s]')

fig, ax = bp.drawInSubPlots([x1, x2, [x1, x2]], [y1, y2, [y1, y2]], sharex = True, sharey = True, nrows = 2)
