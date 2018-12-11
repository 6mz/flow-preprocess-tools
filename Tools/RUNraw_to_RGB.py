# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
from PIL import Image
from os.path import *
import os
import re
from glob import glob

def ReadCERaw(raw_file,size):
    raw=np.fromfile(raw_file,dtype=np.int16)
    raw=raw.reshape(size)
    raw=np.pad(raw,[(1,1),(1,1)],'reflect')
    row_num=raw.shape[0]
    column_num=raw.shape[1]

    img_b=raw[0:row_num:2,0:column_num:2]
    img_gb=raw[0:row_num:2,1:column_num:2]
    img_gr=raw[1:row_num:2,0:column_num:2]
    img_r=raw[1:row_num:2,1:column_num:2]

    img_bggr=np.stack([img_b,img_gb,img_gr,img_r],axis=-1)
    img_bggr=img_bggr/1023#10位

    return img_bggr

def RawToRGB(raw_file,size):
    img_bggr=ReadCERaw(raw_file,size)
    row = np.shape(img_bggr)[0]
    column = np.shape(img_bggr)[1]
    img_rgb = np.zeros([row,column,3])
    img_rgb[:,:,2]=img_bggr[:,:,0]
    img_rgb[:,:,1]=(img_bggr[:,:,1]+img_bggr[:,:,2])/2
    img_rgb[:,:,0]=img_bggr[:,:,3]
    return img_rgb * 255

def BatchConvert(image_root,image_save):
    imgsize = (2976,3968)
    pattern = re.compile('_SU(.*)_FID')
    image_list = sorted(glob(join(image_root, '*.raw')))
    for i,rawimg in enumerate(image_list[:]):
        pic = RawToRGB(rawimg,imgsize)
        savename = pattern.findall(rawimg)[0][:18]
        pic2X = Image.fromarray((pic.astype(np.uint8)))
        pic2X = pic2X.transpose(Image.ROTATE_270) 
        pic2X.save(join(image_save,'2X',savename+'L.jpg'))
        pic4X = pic2X.resize((int(imgsize[0]/4),int(imgsize[1]/4)), Image.ANTIALIAS)
        pic4X.save(join(image_save,'4X',savename+'S.jpg'))
        print('\r已完成：',str(int(i/(len(image_list)-1)*100)),'%',end='')
    return image_list

def Classify5(image_root,ltype2=''):
    image_root = join(image_root,ltype2)
    image_list = sorted(glob(join(image_root, '*.jpg')))
    if len(image_list)%5 :
        print('文件个数不是5的倍数')
    dirNums = (len(image_list)+4)//5
    for dirid in range(dirNums):
        path = image_root 
        new_path = join(path, str(dirid).zfill(4)) 
        if not os.path.isdir(new_path): 
            os.makedirs(new_path)
        for fileid in range(5):
            nameid = fileid + dirid * 5
            if(nameid>=len(image_list)):
                break
            oldname = image_list[nameid]
            sname = split(oldname)[-1]
            newname = join(new_path,sname)
            os.rename(oldname,newname)#重命名文件，移动文件

if __name__=='__main__':
    image_root='E:/data/图片预处理/img/20181203/RAW/'
    image_save='E:/data/图片预处理/imgFromRaw/20181203/'
    new_path = join(image_save, '2X') 
    if not os.path.isdir(new_path): 
        os.makedirs(new_path)
    new_path = join(image_save, '4X') 
    if not os.path.isdir(new_path): 
        os.makedirs(new_path)
    imglist = BatchConvert(image_root,image_save)
    print('转化列表长度:',len(imglist))
    Classify5(image_save,'4X')
    Classify5(image_save,'2X')
    #name='IMX386DUALHYBIRD_SU20181203_180639949190_FID_006bc0386144250125530130000000000000000000000000000000000000_EI_000012s_16384_ISO_3200_WBOTP_c038_6144_2501_LV_9_id_0.raw'
