# -*- coding: utf-8 -*-
# 请在python3下启动本程序

from datasetslib import EasyTest
from myflowlib import save_list
import subprocess
import os 

def ask(something=''):
    ans=input(something+'\n'+'continue?[y/n]')
    while(not ('y' == ans or 'Y' == ans)):
        if('N == ans' or 'n' == ans):
            quit(0)
        ans=input('again?[y/n]')
    print('\n')


my_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(my_dir) 

test=EasyTest('/home/a/public1/flow/data/Sintel/training/',num=1)
#test.set_targetdir('./data/test1',warpdir='show')
#test.set_movedir(A='show',B='show')
test.set_targetdir('./data/test1',warpdir='show')
test.set_movedir(Adir='show',Bdir='show')
test.print_all()

ask()

test.Generatelist()
args=['python' , './proc_images.py' , test.save_img1_name , test.save_img2_name , \
         test.save_out_name , test.save_viz_name , test.save_warp_name] 
commend = str.join(' ', args)
save_list(os.path.join(test.txt_save_path,'commend.txt'),[commend])
print('OUTPUT TXTS: commend.txt IN ' + test.txt_save_path)
#ask('直接执行网络？')
#subprocess.call(args)
test.MovePics()
test.print_all()
print(" 由于python3不能调用python2,请在程序结束后手动复制%s目录下commend.txt里的内容到命令行运行PWC-Net\n " \
      % test.txt_save_path)