from NameManager2 import NameManager2, GetNameOpts
import datasets_func as func
import os

class Aim_3(object):
    '''
    NameManager2的管理类，对其进行了特化设置，用于更加方便的一键生成任意长的 
    <对准中间帧的3帧序列> 
    '''
    def __init__(
            self, iter_num, path,
            outitems=['im', 'flow','viz'],
            outdirform='together'
            ):
        assert outdirform in ['together', 'split']
        assert set(outitems).issubset(set(['im', 'flow', 'viz']))
        assert 1 <= iter_num
        res = self.GenNameOpts(outitems, outdirform)
        operation, sdir, suffix, ext = res
        name_opts = GetNameOpts()
        name_opts['target'] = path
        name_opts['operation'] = operation
        name_opts['sdir'] = sdir
        name_opts['suffix'] = suffix
        name_opts['ext'] = ext
        self.nameManager = NameManager2(iter_num, name_opts)
        self.step = len(outitems)
        self.nameList = []
        self.uncoverList = []
        self.path = path

    def NameManager2(self):
        return self.nameManager

    def __iter__(self):
        self.nameManager.__iter__()
        return self

    def __next__(self):
        name_dict_list = next(self.nameManager)  # error 信号由nameManager发出
        self.nameList.append(name_dict_list)
        s = Step(name_dict_list, self.step)
        return s

    def GenNameOpts(self, outitems, outdirform):
        # 自动生成各个输出项目的文件名
        operation = []
        sdir = []
        suffix = []
        ext = []
        # 0
        pic_id = 0
        if 'im' in outitems:
            operation.append('imB')
            sdir.append(GenSdir(pic_id, 'im', outdirform))
            suffix.append(GenSuffix(pic_id, 'im'))
            ext.append(GenExt('im'))
        # 1,2; 对齐1
        for pic_id in range(1, 3):
            for outitem in outitems:
                if outitem == 'flow':
                    outitem = 'fBA' if pic_id == 1 else 'fAB'
                elif outitem == 'viz':
                    outitem = 'vBA' if pic_id == 1 else 'vAB'
                operation.append(GenOperation(outitem))
                sdir.append(GenSdir(pic_id, outitem, outdirform))
                suffix.append(GenSuffix(pic_id, outitem))
                ext.append(GenExt(outitem))
        return operation, sdir, suffix, ext

    def SaveList(self, fname=None):
        if fname is None:
            fname = os.path.join(self.path, 'file_list.txt')
        nameList = self.ArrangeNameList()
        uncoverList = self.ArrangeUncoverList()
        func.SaveList(fname, nameList)
        func.SaveList(os.path.join(self.path, 'uncover.txt'), uncoverList)

    def ArrangeNameList(self):
        nameList = self.nameList
        res_list = []
        for item in nameList:
            item_pic = []
            item_flow = []
            item_m = []
            for n,p in item:
                if n == 'imB':
                    p_ = os.path.realpath(os.path.normpath(p))
                    item_pic.append(p_)
                elif n == 'flowAB' or n == 'flowBA':
                    p_ = os.path.realpath(os.path.normpath(p))
                    item_flow.append(p_)
                elif n == 'backMAB' or n== 'backMBA':
                    p_ = os.path.realpath(os.path.normpath(p))
                    item_m.append(p_)
            res_list.append(' '.join(item_pic + item_flow + item_m))
        return res_list

    def AddUncover(self,ids):
        self.uncoverList.append(ids)

    def ArrangeUncoverList(self):
        return list(set(self.uncoverList))


class Sequence(object):
    '''
    NameManager2的管理类，对其进行了特化设置，用于更加方便的一键生成任意长的 
    <普通序列> 
    '''
    def __init__(
            self, iter_num, sequence_num, path,
            outitems=['im', 'fAB', 'fBA', 'vAB', 'vBA'],
            outdirform='together'
            ):
        assert outdirform in ['together', 'split']
        assert set(outitems).issubset(set(['im', 'fAB', 'fBA', 'vAB', 'vBA']))
        assert 2 <= sequence_num and 1 <= iter_num
        res = self.GenNameOpts(sequence_num, outitems, outdirform)
        operation, sdir, suffix, ext = res
        name_opts = GetNameOpts()
        name_opts['target'] = path
        name_opts['operation'] = operation
        name_opts['sdir'] = sdir
        name_opts['suffix'] = suffix
        name_opts['ext'] = ext
        self.nameManager = NameManager2(iter_num, name_opts)
        self.step = len(outitems)
        self.nameList = []
        self.uncoverList = []
        self.path = path

    def NameManager2(self):
        return self.nameManager

    def __iter__(self):
        self.nameManager.__iter__()
        return self

    def __next__(self):
        name_dict_list = next(self.nameManager)  # error 信号由nameManager发出
        self.nameList.append(name_dict_list)
        s = Step(name_dict_list, self.step)
        return s

    def GenNameOpts(self, sequence_num, outitems, outdirform):
        operation = []
        sdir = []
        suffix = []
        ext = []
        # 0
        if 'im' in outitems:
            operation.append('imB')
            sdir.append(GenSdir(0, 'im', outdirform))
            suffix.append(GenSuffix(0, 'im'))
            ext.append(GenExt('im'))
        # 1-N
        for pic_id in range(1, sequence_num):
            for outitem in outitems:
                operation.append(GenOperation(outitem))
                sdir.append(GenSdir(pic_id, outitem, outdirform))
                suffix.append(GenSuffix(pic_id, outitem))
                ext.append(GenExt(outitem))
        return operation, sdir, suffix, ext

    def SaveList(self, fname=None):
        if fname is None:
            fname = os.path.join(self.path, 'file_list.txt')
        nameList = self.ArrangeNameList()
        uncoverList = self.ArrangeUncoverList()
        func.SaveList(fname, nameList)
        func.SaveList(os.path.join(self.path, 'uncover.txt'), uncoverList)

    def ArrangeNameList(self):
        nameList = self.nameList
        res_list = []
        for item in nameList:
            item_pic = []
            item_flow = []
            item_m = []
            for n,p in item:
                if n == 'imB':
                    p_ = os.path.realpath(os.path.normpath(p))
                    item_pic.append(p_)
                elif n == 'flowAB' or n == 'flowBA':
                    p_ = os.path.realpath(os.path.normpath(p))
                    item_flow.append(p_)
                elif n == 'backMAB' or n== 'backMBA':
                    p_ = os.path.realpath(os.path.normpath(p))
                    item_m.append(p_)
            res_list.append(' '.join(item_pic + item_flow + item_m))
        return res_list

    def AddUncover(self,ids):
        self.uncoverList.append(ids)

    def ArrangeUncoverList(self):
        return list(set(self.uncoverList))


class DeepHomo_2(object):
    '''
    NameManager2的管理类，对其进行了特化设置，用于更加方便的一键生成任意长的 
    <???????> 
    '''
    def __init__(
            self, iter_num, path,
            outitems=['im', 'fAB', 'vAB', 'mAB'],
            outdirform='together'
            ):
        assert outdirform in ['together', 'split']
        assert set(outitems).issubset(
                set(['im', 'fAB', 'fBA', 'vAB', 'vBA', 'mAB', 'mBA']))
        assert 1 <= iter_num
        res = self.GenNameOpts(outitems, outdirform)
        operation, sdir, suffix, ext = res
        name_opts = GetNameOpts()
        name_opts['target'] = path
        name_opts['operation'] = operation
        name_opts['sdir'] = sdir
        name_opts['suffix'] = suffix
        name_opts['ext'] = ext
        self.nameManager = NameManager2(iter_num, name_opts)
        self.step = len(outitems)
        self.nameList = []
        self.uncoverList = []
        self.path = path

    def NameManager2(self):
        return self.nameManager

    def __iter__(self):
        self.nameManager.__iter__()
        return self

    def __next__(self):
        name_dict_list = next(self.nameManager)  # error 信号由nameManager发出
        self.nameList.append(name_dict_list)
        s = Step(name_dict_list, self.step)
        return s

    def GenNameOpts(self, outitems, outdirform):
        operation = []
        sdir = []
        suffix = []
        ext = []
        # 0
        if 'im' in outitems:
            operation.append('imB')
            sdir.append(GenSdir(0, 'im', outdirform))
            suffix.append(GenSuffix(0, 'im'))
            ext.append(GenExt('im'))
        # 1
        for pic_id in range(1, 2):
            for outitem in outitems:
                operation.append(GenOperation(outitem))
                sdir.append(GenSdir(pic_id, outitem, outdirform))
                suffix.append(GenSuffix(pic_id, outitem))
                ext.append(GenExt(outitem))
        return operation, sdir, suffix, ext

    def SaveList(self, fname=None):
        if fname is None:
            fname = os.path.join(self.path, 'file_list.txt')
        nameList = self.ArrangeNameList()
        uncoverList = self.ArrangeUncoverList()
        func.SaveList(fname, nameList)
        func.SaveList(os.path.join(self.path, 'uncover.txt'), uncoverList)

    def ArrangeNameList(self):
        nameList = self.nameList
        res_list = []
        for item in nameList:
            item_pic = []
            item_flow = []
            item_m = []
            for n,p in item:
                if n == 'imB':
                    p_ = os.path.realpath(os.path.normpath(p))
                    item_pic.append(p_)
                elif n == 'flowAB' or n == 'flowBA':
                    p_ = os.path.realpath(os.path.normpath(p))
                    item_flow.append(p_)
                elif n == 'backMAB' or n== 'backMBA':
                    p_ = os.path.realpath(os.path.normpath(p))
                    item_m.append(p_)
            res_list.append(' '.join(item_pic + item_flow + item_m))
        return res_list

    def AddUncover(self,ids):
        self.uncoverList.append(ids)

    def ArrangeUncoverList(self):
        return list(set(self.uncoverList))


# =========================  func  ==============================
class Step(object):
    def __init__(self, name_dict_list, step):
        self.name_dict_list = name_dict_list
        self.step = step
        self.count = 0

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        count = self.count
        if count >= len(self.name_dict_list):
            raise StopIteration
        if self.count == 0:
            self.count += 1
            return dict((self.name_dict_list[count],))
        else:
            self.count += self.step
            return dict(self.name_dict_list[count:self.count])

# ================================
# 添加新项目请更改下面3个函数
# 上面的类中的__init__、ArrangeNameList函数
# 以及NameManager2的check函数
# 还有lib1的Board类的save函数
# ================================

def GenOperation(outitem):
    # 返回Board类的Save函数中的操作
    if outitem == 'im':  # 序列操作imA就是上一帧的imB，因此im默认为imB
        return 'imB'
    elif outitem == 'fAB':
        return 'flowAB'
    elif outitem == 'fBA':
        return 'flowBA'
    elif outitem == 'vAB':
        return 'flowAB_viz'
    elif outitem == 'vBA':
        return 'flowBA_viz'
    elif outitem == 'mAB':
        return 'backMAB'
    elif outitem == 'mBA':
        return 'backMBA'

def GenSdir(sequence_id, outitem, outdirform):
    # 返回子文件夹名称
    # sequence_id：序号， outitem：项目， outdirform：输出类型
    sequence_strid = column_to_name(sequence_id)
    if outitem == 'im':
        sdir_candidate = ['show', sequence_strid]
    elif outitem == 'fAB' or outitem == 'fBA':
        sdir_candidate = ['flow', 'flow']
    elif outitem == 'vAB' or outitem == 'vBA':
        sdir_candidate = ['show', 'viz_flow']
    elif outitem == 'mAB' or outitem == 'mBA':
        sdir_candidate = ['M', 'M']
    # 根据输出类型二选一(独立文件夹或同一个文件夹)
    return sdir_candidate[outdirform == 'split']


def GenExt(outitem):  # 返回扩展名
    if outitem == 'im':
        return 'png'
    elif outitem == 'fAB' or outitem == 'fBA':
        return 'flo'
    elif outitem == 'vAB' or outitem == 'vBA':
        return 'jpg'
    elif outitem == 'mAB' or outitem == 'mBA':
        return 'npy'


def GenSuffix(sequence_id, outitem):  # 返回名称后缀部分
    sequence_strid_b = column_to_name(sequence_id)
    sequence_strid_a = column_to_name(sequence_id - 1)
    if outitem == 'im':
        return sequence_strid_b
    elif outitem == 'fAB':
        return 'gt' + sequence_strid_a + sequence_strid_b
    elif outitem == 'fBA':
        return 'gt' + sequence_strid_b + sequence_strid_a
    elif outitem == 'vAB':
        return 'viz_gt' + sequence_strid_a + sequence_strid_b
    elif outitem == 'vBA':
        return 'viz_gt' + sequence_strid_b + sequence_strid_a
    elif outitem == 'mAB':
        return 'M' + sequence_strid_a + sequence_strid_b
    elif outitem == 'mBA':
        return 'M' + sequence_strid_b + sequence_strid_a


def column_to_name(colnum):  # excel的列风格的命名法
    # 0->A 26->AA
    if type(colnum) is not int:
        return colnum
    str_ = [] if colnum > 0 else ['A']
    while(colnum > 0):
        str_ += chr(colnum % 26 + ord('A'))
        colnum //= 26
    out = str_[::-1]
    if len(out) > 1:
        out[0] = chr(ord(out[0])-1)
    return ''.join(out)
