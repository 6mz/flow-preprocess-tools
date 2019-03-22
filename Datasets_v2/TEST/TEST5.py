# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
import cv2

from datasets_lib1 import \
    Point, Rect, RectArray, Obj, Trans, Board, GetTransOpts
import datasets_func as func
import datasets_func2 as func2
from datasets_material import RandomImg, GetRandomImgOpts
from VOC_lib import ListMannager
from NameManager2 import NameManager2, GetNameOpts


backgroundGenerator = RandomImg('bing')
materialGenerator = RandomImg('voc')

#img = Image.open('../data/ds_v2/timg.jpg')
#img = img.resize((256, 256))
#im = np.array(img)
#immask = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) < 240
#
#img2 = Image.open('../data/ds_v2/timg2.jpg')
#img2 = img2.resize((256, 256))
#im2 = np.array(img2)
#immask2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY) < 200
#
#img3 = Image.open('../data/ds_v2/timg3.jpg')
#img3 = img3.resize((256, 256))
#im3 = np.array(img3)
#immask3 = cv2.cvtColor(im3, cv2.COLOR_BGR2GRAY) > 30

# 设置参数
iter_num = 10
board_num = 2
obj_num = 5
board_size = [640, 480]

# 初始化 NameManager2
name_opts = GetNameOpts()
name_opts['target'] = '../data/ds_v2/TEST5'
name_opts['sdir'] = ['show', 'show', 'show', 'show', 'show', 'show', 'show']
name_opts['suffix'] = ['A', 'B', 'gtAB_viz', 'gtBA_viz', 'C', 'gtBC_viz', 'gtCB_viz']
name_opts['ext'] = ['jpg', 'jpg', 'jpg', 'jpg', 'jpg','jpg', 'jpg']
nm = NameManager2(iter_num, name_opts)


for i, name in enumerate(nm):
    # =============== 初始化区域 ==================
    # 背景
    # 初始化位置，大小
    pos0 = Point(0, 0)
    back_rect = Rect(pos0, board_size)
    back_data = RectArray(back_rect, 3)
    # 设置背景对象
    backgroud = backgroundGenerator.RandomGet()
    backgroud = backgroud.resize(board_size)
    back_data.SetRectData(np.array(backgroud))
    back_datamask = RectArray(back_rect, 1, dtype=np.bool)
    back_datamask.SetValue(True)
    obj_back = Obj(back_data, back_datamask)
    # 生成背景变换
    trans_back = Trans(obj_back)
    trans_back_opts = GetTransOpts()
    trans_back.QuickTrans('M', trans_back_opts)
    # 创建列表储存初始化的obj
    obj_list = [trans_back.obj_imB]  # 初始化obj列表
    # initboard 用于保存第一帧
    initboard = Board(board_size)
    initboard.addTrans(trans_back)
    # 初始化循环生成 obj
    for _ in range(obj_num):
        # 随机obj的初始位置及大小
        img,imgmask = materialGenerator.RandomGet()
        im = np.array(img)
        immask = np.array(imgmask) > 0
        pos = func2.RandomPoint([0, 0], board_size)
        size = (im.shape[1],im.shape[0])
        # 初始化obj
        obj_rect = Rect(pos, size)
        obj_data = RectArray(obj_rect, 3)
        obj_data.SetRectData(im)
        obj_datamask = RectArray(obj_rect, 1, dtype=np.bool)
        obj_datamask.SetValue(immask)
        obj = Obj(obj_data, obj_datamask)
        # 通过trans初始化obj的姿态，初始化不保存光流
        trans = Trans(obj)
        trans_opts = GetTransOpts()
        trans_opts['xz_theta'] = func.RandomAngle(-np.pi/2, np.pi/2)
        trans_opts['py'] = func.RandomDis((-100, -100), (100, 100))
        trans.QuickTrans(['py', 'xz'], trans_opts)
        # 更新board
        initboard.addTrans(trans)
        # 存入列表
        obj_list.append(trans.obj_imB)
    # 生成、保存
    initboard.Gen()
    name_front = 0
    initboard.Save({'imB': name[name_front]})
    name_front += 1

    # =============== 第一次生成区域 ==================
    # 生成背景
    obj_back = obj_list[0]
    trans_back = Trans(obj_back)
    trans_back_opts = GetTransOpts()
    # <这里插入对opts的修改>
    trans_back.QuickTrans('M', trans_back_opts)
    mainboard = Board(board_size)
    mainboard.addTrans(trans_back)
    # 保存修改
    obj_list[0] = trans_back.obj_imB
    trans_opts_list = [trans_back_opts]  # 初始化变换配置列表
    for j in range(1, obj_num+1):  # 有背景要加一
        obj = obj_list[j]
        # 继承初始化的对象
        trans = Trans(obj)
        trans_opts = GetTransOpts()
        # 首次生成用于生成光流的trans opts
        trans_opts['xz'] = func.RandomAngle(-np.pi/36, np.pi/36)
        trans_opts['py'] = func.RandomDis((-20, -20), (20, 20))
        trans.QuickTrans(['py', 'xz'], trans_opts)
        # 更新board
        mainboard.addTrans(trans)
        # 存入列表
        obj_list[j] = trans.obj_imB
        trans_opts_list.append(trans_opts)
    # 生成、保存
    mainboard.Gen()
    name_dict = dict(zip(['imB', 'flowAB_viz', 'flowBA_viz'],
                         name[name_front: name_front+3]))
    name_front += 3
    mainboard.Save(name_dict)

    # =============== 第一次以后的生成区域 ==================
    for _ in range(board_num - 1):
        # 生成背景
        obj_back = obj_list[0]
        trans_back_opts = trans_opts_list[0]
        trans_back = Trans(obj_back)
        # <这里插入对opts的修改>
        trans_back.QuickTrans('M', trans_back_opts)
        mainboard = Board(board_size)
        mainboard.addTrans(trans_back)
        # 保存修改
        obj_list[0] = trans_back.obj_imB
        trans_opts_list[0] = trans_back_opts
        for j in range(1, obj_num+1):  # 有背景要加一
            obj = obj_list[j]
            trans_opts = trans_opts_list[j]
            trans = Trans(obj)
            # 这里对opt里面的内容进行微调
            trans_opts['xz'] += func.NormalAngle(0, 1, 'd')
            trans_opts['py'] += func.NormalDis(0, 2)
            trans.QuickTrans(['py', 'xz'], trans_opts)
            # 更新board
            mainboard.addTrans(trans)
            # 存入列表
            obj_list[j] = trans.obj_imB
            trans_opts_list[j] = trans_opts
        # 生成、保存
        mainboard.Gen()
        name_dict = dict(zip(['imB', 'flowAB_viz', 'flowBA_viz'],
                             name[name_front: name_front+3]))
        name_front += 3
        mainboard.Save(name_dict)

    print(f'完成:{i}/{iter_num}')
print('全部完成!')
