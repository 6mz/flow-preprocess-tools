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

from NamesManager import NameGenerater,ListsManager
from myflowlib import read_gen,flow_write,save_list,read_list,save_3ziplist
from myflowlib import Sparplot,EPE,EPE_usingmask,abs_flow,viz_flow
from myflowlib import warp_easy,WarpNotEasy
from datasetslib import Randomlist

class EasyTest(object):
    def __init__(self,runDir='./data/NEW DIR'):
        self.runDir = runDir
        self.isempty = True
        self.initListsManagers()
        self.initRunDirs()
        self.initValuesDirs()
        self.initValuesShortNamesExt()
        self.initValuesShortNames()
        self.initSparSetting()

    def initListsManagers(self):
        self.rawData = ListsManager('imgA','imgB','gtFlow')
        self.pics = ListsManager('imgA','imgB')
        self.flows = ListsManager('outFlow','resFlow','bestFlow','gtFlow')
        self.flowVizs = ListsManager(
                'outFlowViz','resFlowViz','bestFlowViz','gtFlowViz')
        self.flowVizsGray = ListsManager(
                'outFlowVizg','resFlowVizg','bestFlowVizg','gtFlowVizg')
        self.warpPics = ListsManager('warp','warpOverlay','warpOverlayUsingMask',
                                     'newWarp','newWarpOverlay',
                                     'newWarpOverlayUsingMask','newWarpMask')
        self.spars = ListsManager('sparData','sparPlot')

    def initRunDirs(self):
        self.rawData.set_runDir(self.runDir)
        self.pics.set_runDir(self.runDir)
        self.flows.set_runDir(self.runDir)
        self.flowVizs.set_runDir(self.runDir)
        self.flowVizsGray.set_runDir(self.runDir)
        self.warpPics.set_runDir(self.runDir)
        self.spars.set_runDir(self.runDir)

    def initTxtNames(self):
        None
        # i.e. 
        #self.flows.set_txtNames(gt="groundtruth",out="out.txt")


    def initTxtDirs(self):
        None

    def initValuesDirs(self):
        self.rawData.set_allValuesDirs('DatasetsPath')#!!
        self.pics.set_allValuesDirs('show')
        self.flows.set_allValuesDirs('flow')
        self.flowVizs.set_allValuesDirs('vizflow')
        self.flowVizsGray.set_allValuesDirs('vizflow_gray')
        self.warpPics.set_allValuesDirs('show')
        self.spars.set_valuesDirs(sparData='spardata',sparPlot='sparplot')

    def initValuesShortNamesExt(self):
        self.rawData.set_allValuesShortNamesExt('.UpToRaw')#!!
        self.pics.set_allValuesShortNamesExt('.UpToRaw')#!!
        self.flows.set_allValuesShortNamesExt('.flo')
        self.flows.set_valuesShortNamesExt(gtFlow = '.UpToRaw')#!!
        self.flowVizs.set_allValuesShortNamesExt('.jpg')
        self.flowVizsGray.set_allValuesShortNamesExt('.jpg')
        self.warpPics.set_allValuesShortNamesExt('.png')
        self.spars.set_valuesShortNamesExt(sparData='.txt',sparPlot='.jpg')

    def initValuesShortNames(self):
        self.rawData.set_valuesShortNames(
                imgA='UpToRaw',imgB = 'UpToRaw',gtFlow = 'UpToRaw')#!!
        self.pics.set_valuesShortNames(
                imgA='A.UpToRaw',imgB = 'B.UpToRaw')#!!
        self.flows.set_valuesShortNames(
                gtFlow = 'f_gt.UpToRaw',outFlow = 'f.flo',
                resFlow = 'f_res.flo',bestFlow = 'f_rbest.flo')
        self.flowVizs.set_valuesShortNames( 
                outFlowViz = 'fviz.jpg',resFlowViz = 'fviz_res.jpg',
                bestFlowViz = 'fviz_rbest.jpg',gtFlowViz = 'fviz_gt.jpg')
        self.flowVizsGray.set_valuesShortNames(
                outFlowVizg = 'fvizg.jpg',resFlowVizg = 'fvizg_res.jpg',
                bestFlowVizg = 'fvizg_rbest.jpg',gtFlowVizg = 'fvizg_gt.jpg')
        self.warpPics.set_valuesShortNames(
                warp = 'A_forward.png',newWarp = 'A_Nforward.png',
                warpOverlay = 'wAB.png',newWarpOverlay = 'wNAB.png',
                warpOverlayUsingMask = 'wAB_UM.png',
                newWarpOverlayUsingMask = 'wNAB_UM.png',
                newWarpMask = 'wNmask.png')
        self.spars.set_valuesShortNames(
                sparData = 'sd.txt' ,sparPlot = 'sp.jpg')

    def initSparSetting(self):
        self.aepes = []
        self.avgAepe = 0
        self.spar_steps = 20

# ================== Genlist ============================

    def GenRandomLists(self,datasets_path,ltype='Sintel',ltype2='clean',num = 10):
        self.GenRawDataFromDatasets(datasets_path = datasets_path,
                                    ltype = ltype,ltype2 = ltype2,num = num)
        self.rawData.set_allExtsAuto()
        self.pics.set_valuesShortNamesExt(
                imgA = self.rawData.get_valuesShortNamesExt('imgA'),
                imgB = self.rawData.get_valuesShortNamesExt('imgB'))
        self.flows.set_valuesShortNamesExt(
                gtFlow = self.rawData.get_valuesShortNamesExt('gtFlow'))
        self.pics.GenAllList(num)
        self.flows.GenList(num,'outFlow','resFlow','gtFlow')
        self.flowVizs.GenList(num,'outFlowViz','resFlowViz','gtFlowViz')
        self.flowVizsGray.GenList(num,'outFlowVizg','resFlowVizg','gtFlowVizg')
        self.warpPics.GenList(num,'warp')

    def GenListsFromTxts(self,num = 10):
        self.ReadRawDataFromTxts(num = num)
        self.rawData.set_allExtsAuto()
        self.pics.set_valuesShortNamesExt(
                imgA = self.rawData.get_valuesShortNamesExt('imgA'),
                imgB = self.rawData.get_valuesShortNamesExt('imgB'))
        self.flows.set_valuesShortNamesExt(
                gtFlow = self.rawData.get_valuesShortNamesExt('gtFlow'))
        self.pics.GenAllList(num)
        self.flows.GenList(num,'outFlow','resFlow','gtFlow')
        self.flowVizs.GenList(num,'outFlowViz','resFlowViz','gtFlowViz')
        self.flowVizsGray.GenList(num,'outFlowVizg','resFlowVizg','gtFlowVizg')
        self.warpPics.GenList(num,'warp')

    def GenRandomLists_Nogt(self,datasets_path,ltype='Sintel',ltype2='clean',num = 10):
        self.GenRawDataFromDatasets_Nogt(datasets_path = datasets_path,
                                    ltype = ltype,ltype2 = ltype2,num = num)
        self.rawData.set_extsAuto('imgA','imgB')
        self.pics.set_valuesShortNamesExt(
                imgA = self.rawData.get_valuesShortNamesExt('imgA'),
                imgB = self.rawData.get_valuesShortNamesExt('imgB'))
        self.pics.GenAllList(num)
        self.flows.GenList(num,'outFlow','resFlow')
        self.flowVizs.GenList(num,'outFlowViz','resFlowViz')
        self.flowVizsGray.GenList(num,'outFlowVizg','resFlowVizg')
        self.warpPics.GenList(num,'warp')

    def GenListsFromTxts_Nogt(self,num = 10):
        self.ReadRawDataFromTxts_Nogt(num = num)
        self.rawData.set_extsAuto('imgA','imgB')
        self.pics.set_valuesShortNamesExt(
                imgA = self.rawData.get_valuesShortNamesExt('imgA'),
                imgB = self.rawData.get_valuesShortNamesExt('imgB'))
        self.pics.GenAllList(num)
        self.flows.GenList(num,'outFlow','resFlow')
        self.flowVizs.GenList(num,'outFlowViz','resFlowViz')
        self.flowVizsGray.GenList(num,'outFlowVizg','resFlowVizg')
        self.warpPics.GenList(num,'warp')

    def GenSparLists(self,num = 10):
        self.flows.GenList(num,'bestFlow')
        self.flowVizs.GenList(num,'bestFlowViz')
        self.flowVizsGray.GenList(num,'bestFlowVizg')
        self.spars.GenAllList(num)

    def SaveLists_stage1(self):
        self.rawData.SaveAlltxts()
        self.flows.Savetxts('outFlow','resFlow')
        self.flowVizs.Savetxts('outFlowViz','resFlowViz','gtFlowViz')
        self.flowVizsGray.Savetxts('outFlowVizg','resFlowVizg','gtFlowVizg')
        self.warpPics.Savetxts('warp')

    def ReadStage1FromTxts(self,num = 10):
        self.flows.Readtxts('outFlow','resFlow')
        self.flowVizs.Readtxts('outFlowViz','resFlowViz','gtFlowViz')
        self.flowVizsGray.Readtxts('outFlowVizg','resFlowVizg','gtFlowVizg')
        self.warpPics.Readtxts('warp')

# ================== Genlist fun ============================

    def GenRawDataFromDatasets(self,datasets_path,ltype='Sintel',ltype2='clean',num = 10):
        self.datasets_path = datasets_path
        self.ltype = ltype
        self.ltype2 = ltype2
        res = Randomlist(datasets_path, num, ltype, ltype2)
        if not res:
            self.isempty = True
            self.datasample_len=0
            self.datasets_len = 0
        else:
            self.isempty = False
            self.rawData.set_value(imgA=res[0] ,imgB=res[1], gtFlow=res[2])
            self.datasample_len=len(self.rawData)
            self.datasets_len = res[3]

    def GenRawDataFromDatasets_Nogt(self,datasets_path,ltype='Sintel',ltype2='clean',num = 10):
        self.datasets_path = datasets_path
        self.ltype = ltype
        self.ltype2 = ltype2
        res = Randomlist(datasets_path, num, ltype, ltype2)
        if not res:
            self.isempty = True
            self.datasample_len=0
            self.datasets_len = 0
        else:
            self.isempty = False
            self.rawData.set_value(imgA=res[0] ,imgB=res[1])
            self.datasample_len=len(self.rawData['imgA'])
            self.datasets_len = res[3]

    def ReadRawDataFromTxts(self,num = 10):
        self.rawData.ReadAlltxts()
        if(len(self.rawData)):
            self.isempty = False
            self.datasample_len=len(self.rawData['imgA'])
            self.datasets_len = self.datasample_len
        else:
            self.isempty = True
            self.datasample_len = 0
            self.datasets_len = 0

    def ReadRawDataFromTxts_Nogt(self,num = 10):
        self.rawData.Readtxts('imgA','imgB')
        if(len(self.rawData)):
            self.isempty = False
            self.datasample_len=len(self.rawData['imgA'])
            self.datasets_len = self.datasample_len
        else:
            self.isempty = True
            self.datasample_len = 0
            self.datasets_len = 0


# ================== other ===========================

    def get_commendTxTNames(self):
        rawDataList = self.rawData.get_SavetxtNamesLists('imgA','imgB')
        flowslist = self.flows.get_SavetxtNamesLists('outFlow')
        flowVizslist = self.flowVizs.get_SavetxtNamesLists('outFlowViz')
        warpPicslist = self.warpPics.get_SavetxtNamesLists('warp')
        return rawDataList + flowslist + flowVizslist + warpPicslist

    def MovePics(self,gt=True):
        imgA_sour = self.rawData['imgA']
        imgB_sour = self.rawData['imgB']
        imgA_dest = self.pics['imgA']
        imgB_dest = self.pics['imgB']
        print(len(imgA_sour),len(imgB_sour),len(imgA_dest),len(imgB_dest))
        source = imgA_sour + imgB_sour
        destination = imgA_dest + imgB_dest
        if(gt):
            gtFlow_sour = self.rawData['gtFlow']
            gtFlow_dest = self.flows['gtFlow']
        assert(len(imgA_sour) == len(imgB_sour) == len(imgA_dest) == len(imgB_dest))
        if(gt):assert len(gtFlow_sour) == len(gtFlow_dest) == len(imgA_sour)
        assert(False == self.isempty)
        print('\nMoving images..')
        for s,d in zip(source,destination):
            r = MovePicsforLinux(s,d)
            if(r):
                print('MOVE  ' + s + '  TO  ' + d + '  SUCCESS!')
            else:
                print('MOVE  ' + s + '  FAIL!')
        print('')
        if(gt):
            for s,d in zip(gtFlow_sour,gtFlow_dest):
                r = MovePicsforLinux(s,d)
                if(r):
                    print('MOVE  ' + s + '  TO  ' + d + '  SUCCESS!')
                else:
                    print('MOVE  ' + s + '  FAIL!')
        print('')

    def VizFlows(self,**dicts):
        for key in dicts:
            if key in self.flows.get_keys():
                print('OUTPUT ' + str(key) + 'vizflow['+dicts[key]+']... ')
                if 'c' == dicts[key] or 'd' == dicts[key]:
                    self.VizColorFlows(key,self.flows[key])
                if 'g' == dicts[key] or 'd' == dicts[key]:
                    self.VizGrayFlows(key,self.flows[key])
            else:
                print('WARRING VizFlows: '+
                      str(key)+' is not in the listdicts')

    def VizColorFlows(self,key,flowList):
        imList = self.flowVizs[key+'Viz']
        assert len(flowList) == len(imList)
        if(len(flowList)==0):print('WARRING VizColorFlows: Not find any flowfiles')
        for flowName,imName in zip(flowList,imList):
            flow = read_gen(flowName)
            flow_viz=Image.fromarray(viz_flow(flow))
            imsave(imName, flow_viz)

    def VizGrayFlows(self,key,flowList):
        imGrayList = self.flowVizsGray[key+'Vizg']
        assert len(flowList) == len(imGrayList)
        if(len(flowList)==0):print('WARRING VizGrayFlows: Not find any flowfiles')
        for flowName,imGrayName in zip(flowList,imGrayList):
            flow = read_gen(flowName)
            flow_g = abs_flow(flow)
            imsave(imGrayName, flow_g/np.max(flow_g))

# =========== warp ==================
#('warp','newWarp','warpOverlay','warpOverlayUsingMask')

    def GenWarp(self,*lists):
        keys = []
        keys_1 = ['nw','nwo','nwom','nwm','w','wo','wom']
        keys_2 = ['newWarp','newWarpOverlay',
                  'newWarpOverlayUsingMask','newWarpMask',
                  'warp','warpOverlay','warpOverlayUsingMask']
        dict_ = dict(zip(keys_1,keys_2))
        keys_3 = ['aw','anw','awww']
        keys_4 = [['warp','warpOverlay','warpOverlayUsingMask'],
                  ['newWarp','newWarpOverlay','newWarpOverlayUsingMask'],
                  ['warpOverlay','warpOverlayUsingMask']]
        dicts = dict(zip(keys_3,keys_4))
        for key in lists:
            if key in self.warpPics.get_keys():
                keys.append(key)
            elif key in dict_:
                keys.append(dict_[key])
            elif key in dicts:
                keys.extend(dicts[key])
            else:
                print('WARRING GenWarp: '+
                      str(key)+' is not in the listdicts')

        print('OUTPUT ',end='')
        Printlist([str(key) for key in keys],end=' , ')
        print(' ...')

        keys =set(keys)

        num = len(self.rawData['imgA'])
        self.warpPics._GenList(num,keys,'nt')
        self.warpPics._Savetxts(keys)
        self._GenWarp(keys)

    def _GenWarp(self,keys):
        flow_list = self.flows['outFlow']
        A_list = self.rawData['imgA']
        B_list = self.rawData['imgB']
        assert len(flow_list)>0
        assert len(flow_list) == len(A_list) == len(B_list)
        for i, F_name, in enumerate(flow_list):
            A_name = A_list[i]
            B_name = B_list[i]
            flow = read_gen(F_name)
            A = read_gen(A_name)
            B = read_gen(B_name)
            if('warp' in keys or 'warpOverlay' in keys or 
               'warpOverlayUsingMask' in keys):
                A_warp = warp_easy(A,flow)
            if('newWarp' in keys or 'newWarpOverlay' in keys or 
               'newWarpOverlayUsingMask' in keys):
                res = WarpNotEasy(A,flow,B)
                if len(res)==2:
                    A_Nwarp,A_Nwarp_mask = res 
                else:
                    A_Nwarp = res
                    A_Nwarp_mask = Mask(A_Nwarp)
            print('\r',str(i),'/',str(len(flow_list)),end='')
            for key in keys:
                O_name = self.warpPics[key][i]
                if('warp' == key):
                    self.Warp(A_warp,B,O_name)
                elif('warpOverlay' == key):
                    self.WarpOverlay(A_warp,B,O_name)
                elif('warpOverlayUsingMask' == key):
                    self.WarpOverlayUsingMask(A_warp,B,O_name,Mask(A_warp))
                elif('newWarp' == key):
                    self.Warp(A_Nwarp,B,O_name)
                elif('newWarpOverlay' == key):
                    self.WarpOverlay(A_Nwarp,B,O_name)
                elif('newWarpOverlayUsingMask' == key):
                    self.WarpOverlayUsingMask(A_Nwarp,B,O_name,A_Nwarp_mask)
                elif('newWarpMask' == key):
                    A_Nwarp_mask_ = A_Nwarp_mask.astype(np.uint8)*255
                    A_Nwarp_mask__ = Image.fromarray(A_Nwarp_mask_)
                    A_Nwarp_mask__.save(O_name)
        print('')


    def Warp(self,A_warp,B,Oname):
        A_warp = A_warp.astype(np.uint8)
        A_warpimg = Image.fromarray(A_warp)
        A_warpimg.save(Oname)

    def WarpOverlay(self,A_warp,B,Oname):
        overlay = A_warp*0.5 + B*0.5
        overlay = overlay.astype(np.uint8)
        overlayimg = Image.fromarray(overlay)
        overlayimg.save(Oname)

    def WarpOverlayUsingMask(self,A_warp,B,Oname,mask):
        A_warp[mask]=B[mask]
        A_warpimg = Image.fromarray(A_warp)
        A_warpimg.save(Oname)



# ========== spar ==============

    def GenerateSparplots(self):
        assert(False == self.isempty)
        flowlist = self.flows['outFlow']
        gtflowlist = self.rawData['gtFlow']
        resflowlist = self.flows['resFlow']
        assert(len(flowlist) == len(gtflowlist) == len(resflowlist))
        for i in range(len(flowlist)):
            flow = read_gen(flowlist[i])
            resflow = read_gen(resflowlist[i])
            gtflow = read_gen(gtflowlist[i])
            _,_,_,aepe0=self.SparplotSimple(i,flow,resflow,gtflow)
            self.aepes.append(aepe0)
        self.avgAepe = np.mean(self.aepes)
        print("整个数据集抽样平均AEPE: ",self.avgAepe)

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

        plt.plot(x, y1, mec='r', mfc='w',label='Our-Net')
        plt.plot(x, y2, ms=10,label='Oracle')
        plt.legend()  # 让图例生效
        plt.margins(0)
        plt.xlabel('Fraction of Removed Pixels') #X轴标签
        plt.ylabel('Average EPE (Normalized)') #Y轴标签
        plt.title('Sparsification Plots') #标题

        plt.savefig(self.spars['sparPlot'][ids])
        plt.close() 
        save_3ziplist(self.spars['sparData'][ids],zip(x,y1,y2),\
                      'aepe0:'+str(aepe0)+'\nRemoved\tPreAEPE\tOraAEPE\n')
        flow_write(self.flows['bestFlow'][ids],gt - flow)
        print('\t\tSave fig, data, imgs and bestFlow!')
        return (remainpixels,res_aepe,best_aepe,aepe0)

# ========== print =============

    def PrintAllInfo(self):
        print('\nEasyTest INFO:')
        self._PrintAll()
        self.rawData.PrintInfo('rawData')
        self.pics.PrintInfo('pics')
        self.flows.PrintInfo('flows')
        self.flowVizs.PrintInfo('flowVizs')
        self.flowVizsGray.PrintInfo('flowVizsGray')
        self.warpPics.PrintInfo('warpPics')
        self.spars.PrintInfo('spars')
        if(self.isempty):print("WANNING: Not find any files !!")

    def _PrintAll(self):
        print ('\n'.join(['%-25s:%-30s' % item for item in self.__dict__.items()]))

    def PrintAll(self):
        print('\nEasyTest INFO:')
        self._PrintAll()
        self.rawData.PrintAll()
        self.pics.PrintAll()
        self.flows.PrintAll()
        self.flowVizs.PrintAll()
        self.flowVizsGray.PrintAll()
        self.warpPics.PrintAll()
        self.spars.PrintAll()

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

def Printlist(lists,end=''):
    for i in lists[:-1]:
        print(i,end=end)
    print(lists[-1],end=' ')

def Mask(im):
    mask = np.sum(im,axis=2) == 0
    masks = np.array([mask,mask,mask]).transpose((1,2,0))
    return masks
