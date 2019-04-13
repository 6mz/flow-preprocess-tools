# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
from itertools import count
from copy import deepcopy

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
        # ===============================
        # =====        前景          =====
        # ===============================
        'foreground_name': 'voc',
        'foreground_RandomImg_opts': None,  # None 表示自动根据foreground_name读取
        # 前景物体的初始位置，auto表示全画幅随机，define表示自定义随机位置的参数,也可以通过做变换来随机
        'foreground_iniPosMethod': 'auto',  # ['auto', 'define']
        # 前景物体初始位置的对齐点，central表示随机的是中心点，topleft表示左上角角点
        'foreground_iniPosStandard': 'central',  # ['central', 'topleft']
        # 如果 foreground_iniPos 设置为 define 则由以下两个参数决定
        'foreground_minIniPos': [0, 0],
        'foreground_maxIniPos': [480, 360],
        # 控制前景不要太大的临界值
        'foreground_size': [150, 100],
        # ===============================
        # =====        背景          =====
        # ===============================
        'background_name': 'bing',
        'background_RandomImg_opts': None,
        # 背景的初始化方法，有中间切片、随机切片、缩放、自定义
        'background_iniMethod': 'slice_random',
        # in ['slice_central', 'slice_random', 'zoom', 'define']
        # 是否检查背景图片的大小（一遍用于爬取的背景图，尺寸参差不齐）
        'background_check': 1,
        # 0： 所有不够安全尺寸的图进行缩放后通过
        # 1： 背景尺寸--安全尺寸 之间的图进行缩放后通过
        # 2： 小于安全尺寸的全部放弃]
        # 逻辑示意图：和原始图的大小比较（长宽都要符合）
        #               0          1          2
        # 尺寸小
        # 情形A        缩放切片    放弃重选     放弃重选
        # 临界尺寸: board（背景尺寸）
        # 情形B        缩放切片    缩放切片     放弃重选
        # 临界尺寸: target（安全尺寸）
        # 情形C        切片        切片        切片
        # 尺寸大
        # 安全系数，切片的大小 = safety_factor * board_size
        'background_safety_factor': 1.4,
        # 如果 background_iniFashion 设置为 define 则由以下三个个参数决定
        'background_minIniPos': [-786, -308],
        'background_maxIniPos': [-100, -100],
        'background_size': [1366, 768],
        }


# 读取DEFAULT_MAINBOARD_OPTS的副本
def GetMainBoardOpts():
    return deepcopy(DEFAULT_MAINBOARD_OPTS)


class TransOptsManager(object):
    '''
    Trans类参数的管理类
    用于管理单个obj(Trans) 生成单应性变换的 多次操作和参数
    本来按编程原则，应该独立生成M
    '''
    def __init__(self, id_=None):
        self.id = id_
        # 注意TransOptsManager只管理单个对象，但是可以被多个对象共用，且如果使用随机函数则
        # 每个对象的变换参数也会不同，但是他们来自于同一个形式的随机函数

        # 唯一的操作号：操作过程（可能包含函数，用于产生<操作结果>）
        self.operates_dict = {}
        self.operates_data = {}  # 唯一的操作号：操作结果（固定值，用于导入Trans）
        self.operates_mode = {}  # 见SetMode
        self.c = count()
        self.mode = 'cover'
        #
        self.TRANS_TYPE = GetTransInfo()[0]
        self.TRANS_OPTSLIST = GetTransOpts().keys()

    def SetMode(self, mode='modify'):
        assert mode in [
                'cover', 'c', 'modify1', 'm1', 'const', 'modifyn', 'mn']
        # 在下一次Get时，会有如下变化：
        # cover： 覆盖1次  modify1： 修改一次  modifyn: 一直修改直到被覆盖
        # const： 不变
        if mode == 'c':
            mode = 'cover'
        if mode == 'm1':
            mode = 'modify1'
        if mode == 'mn':
            mode = 'modifyn'
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
        # item 可以是操作（self.TRANS_TYPE），也可以是参数（self.TRANS_OPTSLIST）
        # 这里TRANS_TYPE是TRANS_OPTSLIST的子集，所以直接判断TRANS_OPTSLIST
        if item in self.TRANS_OPTSLIST:
            # 添加变换
            self.operates_mode[mark] = self.mode  # 给每个变换加单独的mode值
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
        self.operates_mode[mark] = self.mode  # 给每个变换加单独的mode值
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

#    def Modify(self, item, value, mark=None):
#        # 修改固定值
#        if item in self.TRANS_TYPE:
#            assert self.operates_dict[mark][item][0] == 'const'  # 类型检查
#            self.operates_dict[mark][item][1] += value
#        else:
#            print(f'WARRING: TransOptsManager.Modify:' +
#                  f'{item} is not the key of opts')

    def Get(self):
        # 获取参数，随机函数在此时生效
        operates_dict = self.operates_dict  # 获取值产生器
        operates_data = self.operates_data
        operates_mode = self.operates_mode
        operates = []
        operates_opts = []
        for mark in operates_dict:  # 对于对象的每个操作
            # 获得操作类型 和 参数
            mode = operates_mode[mark]
            operate, trans_opts = operates_data[mark]
            if(mode == 'cover'):  # 如果是覆盖模式,则重新生成新的 参数
                trans_opts = GetTransOpts()
            # 对于每一个变换操作做循环，大部分变换由于只有一个参数其实都只循环了一次
            for item in operates_dict[mark]:
                sub_opt = operates_dict[mark][item]
                types = sub_opt[0]  # 值产生器类型，固定值或函数
                if types is 'const':
                    value = sub_opt[1]
                elif types is 'func':
                    fun = sub_opt[1]
                    parameter = sub_opt[2]
                    value = fun(*parameter)
                if value is not None:  # 根据覆盖、调整、不变对原来的 参数 进行修改
                    if(mode == 'cover'):
                        trans_opts[item] = value
                        operates_mode[mark] = 'const'  # 下次就不变了
                    elif(mode == 'modify1'):
                        trans_opts[item] += value
                        operates_mode[mark] = 'const'  # 下次就不变了
                    elif(mode == 'modifyn'):
                        trans_opts[item] += value
                    else:
                        pass
            operates.append(operate)
            operates_opts.append(trans_opts)
            operates_data[mark][1] = trans_opts  # 引用赋值，改变了变量
        # print(operates_mode)
        return (operates, operates_opts)

    def Copyfrom(self, other):  # 《《《每次改动记得也来这里改一下哦》》》
        # 拷贝副本，但是保留本地的私人数据
        assert isinstance(other, TransOptsManager)
        # z = {**x, **y} y覆盖x
        self.operates_mode = deepcopy(
                {**self.operates_mode, **other.operates_mode})
        self.operates_dict = deepcopy(
                {**self.operates_dict, **other.operates_dict})
        self.operates_data = deepcopy(
                {**other.operates_data, **self.operates_data})
        self.c = other.c
        self.mode = other.mode


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
        self.transOptsDict_customize = {}  # 布尔值
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
        back_opts = self.opts['background_RandomImg_opts']
        fore_opts = self.opts['foreground_RandomImg_opts']
        # back
        if isinstance(back_name, str):
            if back_opts is None:
                back_opts = GetRandomImgOpts(back_name)
        elif isinstance(back_name, list):
            assert back_opts is None or len(back_opts) == len(back_name)
            if back_opts is None:
                back_name = np.random.choice(back_name)
                back_opts = GetRandomImgOpts(back_name)
            else:
                ids = np.random.randint(0, len(back_name))
                back_name = back_name[ids]
                if back_opts[ids] is None:
                    back_opts = GetRandomImgOpts(back_name)
                else:
                    back_opts = back_opts[ids]
        # fore
        if isinstance(fore_name, str):
            if fore_opts is None:
                fore_opts = GetRandomImgOpts(fore_name)
        elif isinstance(fore_name, list):
            assert fore_opts is None or len(fore_opts) == len(fore_name)
            if fore_opts is None:
                fore_name = np.random.choice(fore_name)
                fore_opts = GetRandomImgOpts(fore_name)
            else:
                ids = np.random.randint(0, len(fore_name))
                fore_name = fore_name[ids]
                if fore_opts[ids] is None:
                    fore_opts = GetRandomImgOpts(fore_name)
                else:
                    fore_opts = fore_opts[ids]
        # 赋值
        self.backgroundGenerator = RandomImg(back_name, back_opts)
        self.foregroundGenerator = RandomImg(fore_name, fore_opts)

    def initBackground(self, numid=0):
        # 用于初始化背景对象
        board_size = self.opts['board_size']
        background_iniMethod = self.opts['background_iniMethod']
        assert background_iniMethod in [
                'slice_central', 'slice_random', 'zoom', 'define']
        # 设置背景的图片 及 图片的位置和大小
        while(True):
            background = self.backgroundGenerator.RandomGet()  # 读取背景图
            assert background is not None
            if background_iniMethod == 'define':
                # <define 通过直接缩放后确定左上角位置，不进行切片，有待改进>
                back_minpos = self.opts['background_minIniPos']
                back_maxpos = self.opts['background_maxIniPos']
                back_size = self.opts['background_size']
                pos0 = func2.RandomPoint(back_minpos, back_maxpos)
                background = background.resize(back_size)
                break
            if background_iniMethod == 'slice_central':
                # 检查尺寸，进行缩放
                qx, raw_size, tag_size = self.initBackground_check(background)
                if qx == 'f':
                    continue
                elif qx == 's':
                    background = Zoom(background, raw_size, tag_size)
                new_size = np.array(background.size)
                if not (new_size >= tag_size).all():
                    continue  # 以防万一
                cen_pos = (new_size - tag_size)/2
                box = (cen_pos[0], cen_pos[1],
                       cen_pos[0] + tag_size[0],
                       cen_pos[1] + tag_size[1])
                background = background.crop(box)
                back_size = tag_size
                pos0 = Point((np.array(board_size) - tag_size)/2)
                break
            elif background_iniMethod == 'slice_random':
                # 几乎和slice_central一模一样
                qx, raw_size, tag_size = self.initBackground_check(background)
                if qx == 'f':
                    continue
                elif qx == 's':
                    background = Zoom(background, raw_size, tag_size)
                new_size = np.array(background.size)
                if not (new_size >= tag_size).all():
                    continue  # 以防万一
                ran_pos = func.RandomSize((0, 0), new_size-tag_size)
                box = (ran_pos[0], ran_pos[1],
                       ran_pos[0] + tag_size[0],
                       ran_pos[1] + tag_size[1])
                background = background.crop(box)
                back_size = tag_size
                pos0 = Point((np.array(board_size) - tag_size)/2)
                break
            elif background_iniMethod == 'zoom':
                qx, raw_size, tag_size = \
                    self.initBackground_check(background, 2)
                if qx == 'f':
                    continue
                # 几乎和slice_central一模一样，区别在于必定缩放
                background = Zoom(background, raw_size, tag_size)
                new_size = np.array(background.size)
                if not (new_size >= tag_size).all():
                    continue  # 以防万一
                box = (ran_pos[0], ran_pos[1],
                       ran_pos[0] + tag_size[0],
                       ran_pos[1] + tag_size[1])
                box = (ran_pos[0], ran_pos[1], tag_size[0], tag_size[1])
                background = background.crop(box)
                back_size = tag_size
                pos0 = Point((np.array(board_size) - tag_size)/2)
                break
        # 创建背景 Rect 和 RectArray
        back_rect = Rect(pos0, back_size)
        back_data = RectArray(back_rect, 3)
        # 创建背景obj
        back_data.SetRectData(np.array(background))
        back_datamask = RectArray(back_rect, 1, dtype=np.bool)
        back_datamask.SetValue(True)
        obj_back = Obj(back_data, back_datamask)
        self.objDict[numid] = obj_back
        self.transOptsDict[numid] = TransOptsManager()  # 私人变换数据
        self.transOptsDict_customize[numid] = False

    def initBackground_check(self, backgroud, check=None):
        check = self.opts['background_check'] if check is None else check
        board_size = np.array(self.opts['board_size'])
        safety_factor = self.opts['background_safety_factor']
        raw_back_size = np.array(backgroud.size, dtype=np.int)
        target_back_size = np.array(
                board_size*safety_factor, dtype=np.int)
        if (raw_back_size < board_size).all():
            qx = 's' if check == 0 else 'f'
        elif (raw_back_size < target_back_size).all():
            qx = 's' if check == 0 or check == 1 else 'f'
        else:
            qx = 'q'
        return (qx, raw_back_size, target_back_size)

    def initForeground(self, numid):
        # 用于初始化前景对象
        board_size = self.opts['board_size']
        froe_minpos = self.opts['foreground_minIniPos']
        froe_maxpos = self.opts['foreground_maxIniPos']
        foreground_iniPos = self.opts['foreground_iniPosMethod']
        assert foreground_iniPos in ['auto', 'define']
        foreground_iniPosStandard = self.opts['foreground_iniPosStandard']
        assert foreground_iniPosStandard in ['central', 'topleft']
        foreground_size = self.opts['foreground_size']
        # 读入前景
        img, imgmask = self.foregroundGenerator.RandomGet()
        froesize = np.array(img.size)  # (x,y)
        if (froesize > foreground_size).any():
            b = np.max(froesize / foreground_size)
            b = 1 if b < 1 else b  # 以防万一
            froesize = np.array(
                    froesize/(1+(b-1)*np.random.uniform(0, 1)), dtype=np.int)
            img = img.resize(froesize)
            imgmask = imgmask.resize(froesize)
        im = np.array(img)
        immask = np.array(imgmask) > 0
        if foreground_iniPos == 'auto':
            pos = func2.RandomPoint((0, 0), board_size)
        elif foreground_iniPos == 'define':
            pos = func2.RandomPoint(froe_minpos, froe_maxpos)
        if foreground_iniPosStandard == 'central':
            # print(pos)
            pos = pos - froesize/2
        elif foreground_iniPosStandard == 'topleft':
            pass
        froe_rect = Rect(pos, froesize)
        # print(froe_rect)
        froe_data = RectArray(froe_rect, 3)
        froe_data.SetRectData(im)
        froe_datamask = RectArray(froe_rect, 1, dtype=np.bool)
        froe_datamask.SetValue(immask)
        obj_froe = Obj(froe_data, froe_datamask)
        self.objDict[numid] = obj_froe
        self.transOptsDict[numid] = TransOptsManager()  # 私人变换数据
        self.transOptsDict_customize[numid] = False
    # ==========================================

    def SetTransOptsDict(self, id_, transOM):
        assert isinstance(transOM, TransOptsManager)
        assert id_ in ['back', 'fore'] or id_ in self.objDict
        if id_ in self.objDict:
            self.transOptsDict[id_] = transOM
            self.transOptsDict_customize[id_] = True
        else:
            self.transOptsDict[id_] = transOM

    def GetTransOpts(self, id_):
        assert id_ in ['back', 'fore'] or id_ in self.objDict
        if id_ in self.objDict:  # 个人设置优先级高
            return self.transOptsDict[id_]
        elif id_ in ['back', 'fore']:
            if id_ in self.transOptsDict:
                return self.transOptsDict[id_]
            else:
                self.transOptsDict[id_] = TransOptsManager()
                return self.transOptsDict[id_]

    # ==========================
    def TransAllOnce(self, nameDict):
        # 产生一次图
        # 对于背景
        # <多背景需要对这里进行修改>
        back_transOM = self.GetTransOpts('back')
        obj_back = self.objDict[0]
        self.objDict[0] = TransSingalOnce(
                obj_back, self.board, back_transOM, trans_type='back')
        # </>
        for i in range(self.obj_num):
            # 对于所有的前景
            obj_transOM = self.GetTransOpts(i+1)
            if self.transOptsDict_customize[i+1] is False:
                # 从前景拷贝副本，但是保留自身的变换矩阵
                fore_transOM = self.GetTransOpts('fore')
                obj_transOM.Copyfrom(fore_transOM)
            obj_fore = self.objDict[i+1]  # 0是背景
            obj_fore_ = TransSingalOnce(obj_fore, self.board, obj_transOM)
            self.objDict[i+1] = obj_fore_
        self.board.Gen()
        self.board.Save(nameDict)


#def DeepCopytransOM(other):
#        assert isinstance(other, TransOptsManager)
#        # z = {**x, **y} y覆盖x
#        a = TransOptsManager()
#        a.operates_dict = deepcopy(other.operates_dict)
#        a.operates_data = deepcopy(other.operates_data)
#        a.c = deepcopy(other.c)
#        a.mode = deepcopy(other.mode)
#        return a


def TransSingalOnce(obj, board, transOM, trans_type='fore'):
    # 对一个obj变换一次
    assert isinstance(transOM, TransOptsManager)
    trans = Trans(obj)
    operates, operates_opts = transOM.Get()
    trans.QuickTrans(operates, operates_opts)  # 引用传参
    board.addTrans(trans, trans_type)
    return trans.obj_imB


def Zoom(im, raw_size, target_size):
    zx, zy = np.array(target_size) / np.array(raw_size)
    z = max(zx, zy)
    new_size = np.array((z*raw_size), dtype=np.int)
    res_im = im.resize(new_size)
    return res_im

##########################################################
