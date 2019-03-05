# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
import cv2

from datasets_lib1 import \
Point, Rect, RectArray, Obj, Trans, Board, GetTransOpts
import datasets_func as func
from NameManager2 import NameManager2, GetNameOpts


img = Image.open('../data/ds_v1/timg.jpg')
img = img.resize((256, 256))
im = np.array(img)
immask = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)<240

# 初始化 NameManager2
num = 50
name_opts = GetNameOpts()
name_opts['target'] = '../data/ds_v2/TEST3'
name_opts['sdir'].append('vizflow')
name_opts['suffix'].append('gtAB_viz')
name_opts['ext'].append('jpg')
nm = NameManager2(num, name_opts)

for i, name in enumerate(nm):
    # 随机obj1的初始位置及大小
    pos = func.RandomPoint([0, 0], [200, 200])
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
    trans_opts['xz_theta'] = func.RandomAngle(np.pi/2)
    trans_opts['py'] = func.RandomDis((-100, -100), (100, 100))
    trans.QuickTrans(['py', 'xz'], trans_opts)
    # 另一种写法：
    # trans.GenTrans('py',trans_opts)
    # trans.GenTrans('xz',trans_opts)
    # trans.ImposeTrans()
    mainboard = Board([640, 480])
    mainboard.addTrans(trans)
    mainboard.Gen()
    mainboard.Save(dict(zip(['imA', 'imB', 'flowAB', 'flowAB_viz'],
                            name)))
    print(f'完成:{i}/{num}')
print('全部完成!')
