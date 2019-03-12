# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
import cv2

from datasets_lib1 import \
Point, Rect, RectArray, Obj, Trans, Board, GetTransOpts
import datasets_func as func
from NameManager2 import NameManager2, GetNameOpts

img = Image.open('../data/ds_v2/timg.jpg')
img = img.resize((256, 256))
im = np.array(img)
immask = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) < 240

img2 = Image.open('../data/ds_v2/timg2.jpg')
img2 = img2.resize((256, 256))
im2 = np.array(img2)
immask2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY) < 200

img3 = Image.open('../data/ds_v2/timg3.jpg')
img3 = img3.resize((256, 256))
im3 = np.array(img3)
immask3 = cv2.cvtColor(im3, cv2.COLOR_BGR2GRAY) > 30

# 初始化 NameManager2
num = 20
name_opts = GetNameOpts()
name_opts['target'] = '../data/ds_v2/TEST4'
name_opts['sdir'] = ['show', 'show', 'show', 'show', 'show']
name_opts['suffix'] = ['A', 'B', 'gtAB_viz', 'C', 'gtBC_viz']
name_opts['ext'] = ['jpg', 'jpg', 'jpg', 'jpg', 'jpg']
nm = NameManager2(num, name_opts)

for i, name in enumerate(nm):
    # 随机obj1的初始位置及大小
    pos1 = func.RandomPoint([50, 50], [300, 300])
    size1 = im.shape[0:2] #！！！！！！！！！！！！！！！！这句的xy和ij反了
    # 初始化obj1
    obj1_rect = Rect(pos1, size1)
    obj1_data = RectArray(obj1_rect, 3)
    obj1_data.SetRectData(im)
    obj1_datamask = RectArray(obj1_rect, 1, dtype=np.bool)
    obj1_datamask.SetValue(immask)
    obj1 = Obj(obj1_data, obj1_datamask)

    # 初始化trans
    trans1_0 = Trans(obj1)
    trans_opts = GetTransOpts()
    trans_opts['xz_theta'] = func.RandomAngle(-np.pi/2, np.pi/2)
    trans_opts['py'] = func.RandomDis((-100, -100), (100, 100))
    trans1_0.QuickTrans(['py', 'xz'], trans_opts)
    # 另一种写法：
    # trans.GenTrans('py',trans_opts)
    # trans.GenTrans('xz',trans_opts)
    # trans.ImposeTrans()
    trans1_1 = Trans(trans1_0.obj_imB)
    trans_opts = GetTransOpts()
    trans_opts['xz_theta'] = func.RandomAngle(-np.pi/36, np.pi/36)
    trans_opts['py'] = func.RandomDis((-40, -40), (40, 40))
    trans1_1.QuickTrans(['py', 'xz'], trans_opts)


    ###############################################
    # 2222222222222222222222222222222
    # 随机obj1的初始位置及大小
    pos2 = func.RandomPoint([50, 50], [300, 300])
    size2 = im2.shape[0:2]
    # 初始化obj1
    obj2_rect = Rect(pos2, size2)
    obj2_data = RectArray(obj2_rect, 3)
    obj2_data.SetRectData(im2)
    obj2_datamask = RectArray(obj2_rect, 1, dtype=np.bool)
    obj2_datamask.SetValue(immask2)
    obj2 = Obj(obj2_data, obj2_datamask)

    trans2_0 = Trans(obj2)
    trans_opts = GetTransOpts()
    trans_opts['xz_theta'] = func.RandomAngle(-np.pi/2, np.pi/2)
    trans_opts['py'] = func.RandomDis((-100, -100), (100, 100))
    trans2_0.QuickTrans(['py', 'xz'], trans_opts)

    trans2_1 = Trans(trans2_0.obj_imB)
    trans_opts = GetTransOpts()
    trans_opts['xz_theta'] = func.RandomAngle(-np.pi/36, np.pi/36)
    trans_opts['py'] = func.RandomDis((-40, -40), (40, 40))
    trans2_1.QuickTrans(['py', 'xz'], trans_opts)


    ###############################################
    # 33333333333333333333
    # 随机obj1的初始位置及大小
    pos3 = func.RandomPoint([50, 50], [300, 300])
    size3 = im2.shape[0:2]
    # 初始化obj1
    obj3_rect = Rect(pos3, size3)
    obj3_data = RectArray(obj3_rect, 3)
    obj3_data.SetRectData(im3)
    obj3_datamask = RectArray(obj3_rect, 1, dtype=np.bool)
    obj3_datamask.SetValue(immask3)
    obj3 = Obj(obj3_data, obj3_datamask)

    trans3_0 = Trans(obj3)
    trans_opts = GetTransOpts()
    trans_opts['xz_theta'] = func.RandomAngle(-np.pi/2, np.pi/2)
    trans_opts['py'] = func.RandomDis((-100, -100), (100, 100))
    trans3_0.QuickTrans(['py', 'xz'], trans_opts)

    trans3_1 = Trans(trans3_0.obj_imB)
    trans_opts = GetTransOpts()
    trans_opts['xz_theta'] = func.RandomAngle(-np.pi/36, np.pi/36)
    trans_opts['py'] = func.RandomDis((-40, -40), (40, 40))
    trans3_1.QuickTrans(['py', 'xz'], trans_opts)

    mainboard1 = Board([640, 480])
    mainboard1.addTrans(trans1_1)
    mainboard1.addTrans(trans2_1)
    mainboard1.addTrans(trans3_1)
    mainboard1.Gen()
    mainboard1.Save(dict(zip(['imA', 'imB', 'flowAB_viz'],
                             name[0:3])))

#    mainboard2 = Board([640, 480])
#    mainboard2.addTrans(trans1_2)
#    mainboard2.Gen()
#    mainboard2.Save(dict(zip(['imB', 'flowAB_viz'],
#                             name[3:])))
    print(f'完成:{i}/{num}')
print('全部完成!')
