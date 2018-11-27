# -*- coding: utf-8 -*-
# 请在python3下启动本程序

from EasyTest import EasyTest
from myflowlib import save_list
import subprocess
import os 

def ask(something='',flag=0):
    ans=input(something+'\n'+'continue?[y/n]')
    while(not ('y' == ans or 'Y' == ans)):
        if('N' == ans or 'n' == ans):
            if(1 == flag):
                ans=input('quit?[y/n]')
                if('y' == ans or 'Y' == ans):quit(0)
                continue
            else:
                quit(0)
        ans=input('again?[y/n]')
    print('\n')


my_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(my_dir) 

test=EasyTest('/home/a/public1/flow/data/flyingthings3d/',ltype='FlyingThings',ltype2='clean',num=20)

test.set_dir('./data/test_flyingthings3d')
test.set_targetdir(warpdir='show')
test.set_movedir(Adir='show',Bdir='show')
test.print_all()

ask()

test.Generatelist()
args=['python' , './proc_images.py' , test.save_img1_name , test.save_img2_name , \
         test.save_out_name , test.save_viz_name , test.save_warp_name] 
commend = str.join(' ', args)
save_list(os.path.join(test.txt_save_path,'commend.txt'),[commend])
print('OUTPUT TXTS: commend.txt IN ' + test.txt_save_path)

test.MovePics()
test.print_all()

print("由于python3不能调用python2,请在程序挂起期间手动复制%s目录下commend.txt里的内容到python2环境下运行PWC-Net\n " \
      % test.txt_save_path)

ask('是否完成？',flag=1)
test.GenerateSparplots()