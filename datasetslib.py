# -*- coding: utf-8 -*-
from os.path import *
from glob import glob
import random

from myflowlib import read_gen,save_list,read_list



class EasyTest(object):
    def __init__(self,datasets_path,ltype='Sintel' ,ltype2='clean',num=10):
        self.datasets_path = datasets_path
        self.ltype = ltype 
        self.ltype2 = ltype2 
        self.num = num
        
        self.set_txtpath()
        self.set_txtname("img1.txt", "img2.txt", "groundtruth.txt", "out.txt", "viz.txt", "warp.txt")
        self.set_targetdir("./data/test1","flow", "vizflow", "vizwarp")
        self.set_names("t","f.jpg","f_viz.jpg","A_forward.jpg")
        self.init_Randomlist()

    def init_Randomlist(self):
        res = Randomlist(self.datasets_path, self.num, self.ltype, self.ltype2)
        if not res:
            self.isempty = True
            self.imgA = []
            self.imgB = []
            self.gtflow = []
        else:
            self.isempty = False
            self.imgA = res[0]
            self.imgB = res[1]
            self.gtflow = res[2]

    def set_txtpath(self,txt_save_path = '' ):
        self.txt_save_path = txt_save_path

    def set_txtname(self,img1=None,img2=None,gt=None,out=None,viz=None,warp=None):
        if(img1):self.img1txtname = img1 
        if(img2):self.img2txtname = img2 
        if(gt):self.groundtruthtxtname = gt 
        if(out):self.outflowtxtname = out 
        if(viz):self.vizflowtxtname = viz 
        if(warp):self.warptxtname = warp 

    def set_targetdir(self,targetdir=None,outdir=None,vizdir=None,warpdir=None):
        if(targetdir):self.targetdir = targetdir 
        if(outdir):self.outflowdir = outdir 
        if(vizdir):self.vizflowdir = vizdir 
        if(warpdir):self.warpdir = warpdir 

    def set_names(self,head=None,outend=None,vizend=None,warpend=None):
        if(head):self.head = head 
        if(outend):self.outflowend = outend 
        if(vizend):self.vizflowend = vizend 
        if(warpend):self.warpend = warpend 

    def GenerateRandomlist(self):
        print('saving list..')
        save_img1_name = join(self.txt_save_path, self.img1txtname)
        save_img2_name = join(self.txt_save_path, self.img2txtname)
        save_gtflow_name = join(self.txt_save_path, self.groundtruthtxtname)
        save_list(save_img1_name,self.imgA)
        save_list(save_img2_name,self.imgB)
        save_list(save_gtflow_name,self.gtflow)
        print('output %s,%s,%s in '%(self.img1txtname,self.img2txtname,self.groundtruthtxtname) + \

    def GenerateOutVizWarplist(self)
        save_out_name = join(save_txt_path,'out.txt')
        save_viz_name = join(save_txt_path,'viz.txt')
        save_warp_name = join(save_txt_path,'warp.txt')
        idlist = list(map(str,range(num)))
        outlist = [head+x+outend for x in idlist]
        vizlist = [head+x+vizend for x in idlist]
        warplist = [head+x+warpend for x in idlist]
        outlist = list(map(join,[file_path]*num,[outdir]*num,outlist))
        vizlist = list(map(join,[file_path]*num,[vizdir]*num,vizlist))
        warplist = list(map(join,[file_path]*num,[warpdir]*num,warplist))
        save_list(save_out_name,outlist)
        save_list(save_viz_name,vizlist)
        save_list(save_warp_name,warplist)
        print('output out.txt,viz.txt,warp.txt in ' + \
              'current folder' if len(save_txt_path)==0 else save_txt_path)


    def print_all(self):
        print ('arg for EasyTest:')
        print ('\n'.join(['%s:%s' % item for item in self.__dict__.items()]))
#(Aname,Bname,gtname)
#(newn)


#============================== funtions ========================================

def MovePicsforLinux(namelist,target_path):
    path,name=os.path.split(namelist)



#GenerateOutVizWarplist('./data/test1','',5,vizdir='show',warpdir='show')
def GenerateOutVizWarplist(file_path,save_txt_path,num,outdir='flow',vizdir='vizflow',warpdir='vizwarp',\
               head='t',outend='f.jpg',vizend='f_viz.jpg',warpend='A_forward.jpg'):
    save_out_name = join(save_txt_path,'out.txt')
    save_viz_name = join(save_txt_path,'viz.txt')
    save_warp_name = join(save_txt_path,'warp.txt')
    idlist = list(map(str,range(num)))
    outlist = [head+x+outend for x in idlist]
    vizlist = [head+x+vizend for x in idlist]
    warplist = [head+x+warpend for x in idlist]
    outlist = list(map(join,[file_path]*num,[outdir]*num,outlist))
    vizlist = list(map(join,[file_path]*num,[vizdir]*num,vizlist))
    warplist = list(map(join,[file_path]*num,[warpdir]*num,warplist))
    save_list(save_out_name,outlist)
    save_list(save_viz_name,vizlist)
    save_list(save_warp_name,warplist)
    print('output out.txt,viz.txt,warp.txt in ' + \
          'current folder' if len(save_txt_path)==0 else save_txt_path)



#GenerateRandomlist(root_path,'',num=5)
def GenerateRandomlist(datasets_path, save_txt_path , num = 10,ltype = 'Sintel',ltype2 = 'clean'):
    res = Randomlist(datasets_path,item_num = num,ltype = ltype,ltype2 = ltype2)
    print('saving list..')
    save_img1_name = join(save_txt_path, "img1.txt")
    save_img2_name = join(save_txt_path, "img2.txt")
    save_gtflow_name = join(save_txt_path, "groundtruth.txt")
    save_list(save_img1_name,res[0])
    save_list(save_img2_name,res[1])
    save_list(save_gtflow_name,res[2])
    print('output img1.txt,img2.txt,groundtruth.txt in ' + \
          'current folder' if len(save_txt_path)==0 else save_txt_path)
    return res


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

    if(None == datasets_lister):
        print('Wanning : datasets not found\n')
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


# =========================== define datasets list ===========================

class MpiSintel_list(object):
    def __init__(self, root = '', dstype = 'clean'):
        self.flow_list = []
        self.image_list = []

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
            print('='*10 + '\nwanning,MpiSintel_lister not find any files ,please check input dataset path!\n')

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


