# -*- coding: utf-8 -*-
import numpy as np
from scipy import misc
from myflowlib import open_flo_file,abs_flow

path='./data/flow_file/'
name='5_res.jpg_res.flo'
flow=open_flo_file(path+name)
flow=abs_flow(flow)
misc.imsave(path+name+'.png', flow)
