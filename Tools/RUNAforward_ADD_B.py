
import sys
from os.path import join
from PIL import Image
import numpy as np

sys.path.append("../Server_EasyTest")
from myflowlib import read_gen


path= 'E:\我的文档\任务\配准1\测试图片\展示在文档中的\z3'
Aforward_name = 'z3A_forward.png'
B_name = 'z3B.jpg'
save_name = 'z3_F.jpg'

Aforward_name = join(path,Aforward_name)
B_name = join(path,B_name)
save_name = join(path,save_name)

Af = read_gen(Aforward_name)
B = read_gen(B_name)
save = np.array(Af * 0.5+ B * 0.5)
save = save.astype(np.uint8)
saveimg = Image.fromarray(save)
saveimg.save(save_name)