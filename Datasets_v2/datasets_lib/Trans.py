# -*- coding: utf-8 -*-
"""

"""
import numpy as np
from Obj import Obj

class Trans(object):
    def __init__(self,objA):
        '''
        '''
        assert(isinstance(objA, Obj))
        self.objA = None
        self.objB = None
        self.flowA = None
        self.flowB = None
        self.flowAmask = None
        self.flowBmask = None
        self.transMatrix = np.zeros((3,3),dtype = np.float)

    def GenTransMatrix(self,type_,trans_opts):
        pass

    def ImposeTransMatrix(self):
        pass
