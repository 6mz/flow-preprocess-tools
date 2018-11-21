# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import re


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
    TAG_CHAR = 'PIEH'
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
             is_plot=True,is_print=False,is_show=False):
    gt=groundtruth_flow
    res=uncertainty_flow
    flow=netout_flow
    best=gt - flow
    
    total_steps=steps
    assert flow.shape==res.shape==gt.shape
    
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
        print('\r已完成'+str(int(len(res_aepe)/steps*50))+'%',end='')

    best_aepe=[]
    best_threshold=[]
    for p in remainpixels:
        threshold_id=best_sort_index[p-1]
        threshold=best_sort[threshold_id]
        aepe=EPE_usingmask(flow,gt,best<threshold)
        best_aepe.append(aepe)
        best_threshold.append(threshold)
        print('\r已完成'+str(int(len(best_aepe)/steps*50+50))+'%',end='')

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
        plt.show()

    if(is_print):
        print('Removed\tPreAEPE\tOraAEPE')
        for xi,y1i,y2i in zip(x,y1,y2):
            print('%.2f'% xi,'\t%.4f'% y1i,'\t%.4f'% y2i)
 
    if(is_show):
        plt.imshow(res,cmap='gray')
        plt.show()
        plt.imshow(best,cmap='gray')
        plt.show()

    return (remainpixels,res_aepe,best_aepe,aepe0)
