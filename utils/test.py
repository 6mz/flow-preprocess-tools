# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 20:03:46 2018

@author: Administrator
"""

class A:
    def __init__(self):
        print('A')
    
    def p(self):
        print('pA')
        

class B:
    def __init__(self):
        print('B')

    def p(self):
        print('pB')

    def p2(self):
        print('p2B')

class C:
    def __init__(self):
        print('C')
    
    def pc(self):
        print('pC')

def fun():
    print('f')