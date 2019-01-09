# -*- coding: utf-8 -*-
import numpy as np
import sys
from PIL import Image

sys.path.append("../Server_EasyTest")
from myflowlib import read_gen,viz_flow


def Warp_v2(im1,im2,flow):
    image_height = im1.shape[0]
    image_width = im1.shape[1]
    flow_height = flow.shape[0]
    flow_width = flow.shape[1]
    
#    (iy, ix) = np.mgrid[0:image_height, 0:image_width]
    (fy, fx) = np.mgrid[0:flow_height, 0:flow_width]
    fx=np.float64(fx)
    fy=np.float64(fy)
    fx += flow[:,:,0]
    fy += flow[:,:,1]

    fx = np.minimum(np.maximum(fx, 0), flow_width-1)
    fy = np.minimum(np.maximum(fy, 0), flow_height-1)

    warp = np.zeros((image_height, image_width, im1.shape[2]),dtype=np.uint8)

    fx=np.rint(fx)
    fy=np.rint(fy)
    fx=fx.astype(np.int)
    fy=fy.astype(np.int)

    count = 0
    for y in range(image_height):
        for x in range(image_width):
            y_ = fy[y,x]
            x_ = fx[y,x]
            if (warp[y_,x_].any()):
                im2pix =  im2[y_ , x_]
                old = np.linalg.norm(im2pix - warp[y_,x_])
                new = np.linalg.norm(im2pix - im1[y,x])
                count += 1
                if(old > new):
                    warp[y_,x_] = im1[y,x]
                else:
                    None
            else:
                warp[y_,x_] = im1[y,x]

    print(count)
    return warp.astype(np.uint8)



path= '../data/TEST datasetslib/'
gt_name = 't12gt.pfm'
A_name = 't12A.png'
B_name = 't12B.png'

gt_name = path + gt_name
A_name =  path + A_name
B_name =  path + B_name

gt = read_gen(gt_name)
A = read_gen(A_name)
B = read_gen(B_name)

A_warp = Warp_v2(A,B,gt)

A_warpimg = Image.fromarray(A_warp)
A_warpimg.save(path+'t12B_2.png')



