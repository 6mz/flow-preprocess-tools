# -*- coding: utf-8 -*-
import copy

from EstablishRealDatasets import NameAnalyzer,_DEFAULT_NameAnalyzer_OPTION
from VideoReader import _DEFAULT_VideoReader_OPTION


# 路径设置
image_dir = 'E:/data/图片预处理/img/20190108/VIDEO/VIDEO_IMAGE/'
out_dir = '../data/Real/test7/'

# 参数设置帮助见EstablishRealDatasets
# 公共参数设置
opts = copy.deepcopy(_DEFAULT_NameAnalyzer_OPTION)
opts['out_style']='concentrate' 
#opts['split_keep_serial']=True
#opts['split_keep_serial_style']= 'number'
opts['start_id'] = 50
opts['dir_prefix']= ''
opts['dir_digits']= 0
opts['file_digits']= 0
opts['auto_rotate']=True

# 图片设置
img_opts = copy.deepcopy(opts)
img_opts['path_in'] = image_dir
img_opts['path_out'] = out_dir
# img_opts['img_max_interval']= 3
img_opts['img_min_ele_num']= 3
dtype = 'img_from_video'

# 运行图像处理
img_na = NameAnalyzer(dtype,img_opts)
img_na.Run()


