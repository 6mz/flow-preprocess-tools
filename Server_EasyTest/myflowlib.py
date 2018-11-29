# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import re
from PIL import Image
from scipy.misc import imsave,imread
from os.path import *


#%%========================================
def open_flo_file(filename):
    with open(filename, 'rb') as f:
        magic = np.fromfile(f, np.float32, count=1)
        if 202021.25 != magic:
            print('Magic number incorrect. Invalid .flo file')
        else:
            w = np.fromfile(f, np.int32, count=1)
        h = np.fromfile(f, np.int32, count=1)
        data = np.fromfile(f, np.float32, count=2*w[0]*h[0])
        # Reshape data into 3D array (columns, rows, bands)
        return np.resize(data, (h[0], w[0], 2))


def flow_read(filename):
    u,v = flow_read_(filename)
    return np.array([u,v])

def flow_read_(filename):
    """ Read optical flow from file, return (U,V) tuple. 
    
    Original code by Deqing Sun, adapted from Daniel Scharstein.
    """
    TAG_FLOAT = 202021.25
    f = open(filename,'rb')
    check = np.fromfile(f,dtype=np.float32,count=1)[0]
    assert check == TAG_FLOAT, ' flow_read:: Wrong tag in flow file (should be: {0}, is: {1}). Big-endian machine? '.format(TAG_FLOAT,check)
    width = np.fromfile(f,dtype=np.int32,count=1)[0]
    height = np.fromfile(f,dtype=np.int32,count=1)[0]
    size = width*height
    assert width > 0 and height > 0 and size > 1 and size < 100000000, ' flow_read:: Wrong input size (width = {0}, height = {1}).'.format(width,height)
    tmp = np.fromfile(f,dtype=np.float32,count=-1).reshape((height,width*2))
    u = tmp[:,np.arange(width)*2]
    v = tmp[:,np.arange(width)*2 + 1]
    return u,v


def readPFM(file):
    return readPFM_(file)[0][:,:,0:2] 

def readPFM_(file):
    file = open(file, 'rb')

    color = None
    width = None
    height = None
    scale = None
    endian = None

    header = file.readline().rstrip()
    if header.decode("ascii") == 'PF':
        color = True
    elif header.decode("ascii") == 'Pf':
        color = False
    else:
        raise Exception('Not a PFM file.')

    dim_match = re.match(r'^(\d+)\s(\d+)\s$', file.readline().decode("ascii"))
    if dim_match:
        width, height = list(map(int, dim_match.groups()))
    else:
        raise Exception('Malformed PFM header.')

    scale = float(file.readline().decode("ascii").rstrip())
    if scale < 0: # little-endian
        endian = '<'
        scale = -scale
    else:
        endian = '>' # big-endian

    data = np.fromfile(file, endian + 'f')
    shape = (height, width, 3) if color else (height, width)

    data = np.reshape(data, shape)
    data = np.flipud(data)
    return data, scale


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
        return open_flo_file(file_name)
    elif ext == '.pfm':
        return readPFM(file_name)
    return []


def flow_write(filename,uv,v=None):
    """ Write optical flow to file.
    
    If v is None, uv is assumed to contain both u and v channels,
    stacked in depth.
    Original code by Deqing Sun, adapted from Daniel Scharstein.
    """
    nBands = 2

    if v is None:
        assert(uv.ndim == 3)
        assert(uv.shape[2] == 2)
        u = uv[:,:,0]
        v = uv[:,:,1]
    else:
        u = uv

    assert(u.shape == v.shape)
    height,width = u.shape
    f = open(filename,'wb')
    TAG_CHAR = b'PIEH'
    f.write(TAG_CHAR)
    np.array(width).astype(np.int32).tofile(f)
    np.array(height).astype(np.int32).tofile(f)
    # arrange into matrix form
    tmp = np.zeros((height, width*nBands))
    tmp[:,np.arange(width)*2] = u
    tmp[:,np.arange(width)*2 + 1] = v
    tmp.astype(np.float32).tofile(f)
    f.close()

#%%====================================================================
def save_list(fname,listname):
    with open(fname,'w') as f:
        for line in listname:
            f.write(str(line)+'\n')

def save_3ziplist(fname,ziplist,title=''):
    with open(fname,'w') as f:
        f.write(title)
        for xi,y1i,y2i in ziplist:
            f.write('%.2f\t%.4f\t%.4f\n'% (xi,y1i,y2i))

def read_list(fname):
    with open(fname,'r') as f:
        lists = [line.strip() for line in f.readlines() if len(line.strip()) > 0]
    return lists


#%%====================================================================
def viz_flow_fromfile(flow,logscale=True,scaledown=6,output=False):
    return viz_flow_(flow[0,:,:],flow[1,:,:],logscale=logscale,scaledown=scaledown,output=output)

def viz_flow(flow,logscale=True,scaledown=6,output=False):
    return viz_flow_(flow[:,:,0],flow[:,:,1],logscale=logscale,scaledown=scaledown,output=output)

def viz_flow_(u,v,logscale=True,scaledown=6,output=False):
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


#%%============================================================
def abs_flow(flow,axis=2):
    return np.linalg.norm(flow,axis=axis)


def EPE(input_flow, target_flow ,axis=2):
    assert input_flow.shape==target_flow.shape
    return np.linalg.norm(target_flow-input_flow,axis=axis).mean()

def EPE_usingmask(input_flow, target_flow , mask):
    assert input_flow.shape==target_flow.shape
    assert input_flow.shape[0:2]==mask.shape
    input_flows=np.vstack((input_flow[:,:,0][mask],input_flow[:,:,1][mask]))
    target_flows=np.vstack((target_flow[:,:,0][mask],target_flow[:,:,1][mask]))
    return np.linalg.norm(input_flows-target_flows,axis=0).mean()


def Sparplot(netout_flow,uncertainty_flow,groundtruth_flow,steps=50,\
             is_plot=True,is_print=False,is_show=False,is_save=False,style=None,path='./'):

    gt=groundtruth_flow
    res=uncertainty_flow
    flow=netout_flow
    assert flow.shape==res.shape==gt.shape

    best=gt - flow

    total_steps=steps

    aepe0=EPE(flow,gt)
    print('AEPE:'+str(aepe0))
    
    totalpixels=int(flow.size/2)
    remainpixels=np.linspace(totalpixels,0,total_steps,endpoint=False,dtype='int')

    res=abs_flow(res)
    best=abs_flow(best)

    res_sort=res.flatten()
    best_sort=best.flatten()

    res_sort_index=np.argsort(res_sort)
    best_sort_index=np.argsort(best_sort)

    res_aepe=[]
    res_threshold=[]
    for p in remainpixels:
        threshold_id=res_sort_index[p-1]
        threshold=res_sort[threshold_id]
        aepe=EPE_usingmask(flow,gt,res<threshold)
        res_aepe.append(aepe)
        res_threshold.append(threshold)
        print( u"\r已完成 "+str(int(len(res_aepe)/steps*50))+'%',end = '')

    best_aepe=[]
    best_threshold=[]
    for p in remainpixels:
        threshold_id=best_sort_index[p-1]
        threshold=best_sort[threshold_id]
        aepe=EPE_usingmask(flow,gt,best<threshold)
        best_aepe.append(aepe)
        best_threshold.append(threshold)
        print( u"\r已完成"+str(int(len(best_aepe)/steps*50+50))+'%',end = '')

    x=(totalpixels-remainpixels)/totalpixels
    y1=res_aepe/aepe0
    y2=best_aepe/aepe0

    if(is_plot):
        plt.plot(x, y1, mec='r', mfc='w',label='Pred-Merged')
        plt.plot(x, y2, ms=10,label='Oracle')
        plt.legend()  # 让图例生效
        plt.margins(0)
        plt.xlabel('Fraction of Removed Pixels') #X轴标签
        plt.ylabel('Average EPE (Normalized)') #Y轴标签
        plt.title('Sparsification Plots') #标题
        if(is_save):
            print('\nsave fig')
            plt.savefig(path+'Sparsification Plots.png')
        plt.show()

    if(is_print):
        print('Removed\tPreAEPE\tOraAEPE')
        for xi,y1i,y2i in zip(x,y1,y2):
            print('%.2f'% xi,'\t%.4f'% y1i,'\t%.4f'% y2i)
 
    if(is_show or is_save):
        plt.imshow(res,cmap='gray')
        plt.xticks([])
        plt.yticks([])
        plt.axis('off')
        plt.show()
        plt.imshow(best,cmap='gray')
        plt.xticks([])
        plt.yticks([])
        plt.axis('off')
        plt.show()
        if(is_save):
            print('save 3 imgs !')
            if(style=='gray'):
                gt=abs_flow(gt)
                imsave('net_res_flow.jpg', res)
                imsave('best_res_flow.jpg', best)
                imsave('groundtruth_flow.jpg', gt)
            else:
                res=Image.fromarray(viz_flow(uncertainty_flow))
                best=Image.fromarray(viz_flow(netout_flow-gt))
                gt=Image.fromarray(viz_flow(gt))
                imsave(path+'net_res_flow.jpg', res)
                imsave(path+'best_res_flow.jpg', best)
                imsave(path+'groundtruth_flow.jpg', gt)

    return (remainpixels,res_aepe,best_aepe,aepe0)
