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

from myflowlib import viz_flow,flow_write,flow_read,viz_flow_fromfile

def draw_rect(ids,root=''):
    backsize = np.array([640 ,480])#(x,y)
    rectsize_min =  np.array([50,50])#(x,y)
    rectsize_max =  np.array([200,200])#(x,y)

    backarray = background(backsize)
    rectsize = randrectsize(rectsize_min,rectsize_max)
    pos1 = randpos(backsize,rectsize)
    pos2 = randpos(backsize,rectsize)
    while(pos1 == pos2):
        pos2 = randpos(backsize,rectsize)
    move = pos2 - pos1
    pos1_n = pos1 + rectsize
    pos2_n = pos2 + rectsize

    image = Image.fromarray(backarray)
    draw = ImageDraw.Draw(image)
    draw.rectangle((pos1.x, pos1.y, pos1_n.x, pos1_n.y), 'red', 'red')
    image.save(os.path.join(root,'A',str(ids)+'A.jpg'))

    image = Image.fromarray(backarray)
    draw = ImageDraw.Draw(image)
    draw.rectangle((pos2.x, pos2.y, pos2_n.x, pos2_n.y), 'red', 'red')
    image.save(os.path.join(root,'B',str(ids)+'B.jpg'))

    gtflow = np.zeros((backsize[1],backsize[0],2),dtype='float')
    gtflow[pos1.i:pos1_n.i, pos1.j:pos1_n.j, 0] = move[0]
    gtflow[pos1.i:pos1_n.i, pos1.j:pos1_n.j, 1] = move[1]
    flow_write(os.path.join(root,'gt',str(ids)+'gt.flo'),gtflow)
#    image = Image.fromarray(viz_flow(gtflow))
#    image.save(os.path.join(root,'gt_viz',str(ids)+'gt.jpg'))

#    print(move)
#    flow = flow_read(os.path.join(root,'gt',str(ids)+'gt.flow'))
#    image = Image.fromarray(viz_flow_fromfile(flow))
#    image.save(os.path.join(root,'gt_viz',str(ids)+'gt_fromfile.jpg'))
#    return flow



def randrectsize(minsize,maxsize):
    assert True == (minsize < maxsize).all()
    return np.array([random.randint(minsize[0],maxsize[0]),random.randint(minsize[1],maxsize[1])])

def randpos(backsize,rectsize):
    assert True == (rectsize < backsize).all()
    minpt = np.array([0,0])
    maxpt = backsize - rectsize
    return point(random.randint(minpt[0],maxpt[0]),random.randint(minpt[1],maxpt[1]))

def background(backsize,color = [255,255,0]):
    # x,y -> i,j
    array = np.zeros((backsize[1], backsize[0], 3), np.uint8)
    array[:, :, 0] = color[0]
    array[:, :, 1] = color[1]
    array[:, :, 2] = color[2]
    return array

class point(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.i = y
        self.j = x
    def __getitem__(self,key):
        return self.y if key else self.x
    def __add__(self, other):
        x = self.x+other[0]
        y = self.y+other[1]
        return point(x,y)
    def __radd__(self, other):
        x = other[0] + self.x
        y = other[1] + self.y
        return point(x,y)
    def __sub__(self,other):
        x = self.x-other[0]
        y = self.y-other[1]
        return np.array([x,y])
    def __rsub__(self, other):
        x = other[0] - self.x
        y = other[1] - self.y
        return np.array([x,y])
    def __mul__(self, num):
        x = self.x * num
        y = self.y * num
        return point(x,y)
    def __str__(self):
        return ' x:%s,y:%s '%(self.x,self.y)
    def __repr__(self):
        return str((self.x,self.y))
    def __eq__(self,other):
        return self.x == other.x and self.y == other.y
    def __lt__(self,other):
        return self.x < other.x and self.y < other.y
    def __gt__(self,other):
        return self.x > other.x and self.y > other.y

if '__main__' == __name__:
    for i in range(0,1):
        gtflow=draw_rect(i,root = './data')#'./data/TESTsimple2d/rect')




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