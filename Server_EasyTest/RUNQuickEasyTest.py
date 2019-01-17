# -*- coding: utf-8 -*-
import os
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


def GenAndSaveWarp(A_list,B_list,flow_list,save_dir):
    ids = [str(id_) for id_ in range(len(A_list))]
    ratios =[]
    for id_,A_name,B_name,F_name in zip(ids,A_list,B_list,flow_list):
        flow = read_gen(F_name)
        A = read_gen(A_name)
        B = read_gen(B_name)
        A_Nwarp,A_Nwarp_mask = WarpNotEasy(A,flow,B)
        ratio = np.sum(A_Nwarp_mask)/A_Nwarp_mask.size
        
        A_Nwarp = A_Nwarp.astype(np.uint8)
        A_Nwarpimg = Image.fromarray(A_Nwarp)
        oname = os.path.join(save_dir,'A_Nwarp'+str(id_)+'.png')
        A_Nwarpimg.save(oname)
        
        A_Nwarp_mask = A_Nwarp_mask.astype(np.uint8)*255
        A_Nwarp_maskimg = Image.fromarray(A_Nwarp_mask)
        oname = os.path.join(save_dir,'A_Nwarp_mask'+str(id_)+'.png')
        A_Nwarp_maskimg.save(oname)

        print(ratio)
        ratios.append(ratio)

    oname = os.path.join(save_dir,'mask_ratios.txt')
    save_list(oname,ratios)


#    A_Nwarp,A_Nwarp_mask = WarpNotEasy(A,flow,B)
if __name__=="__main__":
    source_dir = './data/test1'
    target_dir = './data/test1/maskAndWarp'
    source_list_dir = os.path.join(source_dir,'txts')
    flow_list = read_list(os.path.join(source_list_dir,'outFlow.txt'))
    A_list = read_list(os.path.join(source_list_dir,'imgA.txt'))
    B_list = read_list(os.path.join(source_list_dir,'imgB.txt'))
    GenAndSaveWarp(A_list,B_list,flow_list,target_dir)