# -*- coding: utf-8 -*-
from os.path import *
from glob import glob
from PIL import Image 


def zoom(imagelist,zoom=0.5):
    sImg = Image.open(imagelist[0]) 
    w, h = sImg.size 
    print('first img size:', w, h ,' to ' ,int(w*zoom),int(h*zoom)) 
    print('total %s img'%len(imagelist))
    flag=input('input N to give up')
    if('N' == flag or 'n' == flag):
        return
    for im in imagelist:
        if(isfile(im)):
            print('zoom: '+im)
            sImg = Image.open(im)
            w, h = sImg.size
            dImg = sImg.resize((int(w*zoom), int(h*zoom)), Image.ANTIALIAS)
            dImg.save(im)

if '__main__' == __name__:
    root = '/home/a/public1/flow/data/test/real20181127/pic/'
    scale = 1
    image_list = []

    image_dirs = sorted(glob(join(root, '*')))
    for idir in image_dirs:
        if( not isdir(idir)):continue
        images = sorted( glob(join(idir, '*.jpg')))
        image_list += images

    if(len(image_list)==0):
        print('='*10 + '\nWANNING : Real_lister not find any files ,please check input dataset path!\n')
    else:
        zoom(image_list,scale)
