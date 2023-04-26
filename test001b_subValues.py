# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 00:57:03 2022

@author: eferlius
"""
import bikeTrackLib.imagelib as btil
import numpy as np
#%%
frame = np.array([[0,0],[0,1]])

ans = (btil.subValues(frame, trueValueIni = 1))
assert np.allclose(ans,np.array([[[0, 0], [0, 1]]])), f'fail'

frame = np.array([[[0,0,0],[0,1,0]],[[0,0,0],[0,1,1]]])

ans = (btil.subValues(frame, trueValueIni = [0,1,1]))
assert np.allclose(ans,np.array([[[0, 0], [0, 1]]])), f'fail'

ans = (btil.subValues(frame, trueValueIni = [0,1,1], trueValueFin = [1], falseValueFin = [0]))
assert np.allclose(ans,np.array([[[[0], [0]], [[0], [1]]]])), f'fail'

ans = btil.subValues(frame, trueValueIni = [0,1,1], trueValueFin = [1,1,1], falseValueFin = [0,0,0])
assert np.allclose(ans, np.array([[[0, 0, 0], [0, 0, 0]], [[0, 0, 0], [1, 1, 1]]])), f'fail'

ans = btil.subValues(frame, trueValueIni = [0,1,1], trueValueFin = [255,255,255], falseValueFin = [0,0,0])
assert np.allclose(ans, np.array([[[0, 0, 0], [0, 0, 0]], [[0, 0, 0], [255, 255, 255]]])), f'fail'

ans = btil.subValues(frame, trueValueIni = [0,0,0], trueValueFin = [255,255,255], falseValueFin = None)
assert np.allclose(ans, np.array([[[255, 255, 255], [0, 1, 0]], [[255, 255, 255], [0,1,1]]])), f'fail'


frame = np.array([[[0],[0]],[[0],[1]]])

ans = (btil.subValues(frame, trueValueIni = [1]))
assert np.allclose(ans,np.array([[[0, 0], [0, 1]]])), f'fail'

ans = (btil.subValues(frame, trueValueIni = [1], trueValueFin = 1))
assert np.allclose(ans,np.array([[[0, 0], [0, 1]]])), f'fail'

ans = (btil.subValues(frame, trueValueIni = [1], trueValueFin = [1], falseValueFin = [5]))
assert np.allclose(ans,np.array([[[5],[5]],[[5],[1]]])), f'fail'

ans = (btil.subValues(frame, trueValueIni = [1], trueValueFin = [1], falseValueFin = [0]))
assert np.allclose(ans,np.array([[[[0], [0]], [[0], [1]]]])), f'fail'

ans = btil.subValues(frame, trueValueIni = [1], trueValueFin = [1,1,1], falseValueFin = [0,0,0])
assert np.allclose(ans, np.array([[[0, 0, 0], [0, 0, 0]], [[0, 0, 0], [1, 1, 1]]])), f'fail'

ans = btil.subValues(frame, trueValueIni = [1], trueValueFin = [255,255,255], falseValueFin = [0,0,0])
assert np.allclose(ans, np.array([[[0, 0, 0], [0, 0, 0]], [[0, 0, 0], [255, 255, 255]]])), f'fail'

print('all tests passed!')

# # should raise exception
# ans = btil.subValues(frame, trueValueIni = [0], trueValueFin = [255,255,255], falseValueFin = None, depth = 3)
# assert np.allclose(ans, np.array([[[255, 255, 255], [0, 1, 0]], [[255, 255, 255], [0,1,1]]])), f'fail'
