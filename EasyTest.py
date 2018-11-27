# -*- coding: utf-8 -*-
from os.path import *
from glob import glob

import subprocess
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from scipy.misc import imsave,imread

from myflowlib import read_gen,save_list,read_list,save_3ziplist
from myflowlib import Sparplot,EPE,EPE_usingmask,abs_flow,viz_flow
from datasetslib import Randomlist


class EasyTest(object):
    def __init__(self,datasets_path,ltype='Sintel' ,ltype2='clean',dirs = './data/yourdir',num=10):
        self.datasets_path = datasets_path
        self.ltype = ltype 
        self.ltype2 = ltype2 
        self.num = num
        self.init_dir(dirs)

        self.set_txtpath("./txts")
        self.set_txtname("img1.txt", "img2.txt", "groundtruth.txt", "out.txt", "viz.txt", "warp.txt")
        self.set_txtsparname("sparplot.txt","spardatalist.txt","sparbest.txt","spargrayres.txt",\
                             "spargraybest.txt","spargraygt.txt")
        self.set_targetdir("","flow", "vizflow", "vizwarp" )
        self.set_targetname("t","f.flo","f_viz.jpg","A_forward.jpg")
        self.set_movedir("","A","B","gt")
        self.set_movename(self.head,"A","B","gt")
        self.set_spar(20,"default")
        self.set_spardir("","sparplot","spardata",self.vizflowdir,"vizflow_gray","vizflow_gray","vizflow_gray")
        self.set_sparname(self.head,"sp.jpg","sd.txt","f_viz_resbest.jpg","f_gviz_res.jpg","f_gviz_resbest.jpg","f_gviz_gt.jpg")
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
        self.datalen=len(imgA)

    def init_dir(self,dirs):
        self.dir = dirs
        self.targetdir = dirs
        self.movedir = dirs
        self.spar_dir = dirs

    def set_txtpath(self,txt_save_path = '' ):
        self.txt_save_path = txt_save_path

    def set_dir(self,dirs):
            self.dir = dirs
            self.targetdir = join(self.dir,self.targetdir_short)
            self.movedir = join(self.dir,self.movedir_short)
            self.spar_dir = join(self.dir,self.spar_dir_short)

    def set_txtname(self,img1=None,img2=None,gt=None,out=None,viz=None,warp=None):
        img1,img2,gt,out,viz,warp = endcheck('.txt',img1,img2,gt,out,viz,warp)
        if(img1):self.img1_txtname = img1 
        if(img2):self.img2_txtname = img2 
        if(gt):self.groundtruth_txtname = gt 
        if(out):self.outflow_txtname = out 
        if(viz):self.vizflow_txtname = viz 
        if(warp):self.warp_txtname = warp 

    def set_txtsparname(self,plot=None,data=None,best=None,grayres=None,graybest=None,graygt=None):
        plot,data,best,grayres,graybest,graygt=endcheck('.txt',plot,data,best,grayres,graybest,graygt)
        if(data):self.spardata_txtname = data
        if(plot):self.sparplot_txtname = plot
        if(best):self.sparbest_txtname = best
        if(grayres):self.spargrayres_txtname = grayres
        if(graybest):self.spargraybest_txtname = graybest
        if(graygt):self.spargraygt_txtname = graygt

    def set_targetdir(self,targetdir = None,outdir=None,vizdir=None,warpdir=None):
        if(None!=targetdir):
            self.targetdir_short = targetdir
            self.targetdir = join(self.dir,self.targetdir_short)
        if(outdir):self.outflowdir = outdir 
        if(vizdir):self.vizflowdir = vizdir 
        if(warpdir):self.warpdir = warpdir 

    def set_targetname(self,head=None,outend=None,vizend=None,warpend=None):
        vizend,warpend = endcheck('.jpg',vizend,warpend)
        outend = endcheck('.flo',outend)
        if(head):self.head = head 
        if(outend):self.outflowend = outend 
        if(vizend):self.vizflowend = vizend 
        if(warpend):self.warpend = warpend 

    def set_movedir(self,movedir=None,Adir=None,Bdir=None,gtdir=None):
        if(None!=movedir):
            self.movedir_short = movedir
            self.movedir = join(self.dir,self.movedir_short)
        if(Adir):self.Adir = Adir 
        if(Bdir):self.Bdir = Bdir 
        if(gtdir):self.gtdir = gtdir 

    def set_movename(self,head=None,Aend=None,Bend=None,gtend=None):
        if(head):self.mhead = head 
        if(Aend):self.Aend = Aend 
        if(Bend):self.Bend = Bend 
        if(gtend):self.gtend = gtend 

    def set_spar(self,steps=None,style=None):
        if(steps):self.spar_steps = steps 
        if(style):self.spar_style = style

    def set_spardir(self,spardir=None,plotdir=None,datadir=None,bestdir=None,\
                    grayresdir=None,graybestdir=None,graygtdir=None):
        if(None!=spardir):
            self.spar_dir_short = spardir
            self.spar_dir = join(self.dir,self.spar_dir_short)
        if(plotdir):self.spar_plotdir = plotdir
        if(datadir):self.spar_datadir = datadir
        if(bestdir):self.spar_bestdir = bestdir
        if(grayresdir):self.spar_grayresdir = grayresdir
        if(graybestdir):self.spar_graybestdir = graybestdir
        if(graygtdir):self.spar_graygtdir = graygtdir

    def set_sparname(self,head=None,plotend=None,dataend=None,bestend=None,\
                    grayresend=None,graybestend=None,graygtend=None):
        plotend,bestend,grayresend,graybestend,graygtend = \
            endcheck('.jpg',plotend,bestend,grayresend,graybestend,graygtend)
        dataend = endcheck('.txt',dataend)
        if(head):self.spar_head = head 
        if(plotend):self.spar_plotend = plotend
        if(dataend):self.spar_dataend = dataend
        if(bestend):self.spar_bestend = bestend
        if(grayresend):self.spar_grayresend = grayresend
        if(graybestend):self.spar_graybestend = graybestend
        if(graygtend):self.spar_graygtend = graygtend

    def Generatelist(self):
        self.GenerateRandomlist()
        self.GenerateOutVizWarplist()
        self.GenerateSparlist()

    def GenerateRandomlist(self):
        print('saving list..')
        self.save_img1_name = join(self.txt_save_path, self.img1_txtname)
        self.save_img2_name = join(self.txt_save_path, self.img2_txtname)
        self.save_gtflow_name = join(self.txt_save_path, self.groundtruth_txtname)
        save_list(self.save_img1_name,self.imgA)
        save_list(self.save_img2_name,self.imgB)
        save_list(self.save_gtflow_name,self.gtflow)
        print('OUTPUT TXTS: %s,%s,%s IN '%(self.img1_txtname,self.img2_txtname,self.groundtruth_txtname) + \
          ('current folder' if len(self.txt_save_path)==0 else self.txt_save_path))

    def GenerateOutVizWarplist(self):
        self.save_out_name = join(self.txt_save_path,self.outflow_txtname)
        self.save_viz_name = join(self.txt_save_path,self.vizflow_txtname)
        self.save_warp_name = join(self.txt_save_path,self.warp_txtname)
        idlist = list(map(str,range(self.num)))
        outlist = [self.head+x+self.outflowend for x in idlist]
        vizlist = [self.head+x+self.vizflowend for x in idlist]
        warplist = [self.head+x+self.warpend for x in idlist]
        self.outlist = list(map(join,[self.targetdir]*self.num,[self.outflowdir]*self.num,outlist))
        self.vizlist = list(map(join,[self.targetdir]*self.num,[self.vizflowdir]*self.num,vizlist))
        self.warplist = list(map(join,[self.targetdir]*self.num,[self.warpdir]*self.num,warplist))
        # reslist 由PWC-Net生成
        save_list(self.save_out_name,self.outlist)
        save_list(self.save_viz_name,self.vizlist)
        save_list(self.save_warp_name,self.warplist)
        print('OUTPUT TXTS: %s,%s,%s IN '%(self.outflow_txtname,self.vizflow_txtname,self.warp_txtname) + \
          ('current folder' if len(self.txt_save_path)==0 else self.txt_save_path))

    def GenerateSparlist(self):
        self.save_sparplot_name = join(self.txt_save_path,self.sparplot_txtname)
        self.save_spardata_name = join(self.txt_save_path,self.spardata_txtname)
        self.save_sparbest_name = join(self.txt_save_path,self.sparbest_txtname)
        self.save_spargrayres_name = join(self.txt_save_path,self.spargrayres_txtname)
        self.save_spargraybest_name = join(self.txt_save_path,self.spargraybest_txtname)
        self.save_spargraygt_name = join(self.txt_save_path,self.spargraygt_txtname)
        idlist = list(map(str,range(self.num)))
        spar_plotlist = [self.spar_head+x+self.spar_plotend for x in idlist]
        spar_datalist = [self.spar_head+x+self.spar_dataend for x in idlist]
        spar_bestlist = [self.spar_head+x+self.spar_bestend for x in idlist]
        spar_grayreslist = [self.spar_head+x+self.spar_grayresend for x in idlist]
        spar_graybestlist = [self.spar_head+x+self.spar_graybestend for x in idlist]
        spar_graygtlist = [self.spar_head+x+self.spar_graygtend for x in idlist]
        self.spar_plotlist = list(map(join,[self.spar_dir]*self.num,[self.spar_plotdir]*self.num,spar_plotlist))
        self.spar_datalist = list(map(join,[self.spar_dir]*self.num,[self.spar_datadir]*self.num,spar_datalist))
        self.spar_bestlist = list(map(join,[self.spar_dir]*self.num,[self.spar_bestdir]*self.num,spar_bestlist))
        self.spar_grayreslist = list(map(join,[self.spar_dir]*self.num,[self.spar_grayresdir]*self.num,spar_grayreslist))
        self.spar_graybestlist = list(map(join,[self.spar_dir]*self.num,[self.spar_graybestdir]*self.num,spar_graybestlist))
        self.spar_graygtlist = list(map(join,[self.spar_dir]*self.num,[self.spar_graygtdir]*self.num,spar_graygtlist))
        save_list(self.save_sparplot_name,self.spar_plotlist)
        save_list(self.save_spardata_name,self.spar_datalist)
        save_list(self.save_sparbest_name,self.spar_bestlist)
        save_list(self.save_spargrayres_name,self.spar_grayreslist)
        save_list(self.save_spargraybest_name,self.spar_graybestlist)
        save_list(self.save_spargraygt_name,self.spar_graygtlist)
        print('OUTPUT TXTS: %s,%s,%s,%s,%s,%s IN '%\
              (self.sparplot_txtname,self.spardata_txtname,self.sparbest_txtname,
               self.spargrayres_txtname,self.spargraybest_txtname,self.spargraygt_txtname) + \
              ('current folder' if len(self.txt_save_path)==0 else self.txt_save_path))



    def MovePics(self,A=True,B=True,gt=True):
        assert(self.num == len(self.imgA) == len(self.imgB))
        if(gt):assert self.num == len(self.gtflow)
        assert(False == self.isempty)
        print('\nMoving images..')
        if(A):
            for i,item in enumerate(self.imgA):
                source = item
                destination_name = self.mhead + str(i) + self.Aend
                destination_path = join(self.movedir , self.Adir)
                destination = join(destination_path , destination_name)
                r = MovePicsforLinux(source,destination)
                if(r):
                    print('MOVE  ' + item + '  TO  ' + destination + '  SUCCESS!')
                else:
                    print('MOVE  ' + item + '  FAIL!')
        print('')
        if(B):
            for i,item in enumerate(self.imgB):
                source = item
                destination_name = self.mhead + str(i) + self.Bend
                destination_path = join(self.movedir , self.Bdir)
                destination = join(destination_path , destination_name)
                r = MovePicsforLinux(source,destination)
                if(r):
                    print('MOVE  ' + item + '  TO  ' + destination + '  SUCCESS!')
                else:
                    print('MOVE  ' + item + '  FAIL!')
        print('')
        if(gt):
            for i,item in enumerate(self.gtflow):
                source = item
                destination_name = self.mhead + str(i) + self.gtend
                destination_path = join(self.movedir , self.gtdir)
                destination = join(destination_path , destination_name)
                r = MovePicsforLinux(source,destination)
                if(r):
                    print('MOVE  ' + item + '  TO  ' + destination + '  SUCCESS!')
                else:
                    print('MOVE  ' + item + '  FAIL!')
        print('')

    def GenerateSparplots(self):
        flowlist = self.outlist
        gtflowlist = self.gtflow
        self.aepes=[]
        for i,flowname in enumerate(flowlist):
            n,e = splitext(flowname)
            resflowname = n + '_res' + e
            flow = read_gen(flowname)
            resflow = read_gen(resflowname)
            gtflow = read_gen(gtflowlist[i])
            _,_,_,aepe0=self.SparplotSimple(i,flow,resflow,gtflow)
            self.aepes.append(aepe0)
        print("整个数据集抽样平均AEPE: ",np.mean(self.aepes))

    def SparplotSimple(self,ids,netout_flow,uncertainty_flow,groundtruth_flow):

        gt = groundtruth_flow
        res = abs_flow(uncertainty_flow)
        flow = netout_flow
        assert flow.shape==uncertainty_flow.shape==gt.shape
        best = abs_flow(gt - flow)
        total_steps=self.spar_steps

        aepe0=EPE(flow,gt)
        print('AEPE:'+str(aepe0))
        totalpixels=int(flow.size/2)
        remainpixels=np.linspace(totalpixels,0,total_steps,endpoint=False,dtype='int')
        res_sort=res.flatten()
        best_sort=best.flatten()
        res_sort_index=np.argsort(res_sort)
        best_sort_index=np.argsort(best_sort)

        res_aepe=[]
        res_threshold=[]
        for p in remainpixels:
            threshold_id=res_sort_index[p-1]
            threshold=res_sort[threshold_id]
            aepe=EPE_usingmask(flow,gt,res<threshold)
            res_aepe.append(aepe)
            res_threshold.append(threshold)
            print( u"\rFinish"+str(int(len(res_aepe)/total_steps*50))+'%',end = '')

        best_aepe=[]
        best_threshold=[]
        for p in remainpixels:
            threshold_id=best_sort_index[p-1]
            threshold=best_sort[threshold_id]
            aepe=EPE_usingmask(flow,gt,best<threshold)
            best_aepe.append(aepe)
            best_threshold.append(threshold)
            print( u"\rFinish"+str(int(len(best_aepe)/total_steps*50+50))+'%',end = '')

        x=(totalpixels-remainpixels)/totalpixels
        y1=res_aepe/aepe0
        y2=best_aepe/aepe0

        plt.plot(x, y1, mec='r', mfc='w',label='Pred-Merged')
        plt.plot(x, y2, ms=10,label='Oracle')
        plt.legend()  # 让图例生效
        plt.margins(0)
        plt.xlabel('Fraction of Removed Pixels') #X轴标签
        plt.ylabel('Average EPE (Normalized)') #Y轴标签
        plt.title('Sparsification Plots') #标题
        plt.savefig(self.spar_plotlist[ids])
        plt.close() 
        save_3ziplist(self.spar_datalist[ids],zip(x,y1,y2),\
                      'aepe0:'+str(aepe0)+'\nRemoved\tPreAEPE\tOraAEPE\n')
        print('\t\tSave fig, data and imgs !')
        if(self.spar_style=='gray' or self.spar_style=='default'):
            # 1 通道
            absgt=abs_flow(gt)
            imsave(self.spar_grayreslist[ids], res/np.max(res))
            imsave(self.spar_graybestlist[ids], best/np.max(best))
            imsave(self.spar_graygtlist[ids], absgt/np.max(absgt))
        if(self.spar_style=='color' or self.spar_style=='default'):
            # 2通道
            bestflow=Image.fromarray(viz_flow(gt - flow))
            imsave(self.spar_bestlist[ids], bestflow)

        return (remainpixels,res_aepe,best_aepe,aepe0)

    def print_all(self):
        print ('\nArg For EasyTest:')
        print ('\n'.join(['%-30s:%-20s' % item for item in self.__dict__.items() \
                          if item[0] is not 'imgA' and \
                             item[0] is not 'imgB' and \
                             item[0] is not 'gtflow' and \
                             'list' not in item[0]]))
        if('./data/yourdir' == self.dir):print("WANNING: not set dir !!")
        if(True == self.isempty):print("WANNING: Not find any files !!")
        
        print('')



#============================== funtions ========================================

def MovePicsforLinux(source ,destination ):
    if(isfile(source)):
        _,e = splitext(source)
        n,_ = splitext(destination)
        destination = n + e
        subprocess.call(['cp', source, destination])
        if(isfile(source)):
            return True
    return False

def endcheck(end,*arg):
    res=[]
    for item in arg:
        if(item):
            _,e = splitext(item)
            if(e):
                res.append(item)
            else:
                res.append(item+end)
        else:
            res.append(item)
    return res if len(res)>1 else res[0]

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
    print('Saving lists..')
    save_img1_name = join(save_txt_path, "img1.txt")
    save_img2_name = join(save_txt_path, "img2.txt")
    save_gtflow_name = join(save_txt_path, "groundtruth.txt")
    save_list(save_img1_name,res[0])
    save_list(save_img2_name,res[1])
    save_list(save_gtflow_name,res[2])
    print('output img1.txt,img2.txt,groundtruth.txt in ' + \
          'current folder' if len(save_txt_path)==0 else save_txt_path)
    return res


#def Randomlist(list_path,item_num = 10,ltype = 'Sintel',ltype2 = 'clean',lister  = None):
#    datasets_lister = lister
#    if(not datasets_lister):
#        if('Sintel' == ltype):
#            if('clean' == ltype2):
#                print('setting datasets_lister: MpiSintelClean_list ...')
#                datasets_lister = MpiSintelClean_list(list_path)
#            elif('final' == ltype2):
#                print('setting datasets_lister: MpiSintelFinal_list ...')
#                datasets_lister = MpiSintelFinal_list(list_path)
#
#    if(None == datasets_lister):
#        print('Wanning : datasets not found\n')
#        return []
#    if(0 >= item_num or len(datasets_lister) < item_num):
#        item_num = len(datasets_lister)
#
#    img1s=[]
#    img2s=[]
#    gtflows=[]
#    for i in range(item_num):
#        item_id = random.randint(0,len(datasets_lister)-1)
#        group = datasets_lister[item_id]
#        img1s.append(group[0])
#        img2s.append(group[1])
#        gtflows.append(group[2])
#
#    return (img1s,img2s,gtflows)


# =========================== define datasets list ===========================

#class MpiSintel_list(object):
#    def __init__(self, root = '', dstype = 'clean'):
#        self.flow_list = []
#        self.image_list = []
#
#        flow_root = join(root, 'flow')# 文件夹目录
#        image_root = join(root, dstype)
#
#        file_list = sorted(glob(join(flow_root, '*/*.flo')))# flow文件夹下的二级目录的所有flo文件路径列表
#
#        for file in file_list:
#            if 'test' in file:# 如果文件名带有test则跳过
#                continue
#
#            fbase = file[len(flow_root)+1:]# 光流文件相对路径（去掉root路径，加一是为了去掉/）
#            fprefix = fbase[:-8]# 光流文件路径前部分（sintel数据集的文件名格式为frame_0000.flo,这里去掉了0000.flo）
#            fnum = int(fbase[-8:-4])# 光流帧序号（整型）
#
#            # 获得图像对(图像根路径替换光流根路径)
#            img1 = join(image_root, fprefix + "%04d"%(fnum+0) + '.png')
#            img2 = join(image_root, fprefix + "%04d"%(fnum+1) + '.png')
#
#            # 如果出现意外（图像或光流文件不存在）则跳过
#            if not isfile(img1) or not isfile(img2) or not isfile(file):
#                continue
#
#            self.image_list += [[img1, img2]]
#            self.flow_list += [file]
#
#        self.size = len(self.image_list)
#        assert (len(self.image_list) == len(self.flow_list))
#        if(len(self.image_list)<=0):
#            print('='*10 + '\nwanning,MpiSintel_lister not find any files ,please check input dataset path!\n')
#
#    def __getitem__(self, index):
#        index = index % self.size
#        img1 = self.image_list[index][0]
#        img2 = self.image_list[index][1]
#        flow = self.flow_list[index]
#        return (img1,img2,flow)
#
#    def __len__(self):
#        return self.size
#
#
#class MpiSintelClean_list(MpiSintel_list):
#    def __init__(self, root , dstype = 'clean'):
#        super(MpiSintelClean_list, self).__init__(root = root, dstype = dstype)
#
#class MpiSintelFinal_list(MpiSintel_list):
#    def __init__(self, root , dstype = 'final'):
#        super(MpiSintelFinal_list, self).__init__(root = root, dstype = dstype)


