# -*- coding: utf-8 -*-
import numpy as np
from copy import deepcopy
class Point(object):
    def __init__(self,x,y=None):
        if(isinstance(x,Point)):
            self.x = x.x
            self.y = x.y
            self.i = x.i
            self.j = x.j
        elif(None == y):
            self.x = x[0]
            self.y = x[1]
            self.i = x[1]
            self.j = x[0]
        else:
            self.x = x
            self.y = y
            self.i = y
            self.j = x
    def __getitem__(self,key):#p[0] or p[1]
        return self.y if key else self.x
    def __add__(self, other):
        x = self.x+other[0]
        y = self.y+other[1]
        return Point(x,y)
    def __radd__(self, other):
        x = other[0] + self.x
        y = other[1] + self.y
        return Point(x,y)
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
        return Point(x,y)
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
    def __call__(self):
        return deepcopy(self)
