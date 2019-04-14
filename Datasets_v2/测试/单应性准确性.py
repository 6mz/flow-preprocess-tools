# -*- coding: utf-8 -*-
import os
import numpy as np
import cv2

path = '../../data/ds_v2/TEST_homo/homo_data/version_homo2_10_6'
spath = '../../data/ds_v2/TEST_homo/6'

if not os.path.exists(spath):
    os.makedirs(spath)
    print(f'Create {spath}')

mpath = os.path.join(path, 'M')
impath = os.path.join(path, 'show')
ids = 0
for ids in range(0,10):
    imAname = os.path.join(impath, str(ids)+'A.png')
    imBname = os.path.join(impath, str(ids)+'B.png')
    Mname = os.path.join(mpath, str(ids)+'MAB.npy')
    M = np.load(Mname)
    imA = cv2.imread(imAname)
    imB = cv2.imread(imBname)
    h, w = imA.shape[0:2]
    imAwB = cv2.warpPerspective(imA, M, (w, h))  # (512, 384))
    cv2.imwrite(os.path.join(spath, str(ids)+'imA.png'), imA)
    cv2.imwrite(os.path.join(spath, str(ids)+'imB.png'), imB)
    cv2.imwrite(os.path.join(spath, str(ids)+'imAwB.png'), imAwB)
    np.savetxt(os.path.join(spath, str(ids)+'M.txt'),M)