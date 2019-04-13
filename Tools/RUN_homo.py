# -*- coding: utf-8 -*-
import cv2
import os
#import sys
import numpy as np
#sys.path.append("../Server_EasyTest")
#from myflowlib import read_gen,viz_flow


def GenFlowAB(M, wh):
    # 生成A->B变换对应的光流
    Awidth = wh[0]  # 宽度，列数
    Aheight = wh[1]
    r1 = range(0, Awidth)   # x
    r2 = range(0, Aheight)  # y
    xs, ys = np.meshgrid(r1, r2)  # 齐次坐标(x,y,z)
    zs = np.ones_like(xs)
    homoc = np.array([xs.flatten(), ys.flatten(), zs.flatten()])
    homoc = np.matmul(M, homoc)
    resx = (homoc[0, :]/homoc[2, :]).reshape(Aheight, Awidth) - xs
    resy = (homoc[1, :]/homoc[2, :]).reshape(Aheight, Awidth) - ys
    flow = np.array((resx, resy)).transpose((1, 2, 0))
    assert flow.shape == (Aheight, Awidth, 2)
    return flow


def homo(path, imgA, imgB, save_path):
    p_imA = os.path.join(path, imgA)
    s_imA = os.path.join(save_path, 'imgA.png')
    p_imB = os.path.join(path, imgB)
    s_imB = os.path.join(save_path, 'imgB.png')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f'Create {save_path}')
    imA = cv2.imread(p_imA)
    imB = cv2.imread(p_imB)
    
    surf = cv2.xfeatures2d.SURF_create(200)
    keypointA, descriptorA = surf.detectAndCompute(imA, None)
    keypointB, descriptorB = surf.detectAndCompute(imB, None)
    if descriptorA is None or descriptorB is None:
        print('!!')
        return
    bastMacher = cv2.FlannBasedMatcher_create()
    matches = bastMacher.match(descriptorA, descriptorB)
    matches.sort(key=lambda m: m.distance)
    if len(matches)>10:
        best = 10
    elif len(matches)>=4:
        best = len(matches)
    else:
        print('!!!')
        return
    print(f'len(goodmatch):{best}')
    goodmatch = matches[0:best]
    imagePointsA = np.array([keypointA[m.queryIdx].pt for m in goodmatch])
    imagePointsB = np.array([keypointB[m.trainIdx].pt for m in goodmatch])
    homo, mask = cv2.findHomography(imagePointsA, imagePointsB)
    matchesMask = mask.ravel().tolist()
    h, w = imA.shape[0:2]
    imAwB = cv2.warpPerspective(imA, homo, (w, h))  # (512, 384))
    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=None,
                       matchesMask=matchesMask,
                       flags=2)
    img3 = cv2.drawMatches(imA, keypointA,imB ,keypointB, goodmatch, None)
    cv2.imwrite(s_imA, imA)
    cv2.imwrite(s_imB, imB)
    cv2.imwrite(os.path.join(save_path, 'imAwB.png'), imAwB)
    cv2.imwrite(os.path.join(save_path, 'match.jpg'), img3)


path = '../data/Tools/TEST_EPE/5/'
imgA = '1A.jpg'
imgB = '1B.jpg'
save_path = path
homo(path, imgA, imgB, save_path)
path = '../data/Tools/TEST_EPE/5/'
imgA = '2A.jpg'
imgB = '2B.jpg'
save_path = path
homo(path, imgA, imgB, save_path)