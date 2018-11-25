# -*- coding: utf-8 -*-
from myflowlib import read_gen,read_list
from datasetslib import MpiSintelClean_list,GenerateRandomlist,Randomlist,GenerateOutVizWarplist
from datasetslib import EasyTest
import subprocess
import os

#  ================   part 1   ==========================
#path= 'E:\\GitProgram\\preprocess-tools\\data\\TEST datasetslib\\'
#flow_name = 'a_frame_0001_forward.flo'
#res_name = 'a_frame_0001_forward_res.flo'
#gt_name = 'flow_frame_0001.flo'
#flow_name = '0014_forward_res.flo'
#jpg_name = '0014_forward.jpg'
#gt_name = 't1gt.pfm'
#A_name = 't1A.png'
#
#flow_name = path + flow_name
#jpg_name = path + jpg_name
#gt_name = path + gt_name
#A_name = path + A_name
#
#flow = read_gen(flow_name)
#jpg = read_gen(jpg_name)
##gt = open_flo_file(gt_name)
#gt = read_gen(gt_name)
#A = read_gen(A_name)

#  ================   part 2   ==========================
#root_path='/home/a/public1/flow/data/Sintel/training'
##list_table=MpiSintelClean_list(root_path)
##print(id(list_table))
##r1=Randomlist(root_path,lister = list_table)
#GenerateRandomlist(root_path,'',num=5)
##GenerateOutVizWarplist('./outdata','',5)
#GenerateOutVizWarplist('./data/test1','',5,vizdir='show',warpdir='show')
#print(len(read_list('img1.txt')))
##with open('img1.txt', 'r') as f:
##    images1 = [line.strip() for line in f.readlines() if len(line.strip()) > 0]
##    print(len(images1))
##
##with open('out.txt', 'r') as f:
##    images1 = [line.strip() for line in f.readlines() if len(line.strip()) > 0]
##    print(len(images1))
#my_dir = os.path.dirname(os.path.realpath(__file__))
#os.chdir(my_dir)    
#subprocess.call(['cp', 'img2.txt', 'img1.txt'])

#  ================   part 3   ==========================
test=EasyTest('E:\\example',ltype2='finall',num=5)
#test.set_txtname('1')
#test.set_txtname(viz='vizssss.txt')
test.GenerateRandomlist()
test.GenerateOutVizWarplist()
test.print_all()