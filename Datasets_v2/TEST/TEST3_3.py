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

# 初始化 NameManager2
num = 10
name_opts = GetNameOpts()
name_opts['target'] = '../data/ds_v2/TEST3_3'
name_opts['sdir'] = ['show', 'show', 'flow', 'show', 'show', 'flow', 'show']
name_opts['suffix'] = ['A', 'B', 'gtAB', 'gtAB_viz', 'C', 'gtBC', 'gtBC_viz']
name_opts['ext'] = ['jpg', 'jpg', 'flo', 'jpg', 'jpg', 'flo', 'jpg']
nm = NameManager2(num, name_opts)

for i, name in enumerate(nm):
    # 随机obj1的初始位置及大小
    pos = func.RandomPoint([50, 50], [300, 300])
    size = im.shape[0:2]
    # 初始化obj1
    obj1_rect = Rect(pos, size)
    obj1_data = RectArray(obj1_rect, 3)
    obj1_data.SetRectData(im)
    obj1_datamask = RectArray(obj1_rect, 1, dtype=np.bool)
    obj1_datamask.SetValue(immask)
    obj1 = Obj(obj1_data, obj1_datamask)

    # 初始化trans
    trans = Trans(obj1)
    trans_opts = GetTransOpts()
    trans_opts['xz_theta'] = func.RandomAngle(-np.pi/2, np.pi/2)
    trans_opts['py'] = func.RandomDis((-100, -100), (100, 100))
    trans.QuickTrans(['py', 'xz'], trans_opts)
    # 另一种写法：
    # trans.GenTrans('py',trans_opts)
    # trans.GenTrans('xz',trans_opts)
    # trans.ImposeTrans()
    trans2 = Trans(trans.obj_imB)
    trans_opts = GetTransOpts()
    trans_opts['xz_theta'] = func.RandomAngle(-np.pi/36, np.pi/36)
    trans_opts['py'] = func.RandomDis((-40, -40), (40, 40))
    trans2.QuickTrans(['py', 'xz'], trans_opts)

    trans3 = Trans(trans2.obj_imB)
    trans_opts['xz_theta']
    trans_opts['py']
    trans3.QuickTrans(['py', 'xz'], trans_opts)

    mainboard1 = Board([640, 480])
    mainboard1.addTrans(trans2)
    mainboard1.Gen()
    mainboard1.Save(dict(zip(['imA', 'imB', 'flowAB', 'flowAB_viz'],
                             name[0:4])))

    mainboard2 = Board([640, 480])
    mainboard2.addTrans(trans3)
    mainboard2.Gen()
    mainboard2.Save(dict(zip(['imB', 'flowAB', 'flowAB_viz'],
                             name[4:])))
    print(f'完成:{i}/{num}')
print('全部完成!')
