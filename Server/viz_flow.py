#! /usr/bin/env python

import numpy as np
from PIL import Image
   
    
def viz_flow(u,v,logscale=True,scaledown=6,output=False):
    """
    topleft is zero, u is horiz, v is vertical
    red is 3 o'clock, yellow is 6, light blue is 9, blue/purple is 12
    """
    colorwheel = makecolorwheel()
    ncols = colorwheel.shape[0]

    radius = np.sqrt(u**2 + v**2)
    if output:
        print("Maximum flow magnitude: %04f" % np.max(radius))
    if logscale:
        radius = np.log(radius + 1)
        if output:
            print("Maximum flow magnitude (after log): %0.4f" % np.max(radius))
    radius = radius / scaledown    
    if output:
        print("Maximum flow magnitude (after scaledown): %0.4f" % np.max(radius))
    rot = np.arctan2(-v, -u) / np.pi

    fk = (rot+1)/2 * (ncols-1)  # -1~1 maped to 0~ncols
    k0 = fk.astype(np.uint8)       # 0, 1, 2, ..., ncols

    k1 = k0+1
    k1[k1 == ncols] = 0

    f = fk - k0

    ncolors = colorwheel.shape[1]
    img = np.zeros(u.shape+(ncolors,))
    for i in range(ncolors):
        tmp = colorwheel[:,i]
        col0 = tmp[k0]
        col1 = tmp[k1]
        col = (1-f)*col0 + f*col1
       
        idx = radius <= 1
        # increase saturation with radius
        col[idx] = 1 - radius[idx]*(1-col[idx])
        # out of range    
        col[~idx] *= 0.75
        img[:,:,i] = np.floor(255*col).astype(np.uint8)
    
    return img.astype(np.uint8)
    
def threshBinary(im,thresh):
    table=[]
    for i in range(256):
        if i <thresh:
            table.append(0)
        else:
            table.append(1)
    bim=im.point(table,'1')
    return bim
    
def makecolorwheel():
    # Create a colorwheel for visualization
    RY = 15
    YG = 6
    GC = 4
    CB = 11
    BM = 13
    MR = 6
    
    ncols = RY + YG + GC + CB + BM + MR
    
    colorwheel = np.zeros((ncols,3))
    
    col = 0
    # RY
    colorwheel[0:RY,0] = 1
    colorwheel[0:RY,1] = np.arange(0,1,1./RY)
    col += RY
    
    # YG
    colorwheel[col:col+YG,0] = np.arange(1,0,-1./YG)
    colorwheel[col:col+YG,1] = 1
    col += YG
    
    # GC
    colorwheel[col:col+GC,1] = 1
    colorwheel[col:col+GC,2] = np.arange(0,1,1./GC)
    col += GC
    
    # CB
    colorwheel[col:col+CB,1] = np.arange(1,0,-1./CB)
    colorwheel[col:col+CB,2] = 1
    col += CB
    
    # BM
    colorwheel[col:col+BM,2] = 1
    colorwheel[col:col+BM,0] = np.arange(0,1,1./BM)
    col += BM
    
    # MR
    colorwheel[col:col+MR,2] = np.arange(1,0,-1./MR)
    colorwheel[col:col+MR,0] = 1

    return colorwheel  


def warp_easy(im, flow):
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

    warp = np.zeros((image_height, image_width, im.shape[2]))
    
    fx=np.rint(fx)
    fy=np.rint(fy)
    fx=fx.astype(np.int)
    fy=fy.astype(np.int)

    print('max flow:',np.max(np.max(flow[:,:,1])))
    print('min flow:',np.min(np.min(flow[:,:,1])))

    # print('max_ix:',np.max(np.max(ix)))
    # print('max_iy:',np.max(np.max(iy)))
    # print('max_fx:',np.max(np.max(fx)))
    # print('max_fy:',np.max(np.max(fy)))
    # print('min_fx:',np.min(np.min(fx)))
    # print('min_fy:',np.min(np.min(fy)))
    # print('ix_shape:',ix.shape)
    # print('iy.shape:',iy.shape)
    # print('fx_shape:',fx.shape)
    # print('fy_shape:',fy.shape)
    # print('flow[:,:,0]_shape:',flow[:,:,0].shape)
    # print('fx.dtype:',fx.dtype)
    warp[fy,fx]=im[iy,ix]
    # warp[iy,ix]=im[fy,fx]

    return warp.astype(np.uint8)