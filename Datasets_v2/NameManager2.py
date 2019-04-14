# -*- coding: utf-8 -*-
import os
import copy


DEFAULT_NAME_MANAGER2_OPTIONS = {
        'target': 'TARGET DIR',
         # 操作，与dataset_lib1中的Board类的Save函数中的相一致
        'operation': ['imA', 'imB', 'flowAB_viz'],
        'sdir': ['A', 'B', 'viz_gtAB'],
        'prefix': None,
        'suffix': ['A', 'B', 'viz_gtAB'],
        'ext': ['png', 'png', 'jpg']
        }


def GetNameOpts():
    return copy.deepcopy(DEFAULT_NAME_MANAGER2_OPTIONS)


class NameManager2(object):
    def __init__(self, num, name_opts=DEFAULT_NAME_MANAGER2_OPTIONS,
                 start=0, countinue=False):
        self.num = num
        self.target = None
        self.operation = []
        self.fdir = []
        self.head = []
        self.end = []
        # count
        self.count = start
        self.start = start
        self.countinue = countinue
        self.check(name_opts)

    def check(self, name_opts):
        assert name_opts['target'] != 'TARGET DIR'
        self.operation = name_opts['operation']
        gn = len(self.operation)
        # 判断操作合法性
        assert set(name_opts['operation']).issubset(
                set(['imA', 'imB', 'flowAB', 'flowBA',
                     'flowAB_viz', 'flowBA_viz', 'backMAB', 'backMBA']))
        # 判断长度一致性
        assert not name_opts['prefix'] or len(name_opts['prefix']) == gn
        assert not name_opts['suffix'] or len(name_opts['suffix']) == gn
        assert len(name_opts['sdir']) == gn
        assert len(name_opts['ext']) == gn
        self.target = name_opts['target']
        self.fdir = list(map(
                os.path.join, [self.target] * gn, name_opts['sdir']))
        # 创建子文件夹
        for dir_ in self.fdir:
            if not os.path.exists(dir_):
                os.makedirs(dir_)
                print(f'INFO: Create {dir_}')
        # 生成前缀名
        if name_opts['prefix'] is None:
            self.head = ['' for i in range(gn)]
        else:
            self.head = name_opts['prefix']
        # 生成后缀名
        if name_opts['suffix'] is None:
            self.end = list(map(
                    SufCatExt, ['' for i in range(gn)], name_opts['ext']))
        else:
            self.end = list(map(
                    SufCatExt, name_opts['suffix'], name_opts['ext']))

    def Name_dict(self, c):
        # 生成对应序号的操作和名称字典
        names = []
        for d, h, e in zip(self.fdir, self.head, self.end):
            names.append(os.path.join(d, h + str(c) + e))
        assert len(self.operation) == len(names)
        return list(zip(self.operation, names))

    def __iter__(self):
        if not self.countinue:
            self.count = self.start
        return self

    def __next__(self):
        if self.count < self.num:
            x = self.Name_dict(self.count)
            self.count += 1
            return x
        else:
            raise StopIteration


def SufCatExt(s, e):
    if(e[0] != '.'):
        return s + '.' + e
    return s + e


if __name__ == '__main__':
    pass
#    o = DEFAULT_NAME_MANAGER2_OPTIONS
#    o['target'] = '../data/ds_v2'
#    n = NameManager2(10, o)
#    for name in n:
#        print(name)
