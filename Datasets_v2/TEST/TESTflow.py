# -*- coding: utf-8 -*-
import numpy as np
import sys
import cv2
from PIL import Image
sys.path.append("../../Server_EasyTest")
from myflowlib import read_gen,  viz_flow, WarpNotEasy, warp_easy
from yuyy_postprocess import warp_judge


if __name__ == '__main__':
    path = '../../data/ds_v2/TEST5_1/'
    gt_name = 'flow/2gtAB.flo'
    A_name = 'show/2A.png'
    B_name = 'show/2B.png'

    gt_name = path + gt_name
    A_name = path + A_name
    B_name = path + B_name

    gt = read_gen(gt_name)
    A = read_gen(A_name)
    B = read_gen(B_name)

    # warp,mask = warp_judge(A,gt,B)
    warp = WarpNotEasy(A, gt)
    A_warpimg = Image.fromarray(warp)
    A_warpimg.save(path+'show/2AF.jpg')


    gt_name = 'flow/2gtBA.flo'
    A_name = 'show/2B.png'
    B_name = 'show/2A.png'

    gt_name = path + gt_name
    A_name = path + A_name
    B_name = path + B_name

    gt = read_gen(gt_name)
    A = read_gen(A_name)
    B = read_gen(B_name)

    # warp,mask = warp_judge(A,gt,B)
    warp = WarpNotEasy(A, gt)
    A_warpimg = Image.fromarray(warp)
    A_warpimg.save(path+'show/2BB.jpg')