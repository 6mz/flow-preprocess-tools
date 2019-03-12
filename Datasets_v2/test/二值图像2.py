# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import cv2
import os




img = Image.open('../../data/ds_v2/timg3.jpg')
img = img.resize((256, 256))
im = np.array(img)
immask = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) > 30
imm = Image.fromarray(np.uint8(immask*255))
imm.show()
