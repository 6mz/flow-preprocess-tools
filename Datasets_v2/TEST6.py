import numpy as np
from PIL import Image

import datasets_func as func
import datasets_func2 as func2
from NameManager2 import NameManager2, GetNameOpts
from datasets_lib2 import MainBoard, DEFAULT_MAINBOARD_OPTS, TransOptsManager


if __name__ == '__main__':
    name_opts = GetNameOpts()
    iter_num = 1
    name_opts['operation'] = ['imB', 'imB', 'flowBA', 'flowBA_viz',
                              'imB', 'flowAB', 'flowAB_viz']
    name_opts['target'] = '../data/ds_v2/TEST6'
    name_opts['sdir'] = ['show', 'show', 'flow', 'show',
                         'show', 'flow', 'show']
    name_opts['suffix'] = ['A', 'B', 'gtBA', 'gtBA_viz',
                           'C', 'gtBC', 'gtBC_viz']
    name_opts['ext'] = ['png', 'png', 'flo', 'jpg',
                        'png', 'flo', 'jpg']
    nm = NameManager2(iter_num, name_opts)
    for i, name_dict in enumerate(nm):
        name = list(zip(*name_dict))[1]
        name_front = 0
        mainBoard = MainBoard(5)
        back_transOM = TransOptsManager()
        back_transOM.Set('M')
        fore_transOM = TransOptsManager()
        fore_transOM.Set('xz', func.RandomAngle, (-np.pi/2, np.pi/2))
        fore_transOM.Set('py', func.RandomDis, ((-100, -100), (100, 100)))
        mainBoard.SetTransOptsDict('back', back_transOM)
        mainBoard.SetTransOptsDict('fore', fore_transOM)
        nameDict = {'imB': name[name_front]}
        name_front += 1
        mainBoard.TransAllOnce(nameDict)

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
        nameDict = dict(zip(['imB', 'flowBA', 'flowBA_viz'],
                            name[name_front: name_front+3]))
        name_front += 3
        mainBoard.TransAllOnce(nameDict)

        back_transOM = mainBoard.GetTransOpts('back')
        back_transOM.SetMode('m')
        back_transOM.Set_('xz', func.NormalAngle, (0, 0.15, 'd'))
        back_transOM.Set_('py', func.NormalDis, (0, 1))
        back_transOM.Set_('sf', func.NormalScale, (0, 0.004))
        fore_transOM = mainBoard.GetTransOpts('fore')
        fore_transOM.SetMode('m')
        fore_transOM.Set('xz', func.NormalAngle, (0, 1, 'd'), mark='xz')
        fore_transOM.Set('py', func.NormalDis, (0, 2), mark='py')
        mainBoard.SetTransOptsDict('back', back_transOM)
        mainBoard.SetTransOptsDict('fore', fore_transOM)
        nameDict = dict(zip(['imB', 'flowAB', 'flowAB_viz'],
                            name[name_front: name_front+3]))
        name_front += 3
        mainBoard.TransAllOnce(nameDict)
        print(f'完成:{i+1}/{iter_num}')
    print('全部完成!')
