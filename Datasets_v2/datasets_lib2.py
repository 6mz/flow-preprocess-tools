# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
from itertools import count

from datasets_lib1 import \
    Point, Rect, RectArray, Obj, Trans, Board, GetTransOpts, GetTransInfo
import datasets_func as func
import datasets_func2 as func2
from datasets_material import RandomImg, GetRandomImgOpts
from VOC_lib import ListMannager



#         'iter_num': 10,
#        'board_num': 2,
#        'obj_num': 5,
DEFAULT_MAINBOARD_OPTS = {
        'board_size': [512, 384],
        'foreground_name': 'voc',
        'foreground_minIniPos': [0, 0],
        'foreground_maxIniPos': [480, 360],
        'background_name':'bing',
        'background_minIniPos': [-786, -308],
        'background_maxIniPos': [-100, -100],
        'background_size': [1366, 768],
        }


class TransOptsManager(object):
    '''
    Trans类参数的管理类
    用于管理单个obj(Trans) 生成单应性变换的 多次操作和参数
    本来按编程原则，应该独立生成M
    '''
    def __init__(self, id_=None):
        self.id = id_
        self.operates_dict = {}
        self.operates_data = {}
        self.c = count()
        self.mode = 'cover'
        #
        self.TRANS_TYPE = GetTransInfo()[0]
        self.TRANS_OPTSLIST = GetTransOpts().keys()

    def SetMode(self, mode='modify'):
        assert mode in ['cover', 'c', 'modify', 'm']
        if mode == 'c':
            mode = 'cover'
        if mode == 'm':
            mode = 'modify'
        self.mode = mode

    def Set_(self, *lists):
        self.Set(*lists, mark=lists[0])

    def Set(self, *lists, **dicts):
        if 'mark' in dicts:
            # 使用mark来标记操作的id，达到允许出现同类的操作的目的
            mark = dicts['mark']
        else:
            mark = next(self.c)
        if len(lists) == 1:
            self.SetValue(lists[0], mark=mark)
        elif len(lists) == 2:
            self.SetValue(lists[0], lists[1], mark=mark)
        elif len(lists) == 3:
            self.SetRandom(lists[0], lists[1], lists[2], mark=mark)
        else:
            print('WARRING: TransOptsManager.Set: Wrong number of parameters')

    def SetValue(self, item, value=None, mark=None):
        # 设置固定值
        if item in self.TRANS_OPTSLIST:
            # 添加变换
            if mark in self.operates_dict:
                self.operates_dict[mark][item] = ['const', value]
            else:
                assert item in self.TRANS_TYPE  # 保证创建新操作的时候item的合法性
                self.operates_data[mark] = [item, GetTransOpts()]
                self.operates_dict[mark] = {item: ['const', value]}
        else:
            print(f'WARRING: TransOptsManager.SetValue:' +
                  f'{item} is not in the TRANS_TYPE or TransOpts')

    def SetRandom(self, item, fun, parameter, mark=None):
        # 设置随机函数
        if item in self.TRANS_OPTSLIST:
            # 添加变换
            if mark in self.operates_dict:
                self.operates_dict[mark][item] = ['func', fun, parameter]
            else:
                assert item in self.TRANS_TYPE
                self.operates_data[mark] = [item, GetTransOpts()]
                self.operates_dict[mark] = {item: ['func', fun, parameter]}
        else:
            print(f'WARRING: TransOptsManager.SetRandom:' +
                  f'{item} is not in the TRANS_TYPE or TransOpts')

    def Modify(self, item, value, mark=None):
        # 修改固定值
        if item in self.TRANS_TYPE:
            assert self.operates_dict[mark][item][0] == 'const'  # 类型检查
            self.operates_dict[mark][item][1] += value
        else:
            print(f'WARRING: TransOptsManager.Modify:' +
                  f'{item} is not the key of opts')

    def Get(self):
        # 获取参数，随机函数在此时生效
        operates_dict = self.operates_dict
        operates = []
        operates_opts = []
        for mark in operates_dict:
            operate, trans_opts = self.operates_data[mark]
            if(self.mode == 'cover'):
                trans_opts = GetTransOpts()
            for item in operates_dict[mark]:
                sub_opt = operates_dict[mark][item]
                types = sub_opt[0]
                if types is 'const':
                    value = sub_opt[1]
                elif types is 'func':
                    fun = sub_opt[1]
                    parameter = sub_opt[2]
                    value = fun(*parameter)
                if value is not None:
                    if(self.mode == 'cover'):
                        trans_opts[item] = value
                    else:
                        trans_opts[item] += value
            operates.append(operate)
            operates_opts.append(trans_opts)
            self.operates_data[mark][1] = trans_opts
        return (operates, operates_opts)


class MainBoard(object):
    '''
    Board类的管理类
    辅助储存board的opts、obj、trans等属性，便于连续生成多幅图像
    '''
    def __init__(self, obj_num, mainboard_opts=DEFAULT_MAINBOARD_OPTS):
        self.obj_num = obj_num
        self.opts = mainboard_opts
        self.objDict = {}
        self.transOptsDict = {}
        # ======= func ========
        self.initBoard()
        self.initRandomImgGenerator()
        self.initBackground()
        for numid in range(obj_num):
            self.initForeground(numid+1)  # 0号编号属于背景,从1开始

    # ================  init  =========================
    def initBoard(self):
        board_size = self.opts['board_size']
        self.board = Board(board_size)

    def initRandomImgGenerator(self):
        back_name = self.opts['background_name']
        fore_name = self.opts['foreground_name']
        self.backgroundGenerator = RandomImg(back_name)
        self.foregroundGenerator = RandomImg(fore_name)

    def initBackground(self, numid=0):
        # 用于初始化背景对象
        # <这里在扩展以后需要更改,根据back_size生成back_minpos>
        back_minpos = self.opts['background_minIniPos']
        back_maxpos = self.opts['background_maxIniPos']
        back_size = self.opts['background_size']
        # </>
        # 设置背景的图片 及 图片的位置和大小
        pos0 = func2.RandomPoint(back_minpos, back_maxpos)
        back_rect = Rect(pos0, back_size)
        back_data = RectArray(back_rect, 3)
        backgroud = self.backgroundGenerator.RandomGet()
        backgroud = backgroud.resize(back_size)
        # 创建背景obj
        back_data.SetRectData(np.array(backgroud))
        back_datamask = RectArray(back_rect, 1, dtype=np.bool)
        back_datamask.SetValue(True)
        obj_back = Obj(back_data, back_datamask)
        self.objDict[numid] = obj_back

    def initForeground(self, numid):
        # 用于初始化前景对象
        froe_minpos = self.opts['foreground_minIniPos']
        froe_maxpos = self.opts['foreground_maxIniPos']
        # 读入前景
        img, imgmask = self.foregroundGenerator.RandomGet()
        # <更改前景大小加在这里></>
        im = np.array(img)
        immask = np.array(imgmask) > 0
        pos = func2.RandomPoint(froe_minpos, froe_maxpos)
        size = (im.shape[1], im.shape[0])
        froe_rect = Rect(pos, size)
        froe_data = RectArray(froe_rect, 3)
        froe_data.SetRectData(im)
        froe_datamask = RectArray(froe_rect, 1, dtype=np.bool)
        froe_datamask.SetValue(immask)
        obj_froe = Obj(froe_data, froe_datamask)
        self.objDict[numid] = obj_froe
    # ==========================================

    def SetTransOptsDict(self, id_, transOM):
        assert id_ in ['back', 'fore'] or id_ in self.objDict
        self.transOptsDict[id_] = transOM

    def GetTransOpts(self, id_):
        assert id_ in ['back', 'fore'] or id_ in self.objDict
        if id_ in self.objDict:  # 个人设置优先级高
            return self.transOptsDict[id_]
        elif id_ in ['back', 'fore']:
            return self.transOptsDict[id_]

    # ==========================
    def TransAllOnce(self, nameDict):
        # 产生一次图
        back_transOM = self.GetTransOpts('back')
        obj_back = self.objDict[0]
        self.objDict[0] = TransSingalOnce(obj_back, self.board, back_transOM)
        for i in range(self.obj_num):
            fore_transOM = self.GetTransOpts('fore')
            obj_fore = self.objDict[i+1]  # 0是背景
            obj_fore_ = TransSingalOnce(obj_fore, self.board, fore_transOM)
            self.objDict[i+1] = obj_fore_
        self.board.Gen()
        self.board.Save(nameDict)


def TransSingalOnce(obj, board, transOM):
    # 对一个obj变换一次
    assert isinstance(transOM, TransOptsManager)
    trans = Trans(obj)
    operates, operates_opts = transOM.Get()
    trans.QuickTrans(operates, operates_opts)  # 引用传参
    board.addTrans(trans)
    return trans.obj_imB


##########################################################
