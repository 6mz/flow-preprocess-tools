from NameManager2 import NameManager2, GetNameOpts
from datasets_lib2 import MainBoard, DEFAULT_MAINBOARD_OPTS, TransOptsManager


class Sequence(object):
    '''
    快速生成NameManager2的opts
    '''
    def __init__(
            self, iter_num, sequence_num, path,
            outitems=['im', 'fAB', 'fBA', 'vAB', 'vBA'],
            outdirform='together'
            ):
        assert outdirform in ['together', 'split']
        assert set(outitems).issubset(set(['im', 'fAB', 'fBA', 'vAB', 'vBA']))
        assert 2 <= sequence_num and 1 <= iter_num
        res = GenNameOpts(sequence_num, outitems, outdirform)
        operation, sdir, suffix, ext = res
        name_opts = GetNameOpts()
        name_opts['target'] = path
        name_opts['operation'] = operation
        name_opts['sdir'] = sdir
        name_opts['suffix'] = suffix
        name_opts['ext'] = ext
        self.nameManager = NameManager2(iter_num, name_opts)
        self.step = len(outitems)

    def NameManager2(self):
        return self.nameManager

def GenOperation(outitem):
    if outitem == 'im':
        return 'imB'
    elif outitem == 'fAB':
        return 'flowAB'
    elif outitem == 'fBA':
        return 'flowBA'
    elif outitem == 'vAB':
        return 'flowAB_viz'
    elif outitem == 'vBA':
        return 'flowBA_viz'


def GenSdir(sequence_id, outitem, outdirform):
    sequence_strid = column_to_name(sequence_id)
    if outitem == 'im':
        sdir_candidate = ['show', sequence_strid]
    elif outitem == 'fAB' or outitem == 'fBA':
        sdir_candidate = ['flow', 'flow']
    elif outitem == 'vAB' or outitem == 'vBA':
        sdir_candidate = ['show', 'viz_flow']
    return sdir_candidate[outdirform == 'split']


def GenExt(outitem):
    if outitem == 'im':
        return 'png'
    elif outitem == 'fAB' or outitem == 'fBA':
        return 'flo'
    elif outitem == 'vAB' or outitem == 'vBA':
        return 'jpg'


def GenSuffix(sequence_id, outitem):
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


def GenNameOpts(sequence_num, outitems, outdirform):
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
    for pic_id in range(1, sequence_num):
        for outitem in outitems:
            operation.append(GenOperation(outitem))
            sdir.append(GenSdir(pic_id, outitem, outdirform))
            suffix.append(GenSuffix(pic_id, outitem))
            ext.append(GenExt(outitem))
    return operation, sdir, suffix, ext


def column_to_name(colnum):
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
