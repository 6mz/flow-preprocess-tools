# -*- coding: utf-8 -*-
from os.path import *
from glob import glob
import random

def Randomlist(list_path,item_num = 10,ltype = 'Sintel',ltype2 = 'clean',lister  = None):
    datasets_lister = lister
    if(not datasets_lister):
        if('Sintel' == ltype):
            if('clean' == ltype2):
                print('setting datasets_lister: MpiSintelClean_list ...')
                datasets_lister = MpiSintelClean_list(list_path)
            elif('final' == ltype2):
                print('setting datasets_lister: MpiSintelFinal_list ...')
                datasets_lister = MpiSintelFinal_list(list_path)
        elif('FlyingChairs' == ltype):
            print('setting datasets_lister: FlyingChairs_list ...')
            datasets_lister = FlyingChairs_list(list_path)
        elif('FlyingThings' == ltype):
            if('clean' == ltype2):
                print('setting datasets_lister: FlyingThingsClean_list ...')
                datasets_lister = FlyingThingsClean_list(list_path)
            if('final' == ltype2):
                print('setting datasets_lister: FlyingThingsFinal_list ...')
                datasets_lister = FlyingThingsFinal_list(list_path)

    if(None == datasets_lister ):
        print('nWANNING : datasets not found\n')
        return []
    if(datasets_lister.is_empty):
        return []
    if(0 >= item_num or len(datasets_lister) < item_num):
        item_num = len(datasets_lister)

    img1s=[]
    img2s=[]
    gtflows=[]
    for i in range(item_num):
        item_id = random.randint(0,len(datasets_lister)-1)
        group = datasets_lister[item_id]
        img1s.append(group[0])
        img2s.append(group[1])
        gtflows.append(group[2])

    return (img1s,img2s,gtflows)


# ==================================== Sintel ==============================================

class MpiSintel_list(object):
    def __init__(self, root = '', dstype = 'clean'):
        self.flow_list = []
        self.image_list = []
        self.is_empty=False

        flow_root = join(root, 'flow')# 文件夹目录
        image_root = join(root, dstype)

        file_list = sorted(glob(join(flow_root, '*/*.flo')))# flow文件夹下的二级目录的所有flo文件路径列表

        for file in file_list:
            if 'test' in file:# 如果文件名带有test则跳过
                continue

            fbase = file[len(flow_root)+1:]# 光流文件相对路径（去掉root路径，加一是为了去掉/）
            fprefix = fbase[:-8]# 光流文件路径前部分（sintel数据集的文件名格式为frame_0000.flo,这里去掉了0000.flo）
            fnum = int(fbase[-8:-4])# 光流帧序号（整型）

            # 获得图像对(图像根路径替换光流根路径)
            img1 = join(image_root, fprefix + "%04d"%(fnum+0) + '.png')
            img2 = join(image_root, fprefix + "%04d"%(fnum+1) + '.png')

            # 如果出现意外（图像或光流文件不存在）则跳过
            if not isfile(img1) or not isfile(img2) or not isfile(file):
                continue

            self.image_list += [[img1, img2]]
            self.flow_list += [file]

        self.size = len(self.image_list)
        assert (len(self.image_list) == len(self.flow_list))
        if(len(self.image_list)<=0):
            self.is_empty=True
            print('='*10 + '\nWANNING : MpiSintel_lister not find any files ,please check input dataset path!\n')

    def __getitem__(self, index):
        index = index % self.size
        img1 = self.image_list[index][0]
        img2 = self.image_list[index][1]
        flow = self.flow_list[index]
        return (img1,img2,flow)

    def __len__(self):
        return self.size


class MpiSintelClean_list(MpiSintel_list):
    def __init__(self, root , dstype = 'clean'):
        super(MpiSintelClean_list, self).__init__(root = root, dstype = dstype)

class MpiSintelFinal_list(MpiSintel_list):
    def __init__(self, root , dstype = 'final'):
        super(MpiSintelFinal_list, self).__init__(root = root, dstype = dstype)


# ===================================== FlyingChairs ============================================
class FlyingChairs_list(object):
    def __init__(self, root = '', dstype = None):
        self.flow_list = []
        self.image_list = []
        self.is_empty=False

        images = sorted( glob( join(root, '*.ppm') ) )
        self.flow_list = sorted( glob( join(root, '*.flo') ) )
        assert (len(images)//2 == len(self.flow_list))

        for i in range(len(self.flow_list)):
            im1 = images[2*i]
            im2 = images[2*i + 1]
            self.image_list += [ [ im1, im2 ] ]

        assert len(self.image_list) == len(self.flow_list)
        self.size = len(self.image_list)

        if(len(self.image_list)<=0):
            print('='*10 + '\nWANNING : FlyingChairs_lister not find any files ,please check input dataset path!\n')
            self.is_empty=True

    def __getitem__(self, index):
        index = index % self.size
        img1 = self.image_list[index][0]
        img2 = self.image_list[index][1]
        flow = self.flow_list[index]
        return (img1,img2,flow)

    def __len__(self):
        return self.size

# ===================================== FlyingThings ==============================================

class FlyingThings_list(object):
    def __init__(self, root = '', dstype = 'frames_cleanpass'):
        self.flow_list = []
        self.image_list = []
        self.is_empty=False

        image_dirs = sorted(glob(join(root, dstype, 'TRAIN/*/*')))
        image_dirs = sorted([join(f, 'left') for f in image_dirs] + [join(f, 'right') for f in image_dirs])

        flow_dirs = sorted(glob(join(root, 'optical_flow/TRAIN/*/*')))
        flow_dirs = sorted([join(f, 'into_future/left') for f in flow_dirs] + [join(f, 'into_future/right') for f in flow_dirs])

        assert (len(image_dirs) == len(flow_dirs))

        for idir, fdir in zip(image_dirs, flow_dirs):
            images = sorted( glob(join(idir, '*.png')) )
            flows = sorted( glob(join(fdir, '*.pfm')) )
            for i in range(len(flows)-1):
                self.image_list += [ [ images[i], images[i+1] ] ]
                self.flow_list += [flows[i]]

        assert len(self.image_list) == len(self.flow_list)
        self.size = len(self.image_list)

        if(len(self.image_list)<=0):
            print('='*10 + '\nWANNING : FlyingThings_lister not find any files ,please check input dataset path!\n')
            self.is_empty=True

    def __getitem__(self, index):
        index = index % self.size
        img1 = self.image_list[index][0]
        img2 = self.image_list[index][1]
        flow = self.flow_list[index]
        return (img1,img2,flow)

    def __len__(self):
        return self.size

class FlyingThingsClean_list(FlyingThings_list):
    def __init__(self, root ,dstype = 'frames_cleanpass'):
        super(FlyingThingsClean_list, self).__init__(root = root, dstype = 'frames_cleanpass')

class FlyingThingsFinal_list(FlyingThings_list):
    def __init__(self, root ,dstype = 'frames_finalpass'):
        super(FlyingThingsFinal_list, self).__init__(root = root, dstype = 'frames_finalpass')

