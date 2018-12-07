
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

def FullTest(datasets_path,ltype,ltype2,num,dirs):
    test=EasyTest(datasets_path,ltype=ltype,ltype2=ltype2,num=num)
    test.set_dir(dirs)
    test.set_targetdir(warpdir='show')
    test.set_movedir(Adir='show',Bdir='show')
    test.print_all()
    
    ask()
    
    test.Generatelist()
    args=['python' , './proc_images.py' , test.save_img1_name , test.save_img2_name , \
             test.save_out_name , test.save_viz_name , test.save_warp_name] 
    commend = str.join(' ', args)
    save_list(os.path.join(test.txt_save_path,'commend.txt'),[commend])
    save_list('commend.txt',[commend])
    print('OUTPUT TXTS: commend.txt IN Current Folder AND ' + test.txt_save_path)
    
    test.MovePics()
    test.print_all()
    
    print("由于python3不能调用python2,请在程序挂起期间到python2环境下执行 commend.py 或 commend.txt 运行PWC-Net\n ")
    
    ask('是否完成？',flag=1)
    test.GenerateSparplots()


def NogtTest(datasets_path,ltype,ltype2,num,dirs):
    test=EasyTest(datasets_path,ltype=ltype,ltype2=ltype2,num=num)
    test.set_dir(dirs)
    #test.set_txtpath('./txts',in_dir = False)
    test.set_targetdir(warpdir='show')
    test.set_movedir(Adir='show',Bdir='show')
    test.print_all()
    
    ask()
    
    test.Generatelist(gen_spar=False)
    args=['python' , './proc_images.py' , test.save_img1_name , test.save_img2_name , \
             test.save_out_name , test.save_viz_name , test.save_warp_name] 
    commend = str.join(' ', args)
    save_list(os.path.join(test.txt_save_path,'commend.txt'),[commend])
    save_list('commend.txt',[commend])
    print('OUTPUT TXTS: commend.txt IN Current Folder AND ' + test.txt_save_path)
    
    test.MovePics(gt=False) 
    test.print_all()
    print('INFO : No Groundtruth')

    print("由于python3不能调用python2,请在程序结束后到python2环境下执行commend.py 或 commend.txt 运行PWC-Net\n ")



if '__main__' == __name__:
    my_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(my_dir) 

    datasets_path='/home/a/public1/flow/data/Simple2d/'
    ltype = 'Simple2d'
    ltype2 = 'rect'
    num = 50
    dirs = './data/test_simple2d_rect'

    #NogtTest(datasets_path,ltype,ltype2,num,dirs)
    FullTest(datasets_path,ltype,ltype2,num,dirs)#gt
