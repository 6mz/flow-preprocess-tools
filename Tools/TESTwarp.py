# -*- coding: utf-8 -*-
import numpy as np
import sys
from PIL import Image

sys.path.append("../Server_EasyTest")
from myflowlib import read_gen,viz_flow

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

def budong(im,mask):
    warp2 = np.zeros((im.shape[0], im.shape[1], im.shape[2]))
    for c in range(im.shape[2]):
        warp2[:,:,c]=_budong(im[:,:,c],mask)
    return warp2.astype(np.uint8)

def _budong(im,mask):
    image_height = im.shape[0]
    image_width = im.shape[1]
    flow_height = image_height
    flow_width = image_width
    warp2 = np.zeros((image_height, image_width))
    for i in range(1,flow_height-1):
        for j in range(1,flow_width-1):
            if mask[i][j] == 1:
                a=[]
                a.append(im[i-1][j-1])
                a.append(im[i-1][j  ])
                a.append(im[i-1][j+1])
                a.append(im[i  ][j+1])
                a.append(im[i+1][j+1])
                a.append(im[i+1][j  ])
                a.append(im[i+1][j-1])
                a.append(im[i  ][j-1])
                b=np.array(a)
                if a:
                    warp2[i][j]=np.mean(b[np.nonzero(b)])
    return warp2+im

def WarpNotEasy(im,flow):
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
    absflow = np.sqrt(flow[:,:,0]**2+flow[:,:,1]**2)
    
    fx = np.minimum(np.maximum(fx, 0), flow_width-1)
    fy = np.minimum(np.maximum(fy, 0), flow_height-1)
    
    warp = np.zeros((image_height, image_width, im.shape[2]))
    
    fx=np.rint(fx)
    fy=np.rint(fy)
    fx=fx.astype(np.int)
    fy=fy.astype(np.int)
    fxy = fy*image_width+fx
    
    repeat = FindRepeat(fxy)
    for re in repeat:
        y = re // image_width
        x = re - y * image_width
        af = absflow[y,x]
        maxid = np.argmax(af)
        xmax = x[maxid]
        ymax = y[maxid]
        ix[y,x]=xmax
        iy[y,x]=ymax

    warp[fy,fx]=im[iy,ix]

    return warp.astype(np.uint8)

def FindRepeat(fxy):
    records_array = fxy.flatten()
    idx_sort = np.argsort(records_array)
    sorted_records_array = records_array[idx_sort]
    # 去除相同元素的数组，第一次出现的位置，出现次数
    vals, idx_start, count = np.unique(sorted_records_array, return_counts=True,return_index=True)
    # 按idx_start分割数组成多个数组
    res = np.split(idx_sort, idx_start[1:])
    vals = vals[count > 1]
    res = list(filter(lambda x: x.size > 1, res))
    return res


path= 'E:\\我的文档\\任务\\配准1\\测试图片\\展示在文档中的\\z1\\'
gt_name = 'z1f.flo'
res_name = 'z1res.flo'
A_name = 'z1A.jpg'
B_name = 'z1B.jpg'

gt_name = path + gt_name
A_name =  path + A_name
B_name =  path + B_name
res_name =  path + res_name

gt = read_gen(gt_name)
A = read_gen(A_name)
B = read_gen(B_name)
res = read_gen(res_name)
res = np.sqrt(res[:,:,0]*res[:,:,0]+res[:,:,1]*res[:,:,1])


#A_warp = warp(A,gt)
A_warp2 = WarpNotEasy(A,gt)
mask0 = res > 0.14*(np.max(res))
mask1 = np.sum(A_warp2,axis=2) == 0



#gtimg = Image.fromarray(viz_flow(gt))
#Aimg = Image.fromarray(A)
#Bimg = Image.fromarray(B)
#A_warpimg = Image.fromarray(A_warp)
#A_warp2img = Image.fromarray(A_warp2)
#A_warpimg.save(path+ 'z1A_forward.png')
#A_warp2img.save(path+'z1A_Nforward.png')
A_warp2M = budong(A_warp2,mask1)
mask1 = np.sum(A_warp2M,axis=2) == 0

mask = np.logical_or(mask0,mask1)
masks = np.array([mask,mask,mask]).transpose((1,2,0))

A_warp2M[masks] = B[masks]

A_warp2Mimg = Image.fromarray(A_warp2M)
A_warp2Mimg.save(path+'z1A_NMforward.png')

masks = masks.astype(np.uint8)*255
masksimg = Image.fromarray(masks)
masksimg.save(path+'z1res_masks.png')
##gtimg.show()
##Aimg.show()
##Bimg.show()
