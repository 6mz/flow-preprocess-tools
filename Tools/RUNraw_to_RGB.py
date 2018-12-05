# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc


def read_CE_raw(raw_file,size):
	raw=np.fromfile(raw_file,dtype=np.int16)
	raw=raw.reshape(size)
	raw=np.pad(raw,[(1,1),(1,1)],'reflect')
	row_num=raw.shape[0]
	column_num=raw.shape[1]
	
	img_b=raw[0:row_num:2,0:column_num:2]
	img_gb=raw[0:row_num:2,1:column_num:2]
	img_gr=raw[1:row_num:2,0:column_num:2]
	img_r=raw[1:row_num:2,1:column_num:2]
	
	img_bggr=np.stack([img_b,img_gb,img_gr,img_r],axis=-1)
	img_bggr=img_bggr/1023#10位
	
	return img_bggr

def _raw_to_rgb(raw_file,size):
	img_bggr=read_CE_raw(raw_file,size)
	return img_bggr

if __name__=='__main__':
	path='E:/data/img/20181113/RAW/IMG_20181113_221514/'
	name='IMX386DUALHYBIRD_SU20181113_221515304539_FID_006bc0386144250125530130000000000000000000000000000000000000_EI_000033s_849_ISO_165_WBOTP_c038_6144_2501_LV_58_id_0.raw'
	pic=_raw_to_rgb(path+name,(3968,2976))
	misc.imsave('./data/pic.png', pic[:,:,2])
