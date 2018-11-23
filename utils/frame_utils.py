'''
用于读入各种类型的图像文件，如  jpeg、png、ppm、jpg以及bin、raw和flo

函数列表：
read_gen
'''

import numpy as np
from os.path import *
from scipy.misc import imread
from . import flow_utils 

def read_gen(file_name):
    # 分离后缀名
    ext = splitext(file_name)[-1]
    # 如果是普通文件
    if ext == '.png' or ext == '.jpeg' or ext == '.ppm' or ext == '.jpg':
        im = imread(file_name)
        # 如果三通道以上舍弃其余通道
        if im.shape[2] > 3:
            return im[:,:,:3]
        else:
            return im
    # 如果是二进制文件
    elif ext == '.bin' or ext == '.raw':
        return np.load(file_name)
    # 如果是光流文件
    elif ext == '.flo':
        return flow_utils.readFlow(file_name).astype(np.float32)
    return []
