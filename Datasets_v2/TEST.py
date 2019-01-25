# -*- coding: utf-8 -*-
"""
"""
import mynumpy as m
import numpy as np
from datasets_lib1 import Point, Rect, RectArray, Obj, Trans 
import datasets_func as func


pos = func.RandomPoint([0, 0], [40, 40])
size = func.RandomSize([10, 10], [50, 50])

obj1_rect = Rect(pos, size)
obj1_data = RectArray(obj1_rect, 3)
obj1_data.AddColor([255, 0, 255])
obj1_mask_rect = Rect(pos+size/4, size/2)
obj1_datamask = RectArray(obj1_mask_rect, 1, dtype=np.bool)
obj1_datamask.SetValue(True)

obj1 = Obj(obj1_data, obj1_datamask)

print(obj1)
look = obj1.data.rectArray
