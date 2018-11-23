# -*- coding: utf-8 -*-
from os.path import *
from glob import glob
import random

from myflowlib import read_gen,save_list



def Randomlist(datasets_path, save_path , num = 10,ltype = 'Sintel',ltype2 = 'clean'):
    res = GenerateRandomlist(datasets_path,item_num = num,ltype = ltype,ltype2 = ltype2)
    print('saving list..')
    save_img1_name = join(save_path, "img1.txt")
    save_img2_name = join(save_path, "img2.txt")
    save_gtflow_name = join(save_path, "groundtruth.txt")
    save_list(save_img1_name,res[0])
    save_list(save_img2_name,res[1])
    save_list(save_gtflow_name,res[2])
    print('output img1.txt,img2.txt,groundtruth.txt in ' + \
          'current folder' if len(save_path)==0 else save_path)

def GenerateRandomlist(list_path,item_num = 10,ltype = 'Sintel',ltype2 = 'clean',lister  = None):
    datasets_lister = lister
    if(not datasets_lister):
        if('Sintel' == ltype):
            if('clean' == ltype2):
                print('setting datasets_lister: MpiSintelClean_list ...')
                datasets_lister = MpiSintelClean_list(list_path)

            elif('final' == ltype2):
                print('setting datasets_lister: MpiSintelFinal_list ...')
                datasets_lister = MpiSintelFinal_list(list_path)

    if(None == datasets_lister):
        print('datasets not found')
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
        img2s.append(group[0])
        gtflows.append(group[0])

    return (img1s,img2s,gtflows)



class MpiSintel_list(object):
    def __init__(self, root = '', dstype = 'clean'):
        self.flow_list = []
        self.image_list = []

        # 文件夹目录
        flow_root = join(root, 'flow')
        image_root = join(root, dstype)

        # flow文件夹下的二级目录的所有flo文件路径列表
        file_list = sorted(glob(join(flow_root, '*/*.flo')))

        for file in file_list:
            # 如果文件名带有test则跳过
            if 'test' in file:
                # print file
                continue

            # 光流文件相对路径（去掉root路径，加一是为了去掉/）
            fbase = file[len(flow_root)+1:]
            # 光流文件路径前部分（sintel数据集的文件名格式为frame_0000.flo,这里去掉了0000.flo）
            fprefix = fbase[:-8]
            # 光流帧序号（整型）
            fnum = int(fbase[-8:-4])

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
        assert(len(self.image_list)>0)

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


