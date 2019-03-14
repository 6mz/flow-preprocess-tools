# -*- coding: utf-8 -*-
import os
import copy


DEFAULT_NAME_MANAGER2_OPTIONS = {
        'target': '../data/ds_v2',
        'sdir': ['A', 'B', 'gtAB'],
        'prefix': None,
        'suffix': ['A', 'B', 'gtAB'],
        'ext': ['jpg', 'jpg', 'flo']
        }


def GetNameOpts():
    return copy.deepcopy(DEFAULT_NAME_MANAGER2_OPTIONS)


class NameManager2(object):
    def __init__(self, num, name_opts=DEFAULT_NAME_MANAGER2_OPTIONS):
        self.num = num
        self.target = None
        self.fdir = []
        self.head = []
        self.end = []
        self.check(name_opts)

    def check(self, name_opts):
        assert name_opts['target'] != 'TARGET DIR'
        sdir = name_opts['sdir']
        if isinstance(sdir, list):
            gn = len(sdir)
        elif isinstance(sdir, str):
            gn = 1
        else:
            gn = 0
            print('WARRING: NameManager2: sdir is empty')
        self.group_num = gn
        assert not name_opts['prefix'] or len(name_opts['prefix']) == gn
        assert not name_opts['suffix'] or len(name_opts['suffix']) == gn
        assert len(name_opts['ext']) == gn
        self.target = name_opts['target']
        self.fdir = list(map(
                os.path.join, [self.target] * gn, name_opts['sdir']))
        for dir_ in self.fdir:
            pass
            if not os.path.exists(dir_):
                os.makedirs(dir_)
                print(f'INFO: Create {dir_}')
        if name_opts['prefix'] is None:
            self.head = ['' for i in range(gn)]
        else:
            self.head = name_opts['prefix']
        if name_opts['suffix'] is None:
            self.end = list(map(
                    SufCatExt, ['' for i in range(gn)], name_opts['ext']))
        else:
            self.end = list(map(
                    SufCatExt, name_opts['suffix'], name_opts['ext']))

    def name(self, c):
        names = []
        for d, h, e in zip(self.fdir, self.head, self.end):
            names.append(os.path.join(d, h + str(c) + e))
        return names

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        if self.count < self.num:
            x = self.name(self.count)
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
