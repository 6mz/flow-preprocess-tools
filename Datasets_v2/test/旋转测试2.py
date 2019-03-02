# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PIL import Image
# img = np.ones((50,50,3),dtype=np.uint8)
img = Image.open('./../../data/ds_v1/timg.jpg')
img = img.resize((256, 256))
im = np.array(img)
img = np.uint8(img)
theta = -45/180*np.pi
cx = 128
cy = 128

sin = np.sin(theta)
cos = np.cos(theta)
M1 = np.array([[0.5, 0, 0], [0, 0.5, 0], [0, 0, 1]], dtype=np.float)
M2 = np.array([[cos, sin, 0], [-sin, cos, 0], [0, 0, 1]], dtype=np.float)
M3 = np.array([[cos*0.5, sin, 0], [-sin, cos*0.5, 0], [0, 0, 1]],
              dtype=np.float)
M4 = np.array([[0.5, 0, 10], [0, 0.5, 10], [0, 0, 1]], dtype=np.float)
M5 = np.array([
            [cos, -sin, (1-cos)*cx+sin*cy],
            [sin, cos, (1-cos)*cy-sin*cx],
            [0, 0, 1]])
# m6
x=100
y=100
Acorners = np.float32( [ [0,0],[256,0],[0,256],[256,256] ] ) + np.array([x, y])
xz_theta = 45 / 180 * np.pi  # !!!!!!!!!!!!!!!!!
cos = np.cos(-xz_theta)
sin = np.sin(-xz_theta)
cx = 628 - 500
cy = 628 - 500
# 旋转矩阵
M6 = np.array([
        [cos, -sin, (1-cos)*cx+sin*cy],
        [sin, cos, (1-cos)*cy-sin*cx],
        [0, 0, 1]])
cx = 256+x 
cy = 256+y
M6_ = np.array([
        [cos, -sin, (1-cos)*cx+sin*cy],
        [sin, cos, (1-cos)*cy-sin*cx],
        [0, 0, 1]])
M6_shift = np.array([[1,0,x],
                     [0,1,y],
                     [0,0,1]])
xs = Acorners[:, 0]-x
ys = Acorners[:, 1]-y
zs = np.ones_like(xs)
homoc = np.array([xs, ys, zs])
#homoc = np.matmul(M6_, homoc)
#homoc = np.matmul(np.matmul(M6_shift,M6), homoc)
homoc = np.matmul(M6, homoc)
resx = (homoc[0, :]/homoc[2, :])+x
resy = (homoc[1, :]/homoc[2, :])+y
Bcorners = np.array([resx, resy]).transpose()
print(Acorners, Bcorners)
#print(M6_,np.matmul(M6_shift,M6))

shift = np.array([-53,-53])
Bcorners_shift = Bcorners - shift
M7 = cv2.getPerspectiveTransform(np.float32(Acorners) ,np.float32(Bcorners))
M7_shift = cv2.getPerspectiveTransform(
        np.float32(Bcorners) ,np.float32(Bcorners_shift))
print(M7,M6)



height , width , channels = img.shape
#pts1 = np.float32( [ [0,0],[256,0],[0,256],[256,256] ] )
#pts2 = np.float32( [ [0,0],[800,0],[0,800],[800,800] ] )+10
height , width = np.int32((height*np.sqrt(2), width*np.sqrt(2)))
dst = cv2.warpPerspective( img , np.matmul(M7_shift, M7) , (width, height))
#dst = cv2.warpPerspective( img , M7 , (width, height))
im = Image.fromarray(dst)
im.show()

