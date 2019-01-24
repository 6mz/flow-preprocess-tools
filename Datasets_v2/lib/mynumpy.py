# -*- coding: utf-8 -*-
"""
由于xy和ij坐标系不可协调的冲突创建这个文件
"""

import numpy as np

def zeros(size,dtype = np.float):
    return np.zeros((size[1],size[0]),dtype=dtype)

def ones(size,dtype = np.float):
    return np.zeros((size[1],size[0]),dtype=dtype)

def shape(numpyarray):
    s = numpyarray.shape
    return (s[1],s[0])