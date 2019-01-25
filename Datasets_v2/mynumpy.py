# -*- coding: utf-8 -*-
"""
由于xy和ij坐标系不可协调的冲突创建这个文件
"""

import numpy as np

def zeros2(size,dtype = np.float):
    return np.zeros((size[1],size[0]),dtype=dtype)

def zeros3(size,dim3 = 3,dtype = np.float):
    return np.zeros((size[1],size[0],dim3),dtype=dtype)

def ones2(size,dtype = np.float):
    return np.zeros((size[1],size[0]),dtype=dtype)

def shape(numpyarray):
    s = numpyarray.shape
    return (s[1],s[0])