# -*- coding: utf-8 -*-
import numpy as np

r = range(0, 10)  # x
r2 = range(0, 20)  # y
xs,ys = np.meshgrid(r,r2)
zs = np.ones_like(xs)

fin = np.array([xs.flatten(),ys.flatten(),zs.flatten()])
#.transpose((2, 0, 1))
t = np.sqrt(2)/2
M1 = np.array([
        [t, t, 0],
        [-t, t, 0],
        [0, 0 ,1]])
M2 = np.array([
        [1, 0, 10],
        [0, 1, 20],
        [0, 0 ,1]])
fin1 = np.matmul(M2,fin)
#
resx = (fin1[0, :]/fin1[2, :]).reshape(20,10)
resy = (fin1[1, :]/fin1[2, :]).reshape(20,10)

flowy = resy - ys
##print(t1B)
#t1B = (t1B[0]/t1B[2], t1B[1]/t1B[2])
#print(t1B)
