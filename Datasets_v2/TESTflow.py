# -*- coding: utf-8 -*-
import numpy as np
import sys
import cv2
from PIL import Image
sys.path.append("../Server_EasyTest")
from myflowlib import read_gen,  viz_flow, WarpNotEasy
from yuyy_postprocess import warp_judge


if __name__ == '__main__':
    path = '../data/ds_v1/t3/'
    gt_name = '1gt.flo'
    A_name = '1A.jpg'
    B_name = '1B.jpg'

    gt_name = path + gt_name
    A_name = path + A_name
    B_name = path + B_name

    gt = read_gen(gt_name)
    A = read_gen(A_name)
    B = read_gen(B_name)

    # warp,mask = warp_judge(A,gt,B)
    warp = WarpNotEasy(A, gt)
    A_warpimg = Image.fromarray(warp)
    A_warpimg.save(path+'1AF.jpg')
