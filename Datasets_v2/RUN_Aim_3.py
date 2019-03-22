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

if __name__ == '__main__':
    iter_num = 50
    mainboard_opts = GetMainBoardOpts()  # 详细信息见datasets_lib2
    mainboard_opts['background_name'] = 'sky'
    mainboard_opts['background_iniMethod'] = 'slice_random'
    aim_3 = Aim_3(  # 详细信息见 datasets_lib3
            iter_num, path='../data/ds_v2/TEST_Aim_3_1',
            outitems=['im', 'viz'], outdirform='together'
            )
    for i, nameDict_iter in enumerate(aim_3):
        mainBoard = MainBoard(5, mainboard_opts)
        for j, nameDict in enumerate(nameDict_iter):
            if(j == 0):
                back_transOM = TransOptsManager()
                back_transOM.Set('M')
                fore_transOM = TransOptsManager()
                fore_transOM.Set('xz', func.RandomAngle, (-np.pi/2, np.pi/2))
                mainBoard.SetTransOptsDict('back', back_transOM)
                mainBoard.SetTransOptsDict('fore', fore_transOM)
                mainBoard.TransAllOnce(nameDict)
            elif(j == 1):
                back_transOM = TransOptsManager()
                back_transOM.Set_('xz', func.RandomAngle, (-1, 1, 'd'))
                back_transOM.Set_('py', func.RandomDis, ((-5, -5), (5, 5)))
                back_transOM.Set_('sf', func.RandomScale,
                                  ((0.98, 0.98), (1.02, 1.02)))
                fore_transOM = TransOptsManager()
                # 这里以后要改成单个随机，参数一样，传入参数
                fore_transOM.Set('xz', func.RandomAngle,
                                 (-np.pi/36, np.pi/36), mark='xz')
                fore_transOM.Set('py', func.RandomDis,
                                 ((-20, -20), (20, 20)), mark='py')
                mainBoard.SetTransOptsDict('back', back_transOM)
                mainBoard.SetTransOptsDict('fore', fore_transOM)
                mainBoard.TransAllOnce(nameDict)
            else:
                back_transOM = mainBoard.GetTransOpts('back')
                back_transOM.SetMode('m')
                back_transOM.Set_('xz', func.NormalAngle, (0, 0.15, 'd'))
                back_transOM.Set_('py', func.NormalDis, (0, 1))
                back_transOM.Set_('sf', func.NormalScale, (0, 0.004))
                fore_transOM = mainBoard.GetTransOpts('fore')
                fore_transOM.SetMode('m')
                fore_transOM.Set(
                        'xz', func.NormalAngle, (0, 1, 'd'), mark='xz')
                fore_transOM.Set('py', func.NormalDis, (0, 2), mark='py')
                mainBoard.SetTransOptsDict('back', back_transOM)
                mainBoard.SetTransOptsDict('fore', fore_transOM)
                mainBoard.TransAllOnce(nameDict)
        print(f'完成:{i+1}/{iter_num}')
    aim_3.SaveList()
    print('全部完成!')
