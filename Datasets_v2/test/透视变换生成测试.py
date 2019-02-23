# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PIL import Image
# img = np.ones((50,50,3),dtype=np.uint8)
img = cv2.imread('./../../data/timg.jpg')
img = np.uint8(img)
theta = 0.5/np.pi
sin = np.sin(theta)
cos = np.cos(theta)
M1 = np.array([[0.5, 0, 0], [0, 0.5, 0], [0, 0, 1]], dtype=np.float)
M2 = np.array([[cos, sin, 0], [-sin, cos, 0], [0, 0, 1]], dtype=np.float)
M3 = np.array([[cos*0.5, sin, 0], [-sin, cos*0.5, 0], [0, 0, 1]],
              dtype=np.float)
M4 = np.array([[0.5, 0, 10], [0, 0.5, 10], [0, 0, 1]], dtype=np.float)
#dst = cv2.warpPerspective(img, M4, (385, 240))
#im = Image.fromarray(dst)
#im.show()


height , width , channels = img.shape
pts1 = np.float32( [ [0,0],[385,0],[0,240],[385,240] ] )
pts2 = np.float32( [ [0,0],[385,0],[0,240],[385,240] ] )+10
M = cv2.getPerspectiveTransform(pts1 , pts2)
dst = cv2.warpPerspective( img , M , (width , height))
im = Image.fromarray(dst)
im.show()

