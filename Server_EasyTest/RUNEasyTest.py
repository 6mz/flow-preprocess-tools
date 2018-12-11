# -*- coding: utf-8 -*-
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

def NogtTest(rundir,datasets_path,ltype,ltype2,num):
    et = EasyTest(rundir)
    et.GenRandomLists_Nogt(datasets_path,ltype,ltype2,num)
    et.PrintAllInfo()
    ask()
    et.SaveLists_stage1()
    args=['python' , './proc_images.py' ] + et.get_commendTxTNames()
    commend = str.join(' ', args)
    save_list(os.path.join(et.runDir,'commend.txt'),[commend])
    save_list('commend.txt',[commend])
    print('OUTPUT TXTS: commend.txt IN Current Folder AND ' + et.runDir)
    et.MovePics(gt=False)
    print("由于python3不能调用python2,请在程序挂起期间后到python2环境下执行 commend.py 或 commend.txt 运行PWC-Net\n ")
    ask('是否完成？',flag=1)
    et.VizFlows(outFlow='g',resFlow='g')

def FullTest(rundir,datasets_path,ltype,ltype2,num):
    et = EasyTest(rundir)
    et.GenRandomLists(datasets_path,ltype,ltype2,num)
    et.PrintAllInfo()
    ask()
    et.SaveLists_stage1()
    args=['python' , './proc_images.py' ] + et.get_commendTxTNames()
    commend = str.join(' ', args)
    save_list(os.path.join(et.runDir,'commend.txt'),[commend])
    save_list('commend.txt',[commend])
    print('OUTPUT TXTS: commend.txt IN Current Folder AND ' + et.runDir)
    et.MovePics()
    et.VizFlows(outFlow='g',resFlow='g',gtFlow='d')
    print("由于python3不能调用python2,请在程序挂起期间到python2环境下执行 commend.py 或 commend.txt 运行PWC-Net\n ")
    ask('是否完成？',flag=1)
    et.GenSparLists(num)
    et.GenerateSparplots()
    et.VizFlows(bestFlow='d')
    et.PrintAllInfo()

def FullTest2(rundir,num):
    et = EasyTest(rundir)
    et.ReadDataFromTxts_Nogt(num)
    et.PrintAllInfo()
    ask()
    et.SaveLists_stage1()
    args=['python' , './proc_images.py' ] + et.get_commendTxTNames()
    commend = str.join(' ', args)
    save_list(os.path.join(et.runDir,'commend.txt'),[commend])
    save_list('commend.txt',[commend])
    print('OUTPUT TXTS: commend.txt IN Current Folder AND ' + et.runDir)
    et.MovePics()
    et.VizFlows(outFlow='g',resFlow='g',gtFlow='d')
    print("由于python3不能调用python2,请在程序挂起期间到python2环境下执行 commend.py 或 commend.txt 运行PWC-Net\n ")
    ask('是否完成？',flag=1)
    et.GenSparLists(num)
    et.GenerateSparplots()
    et.VizFlows(bestFlow='d')
    et.PrintAllInfo()

if '__main__' == __name__:
    my_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(my_dir) 
    rundir = './data/real_raw_01'
    datasets_path='/home/a/public1/flow/data/test/real20181211/20181203/4X/'
    ltype = 'Real'
    ltype2 = None
    num = 10

    NogtTest(rundir,datasets_path,ltype,ltype2,num)
    #FullTest(rundir,datasets_path,ltype,ltype2,num)#gt
    #FullTest2(rundir,num)#gt