# -*- coding: utf-8 -*-
import os
import numpy as np
from PIL import Image
from copy import deepcopy
import platform

from VOC_lib import ListMannager
import datasets_func as func


'''
添加流程：
1.TYPE_LIST 里设置类型
2.DEFAULT_OPTS_LIST 里设置默认参数
3.定义初始化函数
4.定义随机获取函数
'''

if platform.system() == 'Windows':
    material_path = "E:/GitProgram/preprocess-tools/data/ds_v2_material"
elif platform.system() == 'Linux':
    system = 'linux'
# ===================== set ===========================
TYPE_LIST = {
        'foreground': ['voc'],
        'background': ['bing', 'sky'],
        }

DEFAULT_MATERIAL_VOC_OPTS = {
        'path': os.path.join(material_path, "voc\\_Annotations"),
        'level': {0: 0.2, 1: 0.25, 2: 0.25, 3: 0.2, 4: 0.1},
        }

DEFAULT_BACKGROUND_BING_OPTS = {
        'path': os.path.join(material_path,
                             "background\\bing-gallery-1366x768"),
        }

DEFAULT_BACKGROUND_SKY_OPTS = {
        'path': os.path.join(material_path, "background\\sky"),
        }


DEFAULT_OPTS_LIST = {
                    'voc': DEFAULT_MATERIAL_VOC_OPTS,
                    'bing': DEFAULT_BACKGROUND_BING_OPTS,
                    'sky': DEFAULT_BACKGROUND_SKY_OPTS
                    }


#
def GetRandomImgOpts(name):
        return deepcopy(DEFAULT_OPTS_LIST[name])


# ================== func ==========================
# 读取列表模块
def ReadVOCList(path):
    # 用于解析RUN_VOC生成的_Annotations文件夹
    materialList = ListMannager()
    materialList.QuickOpen(path)
    materialType = ListMannager()
    for key in materialList.names.keys():
        types = key.split('_')[0]
        materialType.Add(types, key)
    materialLevel = ListMannager()
    for item in materialType.names['level']:
        # 对于等级的制定规则：
        _, lx, ly = item.split('_')
        if int(lx) >= 300 and int(ly) >= 300:
            level = 4
        elif int(lx) >= 200 and int(ly) >= 200:
            level = 3
        elif int(lx) >= 100 and int(ly) >= 100:
            level = 2
        elif int(lx) >= 50 and int(ly) >= 50:
            level = 1
        else:
            level = 0
        materialLevel.Add(level, item)
    return (materialList, materialType, materialLevel)


def ReadList(path, ext='.jpg'):
    # 读取某个文件夹下某种后缀名文件的列表
    fileList = os.listdir(path)
    lists = []
    for file in fileList:
        n, e = os.path.splitext(file)
        if e == ext:
            lists.append(os.path.join(path, file))
    return lists


# ===================================================
# 创建随机器
class RandomImg(object):
    def __init__(self, name, opts=None):
        assert isinstance(name, str)
        if name in TYPE_LIST:
            name = np.random.choice(TYPE_LIST[name])
        assert name in DEFAULT_OPTS_LIST
        self.name = name
        if opts is None:
            self.opts = DEFAULT_OPTS_LIST[name]
        else:
            self.opts = opts
        # 根据name调用不同的初始化方法
        if name == 'voc':
            self.init_voc()
        elif name == 'bing':
            self.init_bing()
        elif name == 'sky':
            self.init_sky()

# 初始化区
    def init_voc(self):
        path = self.opts['path']
        assert os.path.exists(path)
        vocList, vocType, vocLevel = ReadVOCList(path)
        self.list = vocList
        self.__vocType = vocType
        self.__vocLevel = vocLevel

    def init_bing(self):
        path = self.opts['path']
        assert os.path.exists(path)
        bingList = ReadList(path)
        self.list = bingList

    def init_sky(self):
        path = self.opts['path']
        assert os.path.exists(path)
        skyList = ReadList(path)
        self.list = skyList


# 获取区
    def RandomGet(self):
        # 根据name调用不同的获取方法
        if self.name == 'voc':
            return self.RandomGet_VOC()
        elif self.name == 'bing':
            return self.RandomGet_bing()
        elif self.name == 'sky':
            return self.RandomGet_sky()

    def RandomGet_VOC(self):
        # 随机一对图片
        levelProbabilityTables = self.opts['level']
        randLv = func.RandomLevel(levelProbabilityTables)
        lvCatalogList = self.__vocLevel[randLv]
        lvItemList = self.list.Get(lvCatalogList)
        isexists = False
        while not isexists:
            item = np.random.choice(lvItemList)
            imName, maName = item.split('+')
            isexists = os.path.exists(imName) & os.path.exists(maName)
        img = Image.open(imName)
        mask = Image.open(maName)
        return (img, mask)  # 返回Image对象

    def RandomGet_bing(self):
        isexists = False
        while not isexists:
            item = np.random.choice(self.list)
            isexists = os.path.exists(item)
        img = Image.open(item)
        return img  # 返回Image对象(背景图只返回图片，没有mask)

    def RandomGet_sky(self):
        isexists = False
        while not isexists:
            item = np.random.choice(self.list)
            isexists = os.path.exists(item)
        img = Image.open(item)
        return img  # 返回Image对象(背景图只返回图片，没有mask)


#def GetRandomBackground(opts):
#    path = opts['background_path']
#    materialList, materialType, materialLevel = ReadMaterialList(path)
#    randLv = func.RandomLevel(level)
#    lvCatalogList = materialLevel[randLv]
#    lvItemList = materialList.Get(lvCatalogList)
#    item = np.random.choice(lvItemList)
#    img,mask = GetImgAndMask(item)
#    return (img, mask)

