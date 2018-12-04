# -*- coding: utf-8 -*-
import numpy as np
import sys
from PIL import Image

sys.path.append("../Server_EasyTest")
from myflowlib import read_gen,viz_flow

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

    warp[fy,fx]=im[iy,ix]

    return warp.astype(np.uint8)

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


path= 'E:\\GitProgram\\preprocess-tools\\data\\TEST datasetslib\\'
gt_name = 't19f.flo'
A_name = 't19A.jpg'
B_name = 't19B.jpg'

gt_name = path + gt_name
A_name =  path + A_name
B_name =  path + B_name

gt = read_gen(gt_name)
A = read_gen(A_name)
B = read_gen(B_name)
A_warp = warp_easy(A,gt)
A_warp2 = WarpNotEasy(A,gt)


#gtimg = Image.fromarray(viz_flow(gt))
#Aimg = Image.fromarray(A)
#Bimg = Image.fromarray(B)
A_warpimg = Image.fromarray(A_warp)
A_warp2img = Image.fromarray(A_warp2)
A_warpimg.save(path+'t19A__oldwarp.jpg')
A_warp2img.save(path+'t19A_newwarp.jpg')
##gtimg.show()
##Aimg.show()
##Bimg.show()
