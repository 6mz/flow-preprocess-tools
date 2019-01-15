# -*- coding: utf-8 -*-
import copy
import sys
from EstablishRealDatasets import NameAnalyzer,_DEFAULT_NameAnalyzer_OPTION
from VideoReader import _DEFAULT_VideoReader_OPTION


# 路径设置
image_dir = './source/'
video_dir = './source/'
out_dir = './target/'
start_id = int(sys.argv[1]) if len(sys.argv)>= 2 else 0

# 参数设置帮助见EstablishRealDatasets
# 公共参数设置
opts = copy.deepcopy(_DEFAULT_NameAnalyzer_OPTION)
opts['height']= 1440
opts['width']= 1080
opts['out_style']='concentrate' # 输出形式
opts['start_id'] = start_id # 输出组的开始id
opts['dir_prefix']= ''
opts['dir_digits']= 0
opts['file_digits']= 0
opts['auto_rotate']=True

# 图片设置
img_opts = copy.deepcopy(opts)
img_opts['path_in'] = image_dir
img_opts['path_out'] = out_dir
img_opts['img_max_interval']= 3 # 两张3s以内的图片被认为是同一组
img_opts['img_min_ele_num']= 3 # 一组图片最少几张

# 运行图像处理
img_na = NameAnalyzer('img',img_opts)
img_na.Run()

# 视频设置
video_opts= copy.deepcopy(opts)
vr_opts = copy.deepcopy(_DEFAULT_VideoReader_OPTION)
vr_opts['start'] = 0.05 # 有效区间从5%处开始
vr_opts['end'] = 0.95 # 有效区间到95%处结束
video_opts['video_vr_opts'] = vr_opts
video_opts['path_in'] = video_dir
video_opts['path_out'] = out_dir
video_opts['video_group_num'] = 2 # 一个视频出几组
video_opts['video_ele_num'] = 3 # 一组几帧
video_opts['video_wait'] = False

# 运行视频处理
video_na = NameAnalyzer('video',video_opts)
video_na.ContinueId(img_na)
video_na.Run()


