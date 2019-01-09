# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from scipy.misc import imread, imsave
import matplotlib.pyplot as plt
from flowlib import flow_to_image
from IO import read

def open_flo_file(filename):
    with open(filename, 'rb') as f:
        magic = np.fromfile(f, np.float32, count=1)
        if 202021.25 != magic:
            print('Magic number incorrect. Invalid .flo file')
        else:
            w = np.fromfile(f, np.int32, count=1)
            h = np.fromfile(f, np.int32, count=1)
            data = np.fromfile(f, np.float32, count=2*w*h)
            # Reshape data into 3D array (columns, rows, bands)
            return np.resize(data, (h[0], w[0], 2))

def warp(im, flow):
    warp = np.zeros((im.shape[0], im.shape[1], im.shape[2]))
    for c in range(im.shape[2]):
        warp[:,:,c]=warp_(im[:,:,c],flow)
    return warp.astype(np.uint8)

def warp_(im, flow):   
    image_height = im.shape[0]
    image_width = im.shape[1]
    flow_height = flow.shape[0]
    flow_width = flow.shape[1]

    (iy, ix) = np.mgrid[0:image_height, 0:image_width]
    (fy, fx) = np.mgrid[0:flow_height, 0:flow_width]
    fx=np.float64(fx)
    fy=np.float64(fy)
    fx += flow[:,:,0]
    fy += flow[:,:,1]

    fx = np.minimum(np.maximum(fx, 0), flow_width-1)
    fy = np.minimum(np.maximum(fy, 0), flow_height-1)
    warp = np.zeros((image_height, image_width))
    
    fx=np.rint(fx)
    fy=np.rint(fy)
    fx=fx.astype(np.int)
    fy=fy.astype(np.int)
    warp[fy,fx]=im[iy,ix]

    warp2 = np.zeros((image_height, image_width))
    for i in range(1,flow_height-1):
        for j in range(1,flow_width-1):
            if warp[i][j]==0:
                a=[]
                a.append(warp[i-1][j-1])
                a.append(warp[i-1][j  ])
                a.append(warp[i-1][j+1])
                a.append(warp[i  ][j+1])
                a.append(warp[i+1][j+1])
                a.append(warp[i+1][j  ])
                a.append(warp[i+1][j-1])
                a.append(warp[i  ][j-1])
                b=np.array(a)
                if a:
                    warp2[i][j]=np.mean(b[np.nonzero(b)])
    return warp2+warp
