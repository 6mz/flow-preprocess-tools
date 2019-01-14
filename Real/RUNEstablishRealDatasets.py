import copy

from EstablishRealDatasets import NameAnalyzer,_DEFAULT_NameAnalyzer_OPTION
from VideoReader import _DEFAULT_VideoReader_OPTION


# 路径设置
image_dir = 'E:/data/图片预处理/img/20190108/RGB/'
video_dir = 'E:/data/图片预处理/img/20190108/VIDEO/'
out_dir = '../data/Real/test3/'

# 公共参数设置
opts = copy.deepcopy(_DEFAULT_NameAnalyzer_OPTION)
opts['out_style']='split'
opts['split_keep_serial']=True
opts['split_keep_serial_style']= 'underline'
opts['dir_prefix']= 'im'
opts['dir_digits']= 0
opts['file_digits']= 0
opts['auto_rotate']=True

# 图片设置
img_opts = copy.deepcopy(opts)
img_opts['split_start_fileid'] = 50
img_opts['path_in'] = image_dir
img_opts['path_out'] = out_dir
img_opts['img_max_interval']= 3
img_opts['img_min_ele_num']= 3

# 运行图像处理
img_na = NameAnalyzer('img',img_opts)
img_na.Run()

# 视频设置
video_opts= copy.deepcopy(opts)
vr_opts = copy.deepcopy(_DEFAULT_VideoReader_OPTION)
vr_opts['start'] = 0.1
vr_opts['end'] = 0.9
video_opts['path_in'] = video_dir
video_opts['path_out'] = out_dir
video_opts['video_vr_opts'] = vr_opts
video_opts['video_group_num'] = 2
video_opts['video_ele_num'] = 3
video_opts['video_wait'] = False

# 运行视频处理
video_na = NameAnalyzer('video',video_opts)
video_na.ContinueId(img_na)
video_na.Run()
