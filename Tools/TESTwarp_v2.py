# -*- coding: utf-8 -*-
import numpy as np
import sys
import cv2
from PIL import Image

sys.path.append("../Server_EasyTest")
from myflowlib import read_gen,viz_flow
from yuyy_postprocess import warp_judge


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


def Warp_v3(im1,flow,im2):
    image_height = im1.shape[0]
    image_width = im1.shape[1]
    flow_height = flow.shape[0]
    flow_width = flow.shape[1]
    
    (iy, ix) = np.mgrid[0:image_height, 0:image_width]
    (fy, fx) = np.mgrid[0:flow_height, 0:flow_width]
    fx=np.float64(fx)
    fy=np.float64(fy)
    fx += flow[:,:,0]
    fy += flow[:,:,1]

    fx = np.minimum(np.maximum(fx, -1), flow_width)
    fy = np.minimum(np.maximum(fy, -1), flow_height)
    warp = np.zeros((image_height, image_width, im1.shape[2]),dtype=np.uint8)
    mask = np.zeros((image_height, image_width),dtype = np.bool)
    mask_flag = np.zeros((image_height, image_width),dtype = np.uint8)
    mask_o = np.zeros((image_height, image_width),dtype = np.uint8)

    fx=np.rint(fx)
    fy=np.rint(fy)
    fx=fx.astype(np.int)
    fy=fy.astype(np.int)
    count = 0
    for fi, fj, ii, jj in zip(fy.flat, fx.flat, iy.flat, ix.flat):
        if(-1 < fi < flow_height and 
           -1 < fj < flow_width):
            if not mask_flag[fi,fj]:
                mask_flag[fi, fj] += 1
                mask_o[ii,jj] += 1
                warp[fi,fj] = im1[ii,jj]
            else:
                mask_flag[fi, fj] += 1
                mask_o[ii,jj] += 1
                mask[fi, fj] = 1
                warp[fi,fj] = im1[ii,jj]
        else:
            count += 1
    print(count)


    maskimg = Image.fromarray(np.uint8(mask)*255)
    maskimg.save(path+'t12B_1_mask_重复.png')
    maskimg = Image.fromarray(np.uint8(mask_flag/np.max(mask_flag)*255))
    maskimg.save(path+'t12B_2_mask_数据.png')
    maskimg = Image.fromarray(np.uint8(mask_o/np.max(mask_o)*255))
    maskimg.save(path+'t12B_0_mask_原始数据引用.png')#取反是a->b消失部分
    mask_flag_bool = mask_flag.astype(np.bool)
    maskimg = Image.fromarray(np.uint8(mask_flag_bool)*255)
    maskimg.save(path+'t12B_3_mask_数据bool.png')


    mask_sj = mask_flag_bool.astype(np.uint8)
    mask = mask.astype(np.uint8)


    kernel3 = np.uint8(np.ones((4,4)))
    kernel_10zi = np.uint8([[0,1,0],[1,1,1],[0,1,0]])

#    mask_sj_pz = cv2.dilate(mask_sj, kernel3)
#    maskimg = Image.fromarray(np.uint8(mask_sj_pz)*255)
#    maskimg.save(path+'t12B_4_mask_数据_膨胀.png')
#    mask_sj_1_xf = mask_sj_pz - mask_sj
#    maskimg = Image.fromarray(np.uint8(mask_sj_1_xf)*255)
#    maskimg.save(path+'t12B_5_mask_1阶_细缝.png')
#
#    mask_flag_2 = mask_flag + np.uint8(mask_sj_1_xf)
#    maskimg = Image.fromarray(np.uint8(mask_flag_2/np.max(mask_flag_2)*255))
#    maskimg.save(path+'t12B_6_mask_数据填上_1阶细缝.png')
#
    mask_flag_pz = cv2.dilate(mask_flag, kernel3)
    maskimg = Image.fromarray(np.uint8(mask_flag_pz/np.max(mask_flag_pz)*255))
    maskimg.save(path+'t12B_7_mask_直接膨胀.png')
    mask_flag_pz_xf = mask_flag_pz - mask_flag
    maskimg = Image.fromarray(np.uint8(mask_flag_pz_xf*255))
    maskimg.save(path+'t12B_8_mask_直接膨胀_细缝.png')

#    mask_sj_bi = cv2.morphologyEx(mask_flag,cv2.MORPH_CLOSE,kernel3)
#    maskimg = Image.fromarray(np.uint8(mask_sj_bi/np.max(mask_sj_bi)*255))
#    maskimg.save(path+'t12B_9_mask_直接闭运算.png')
    mask_flag_blackhat =  cv2.morphologyEx(mask_flag, cv2.MORPH_BLACKHAT, kernel3)
    # black_hat(src(x,y))=close(src(x,y))−src(x,y)
    maskimg = Image.fromarray(np.uint8(mask_flag_blackhat*255))
    maskimg.save(path+'t12B_10_mask_直接黑帽运算（细缝）.png')

#    mask_flag_tophat =  cv2.morphologyEx(mask_flag, cv2.MORPH_TOPHAT, kernel3)
#    # top_hat(src(x,y))=src(x,y)−open(src(x,y))
#    maskimg = Image.fromarray(np.uint8(mask_flag_tophat*255))
#    maskimg.save(path+'t12B_11_mask_直接顶帽运算.png')

#    mask_flag_open = cv2.morphologyEx(mask_flag, cv2.MORPH_OPEN, kernel3)
#    mask_flag_open_blackhat = cv2.morphologyEx(mask_flag_open, cv2.MORPH_BLACKHAT, kernel3)
#    maskimg = Image.fromarray(np.uint8(mask_flag_open_blackhat*255))
#    maskimg.save(path+'t12B_12_mask_直接运算_先开运算_后黑帽运算.png')

#    mask_flag_open = cv2.morphologyEx(mask_flag, cv2.MORPH_OPEN, kernel3)
#    mask_flag_open_blackhat = cv2.morphologyEx(mask_flag_open, cv2.MORPH_BLACKHAT, kernel_10zi)
#    maskimg = Image.fromarray(np.uint8(mask_flag_open_blackhat*255))
#    maskimg.save(path+'t12B_13_mask_直接运算_先开运算_后黑帽运算_十字.png')

    nodata_mask = np.logical_or((~mask_flag_bool),mask_flag_blackhat)
    maskimg = Image.fromarray(np.uint8(nodata_mask*255))
    maskimg.save(path+'t12B_14_mask_无数据（缝+空）.png')

    maskimg = Image.fromarray(np.uint8((~mask_flag_bool))*255)
    maskimg.save(path+'t12B_15_mask_空.png')

    A_warpimg = Image.fromarray(warp)
    A_warpimg.save(path+'t12B_res_1_原始.png')
    repeat_mask = np.repeat(mask,3).reshape((image_height,image_width,3))
    res1 = warp * (1-repeat_mask)
    A_warpimg = Image.fromarray(res1)
    A_warpimg.save(path+'t12B_res_2_去掉重复区域.png')

#    res2 = res1 * (1-np.repeat(mask_sj_1_xf,3).reshape((image_height,image_width,3)))
#    A_warpimg = Image.fromarray(np.uint8(res2))
#    A_warpimg.save(path+'t12B_res_3_去掉重复区域和细缝.png')

    mask_flag_blackhat_bool = mask_flag_blackhat.astype(np.bool)
    xf_mask = np.repeat(mask_flag_blackhat_bool,3).reshape((image_height,image_width,3))
    res3 = res1 * (1-xf_mask)
    A_warpimg = Image.fromarray(np.uint8(res3))
    A_warpimg.save(path+'t12B_res_4_去掉重复区域和细缝.png')

    fin_mask = np.logical_or(mask,nodata_mask)
    maskimg = Image.fromarray(np.uint8(fin_mask*255))
    maskimg.save(path+'t12B_16_mask_最终B代替.png')
    fin_mask_ = np.repeat(fin_mask,3).reshape((image_height,image_width,3))


    res3_1 = res3 + im2 * fin_mask_
    A_warpimg = Image.fromarray(np.uint8(res3_1))
    A_warpimg.save(path+'t12B_res_5_去掉重复区域和细缝并用B补上.png')
    A_warpimg = Image.fromarray(np.uint8(im2 * fin_mask_))
    A_warpimg.save(path+'t12B_res_6_用B补上的重复区域和细缝.png')




    mask_flag_pz_xf_bool = mask_flag_pz_xf.astype(np.bool)
    xf_mask2 = np.repeat(mask_flag_pz_xf_bool,3).reshape((image_height,image_width,3))
    fin_mask2 = np.logical_or(np.logical_or(mask,~mask_flag_bool),mask_flag_pz_xf_bool)
    maskimg = Image.fromarray(np.uint8(fin_mask2*255))
    maskimg.save(path+'t12B_17_mask_最终B代替_2.png')
    fin_mask2_ = np.repeat(fin_mask2,3).reshape((image_height,image_width,3))
    res4 = res1*(1-xf_mask2) + im2 * fin_mask2_
    A_warpimg = Image.fromarray(np.uint8(res4))
    A_warpimg.save(path+'t12B_res_7_去掉重复区域和细缝并用B补上_2.png')
#    kernel = np.uint8(np.ones((4,4)))
#    kernel2 = np.uint8(np.ones((8,8)))
#    mask_flag = cv2.erode(mask_flag, kernel0)
#    mask_flag = cv2.dilate(mask_flag, kernel)
#    for i in range(3):
#        warp_ = warp[:,:,i]
#        warp_ = e
    return warp,mask



def rgb2hsv(RGB):
    r, g, b = RGB[0]/255.0, RGB[1]/255.0, RGB[2]/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    hsv = np.array([h, s, v])
    return hsv


if __name__ == '__main__':
    path= '../data/TEST datasetslib/testwarp/'
    gt_name = 't12gt.pfm'
    A_name = 't12A.png'
    B_name = 't12B.png'
    
    gt_name = path + gt_name
    A_name =  path + A_name
    B_name =  path + B_name
    
    gt = read_gen(gt_name)
    A = read_gen(A_name)
    B = read_gen(B_name)

    warp,mask = Warp_v3(A,gt,B)
    
#    A_warpimg = Image.fromarray(warp)
#    A_warpimg.save(path+'t12B_res.png')



