# -*- coding: utf-8 -*-

import numpy as np

def open_flo_file(filename):
	with open(filename, 'rb') as f:
		magic = np.fromfile(f, np.float32, count=1)
		if 202021.25 != magic:
			print('Magic number incorrect. Invalid .flo file')
		else:
			w = np.fromfile(f, np.int32, count=1)
			h = np.fromfile(f, np.int32, count=1)
			data = np.fromfile(f, np.float32, count=2*w[0]*h[0])
			# Reshape data into 3D array (columns, rows, bands)
			return np.resize(data, (h[0], w[0], 2))


def abs_flow(flow):
	u=flow[:,:,0]
	v=flow[:,:,1]
	aflow=np.sqrt(u*u+v*v)
	return aflow


