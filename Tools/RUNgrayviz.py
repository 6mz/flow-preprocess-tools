# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 16:31:24 2018

@author: Administrator
"""
import sys
from os.path import join
from scipy.misc import imsave,imread
from PIL import Image
import numpy as np

sys.path.append("../Server_EasyTest")
from myflowlib import read_gen,abs_flow


path= 'E:\我的文档\任务\配准1\测试图片\展示在文档中的\z3'
name = 'z3res.flo'
save_name ='z3res_gray.jpg'

name = join(path,name)
save_name = join(path,save_name)

res = read_gen(name)
res = abs_flow(res)
imsave(save_name,res/np.max(res))
