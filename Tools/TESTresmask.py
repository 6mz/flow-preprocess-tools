# -*- coding: utf-8 -*-
import numpy as np
import sys
from PIL import Image

sys.path.append("../Server_EasyTest")
from myflowlib import read_gen,viz_flow

path= 'E:\\我的文档\\任务\\配准1\\测试图片\\展示在文档中的\\z1\\'
gt_name = 'z1f.flo'
res_name = 'z1res.flo'
A_name = 'z1A.jpg'
B_name = 'z1B.jpg'

gt_name = path + gt_name
A_name =  path + A_name
B_name =  path + B_name
res_name =  path + res_name

gt = read_gen(gt_name)
A = read_gen(A_name)
B = read_gen(B_name)
res = read_gen(res_name)
res = np.sqrt(res[:,:,0]*res[:,:,0]+res[:,:,1]*res[:,:,1])

res = res > 0.14*(np.max(res))
res = res.astype(np.uint8)*255
resimg = Image.fromarray(res)
resimg.save(path+'z1res_mask.png')