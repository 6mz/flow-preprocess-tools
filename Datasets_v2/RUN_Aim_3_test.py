# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 17:16:59 2019

@author: Administrator
"""

import numpy as np

import datasets_func as func
import datasets_func2 as func2
from datasets_lib2 import MainBoard, GetMainBoardOpts, TransOptsManager
from datasets_lib3 import Aim_3
from datasets_material import GetRandomImgOpts

if __name__ == '__main__':
    iter_num = 2
    obj_num = 5
    path = '/4T_/flow/FlyingThings2D/version_3_test'
    voc_opt = GetRandomImgOpts('voc')
    voc_opt['level'] = {0: 0.08, 1: 0.12, 2: 0.25, 3: 0.25, 4: 0.2}
    mainboard_opts = GetMainBoardOpts()  # 详细信息见datasets_lib2
    mainboard_opts['board_size'] = [960, 540]
    mainboard_opts['background_name'] = ['sky', 'bing']
    mainboard_opts['background_iniMethod'] = 'slice_random'
    mainboard_opts['foreground_name'] = 'voc'
    mainboard_opts['foreground_RandomImg_opts'] = voc_opt
    aim_3 = Aim_3(  # 详细信息见 datasets_lib3
            iter_num, path, outitems=['im','flow','viz'], outdirform='together'
            )
    for i, nameDict_iter in enumerate(aim_3):
        mainBoard = MainBoard(obj_num, mainboard_opts)
        for j, nameDict in enumerate(nameDict_iter):
            if(j == 0):
#                back_transOM = TransOptsManager()
#                back_transOM.Set_('M')
                fore_transOM = TransOptsManager()
                fore_transOM.Set_('xz', func.RandomAngle, (-np.pi/2, np.pi/2))
                # 在添加附属参数的时候，需要使用mark指明绑定到哪个操作上
                fore_transOM.Set(
                        'xz_central', 'local', mark='xz')
                fore_transOM.Set_('sf', func.NormalScale, (1.3, 0.1))
#                mainBoard.SetTransOptsDict('back', back_transOM)
                mainBoard.SetTransOptsDict('fore', fore_transOM)
                mainBoard.TransAllOnce(nameDict)
            elif(j == 1):
                back_transOM = TransOptsManager()
                back_transOM.Set_('xz', func.RandomAngle, (-1.1, 1.1, 'd'))
                back_transOM.Set_('py', func.RandomDis, ((-10, -10), (10, 10)))
                back_transOM.Set_('sf', func.RandomScale,
                                  ((0.96, 0.96), (1.04, 1.04)))
                fore_transOM = TransOptsManager()
                # 这里以后要改成单个随机，参数一样，传入参数
                fore_transOM.Set_('xz', func.RandomAngle,
                                  (-np.pi/36, np.pi/36))
                fore_transOM.Set_('py', func.RandomDis,
                                  ((-60, -60), (60, 60)))
                fore_transOM.Set_('sf', func.RandomScale,
                                  ((0.925, 0.925), (1.075, 1.075)))
                mainBoard.SetTransOptsDict('back', back_transOM)
                mainBoard.SetTransOptsDict('fore', fore_transOM)
                mainBoard.TransAllOnce(nameDict)
            else:
                back_transOM = mainBoard.GetTransOpts('back')
                back_transOM.SetMode('mn')
                back_transOM.Set_('xz', func.NormalAngle, (0, 0.3, 'd'))
                back_transOM.Set_('py', func.NormalDis, (0, 2))
                back_transOM.Set_('sf', func.NormalScale, (0, 0.01))
                fore_transOM = TransOptsManager()
                fore_transOM.SetMode('mn')
                fore_transOM.Set_(
                        'xz', func.NormalAngle, (0, 1, 'd'))
                fore_transOM.Set_('py', func.NormalDis, (0, 4))
                mainBoard.SetTransOptsDict('back', back_transOM)
                mainBoard.SetTransOptsDict('fore', fore_transOM)
                mainBoard.TransAllOnce(nameDict)
        print(f'完成:{i+1}/{iter_num}')
    aim_3.SaveList()
    print('全部完成!')
