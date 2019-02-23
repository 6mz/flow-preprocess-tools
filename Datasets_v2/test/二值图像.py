# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 23:40:55 2019

@author: lmz-pc_2
"""
import matplotlib.pyplot as plt
import numpy as np
import cv2

path = '../../data/datasets/'
sname = '2z.jpg'
name = path + sname

lenna_img = cv2.imread(name)
gray = cv2.cvtColor(lenna_img, cv2.COLOR_RGB2GRAY)  #把输入图像灰度化
ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)

count = 0
for line in binary:
    count += 1
    if not (line == 0).all():
        print(count)
        break



plt.imshow(binary)
plt.axis("off")#去除坐标轴
plt.show()