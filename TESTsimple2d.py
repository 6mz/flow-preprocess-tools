# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:57:14 2018

@author: Administrator
"""

import os.path
import numpy as np
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
 
 
def draw(ids,root=''):
    backsize = np.array([480 ,640])
    rectsize_min =  np.array([50,50])
    rectsize_max =  np.array([200,200])

    backarray = background(backsize)
    rectsize = randrect(rectsize_min,rectsize_max)
    pos1 = randpos(backsize,rectsize)
    pos2 = randpos(backsize,rectsize)
    while(pos1 == pos2 ):
        pos2 = randpos(backsize,rectsize)
    move = sub(pos2,pos1)
    pos1_n = add(pos1,rectsize)
    pos2_n = add(pos2,rectsize)

    image = Image.fromarray(backarray)
    draw = ImageDraw.Draw(image)
    draw.rectangle((pos1[0], pos1[1], pos1_n[0], pos1_n[1]), 'red', 'red')
    image.save(os.path.join(root,'A',str(ids)+'A.jpg'))

    image = Image.fromarray(backarray)
    draw = ImageDraw.Draw(image)
    draw.rectangle((pos2[0], pos2[1], pos2_n[0], pos2_n[1]), 'red', 'red')
    image.save(os.path.join(root,'A',str(ids)+'B.jpg'))
    
    gtflow = background(backsize)
    gtflow[pos1[0]:pos1_n[0], pos1[1]:pos1_n[1],0] = move[0]
    gtflow[pos1[0]:pos1_n[0], pos1[1]:pos1_n[1],1] = move[1]
    
    image = Image.fromarray(gtflow)
    image.save(os.path.join(root,'gt_viz',str(ids)+'gt.jpg'))
    print(pos1,pos1_n,pos2,pos2_n)

def add(a,b):
    return [ai+bi for ai,bi in zip(a,b)]

def sub(a,b):
    return [ai-bi for ai,bi in zip(a,b)]

def randrect(minsize,maxsize):
    assert [0,0]<minsize<maxsize
    return [random.randint(minsize[0],maxsize[0]),random.randint(minsize[1],maxsize[1])]

def randpos(backsize,rectsize):
    assert [0,0]<rectsize<backsize
    minpt = [0,0]
    maxpt = sub(backsize,rectsize)
    return [random.randint(minpt[0],maxpt[0]),random.randint(minpt[1],maxpt[1])]

def background(backsize,color = [0,0,0]):
    array = np.ndarray((backsize[0], backsize[1], 3), np.uint8)
    array[:, :, 0] = color[0]
    array[:, :, 1] = color[1]
    array[:, :, 2] = color[2]
    return array

gtflow=draw(0,root = './data/TESTsimple2d')




#    #绘制直线
#    draw.line((20, 20, 150, 150), 'cyan')
#    #绘制弧
#    draw.arc((100, 200, 300, 400), 0, 180, 'yellow')
#    draw.arc((100, 200, 300, 400), -90, 0, 'green')
# 
#    #绘制弦
#    draw.chord((350, 50, 500, 200), 0, 120, 'khaki', 'orange')
# 
#    #绘制圆饼图
#    draw.pieslice((350, 50, 500, 200), -150, -30, 'pink', 'crimson')
#    
#    #绘制椭圆
#    draw.ellipse((350, 300, 500, 400), 'yellowgreen', 'wheat')
#    #外切矩形为正方形时椭圆即为圆
#    draw.ellipse((550, 50, 600, 100), 'seagreen', 'skyblue') 
# 
#    #绘制多边形
#    draw.polygon((150, 180, 200, 180, 250, 120, 230, 90, 130, 100), 'olive', 'hotpink')
# 
#    #绘制文本
#    font = ImageFont.truetype("consola.ttf", 40, encoding="unic")#设置字体
#    draw.text((100, 50), u'Hello World', 'fuchsia', font)