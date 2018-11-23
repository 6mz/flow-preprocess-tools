# -*- coding: utf-8 -*-
from myflowlib import read_gen
from datasetslib import MpiSintelClean_list,GenerateRandomlist,Randomlist


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
root_path='H:\\flow\\data\\Sintel\\training'
#list_table=MpiSintelClean_list(root_path)
#print(id(list_table))
#r1=GenerateRandomlist(root_path,lister = list_table)
Randomlist(root_path,'',num=5)
with open('img1.txt', 'r') as f:
    images1 = [line.strip() for line in f.readlines() if len(line.strip()) > 0]
