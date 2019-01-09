# -*- coding: utf-8 -*-
import cv2
import os

_DEFAULT_NameAnalyzer_OPTION = {
        'height':1440,
        'width':1080,
        'path_in':'RAW DIR',
        'path_out':'TARGET DIR',
        'output_prefix':None
        }

_DEFAULT_VideoReader_OPTION = {
        'info':True , # 是否在初始化时输出视频信息
        'start': 0 , # 开始帧,默认第一帧
        'end':'last', # 结束帧，默认最后一帧
        'interval': 1 , # 间隔,默认1帧
        'group_num': 3 , # 一组提取的帧数
        'group_interval': 1 # 组内间隔
        }


_NAME_FORMAT_LIST = ['img','raw','video']
_DEFAULT_NAME_FORMAT = {
        'img':[]
        }


class NameAnalyzer(object):
    '''
    对文件夹进行分析，提取里面的照片作为数据集
    所有的文件放在同一文件夹下
    '''
    def __init__(self,dirName,dtype='img'):
        assert(dtype in _NAME_FORMAT_LIST)
        self.dtype = dtype
        self.dirName = dirName

class VideoReader(object):
    '''
    读取用于视频
    '''
    def __init__(self,videoName,opts = _DEFAULT_VideoReader_OPTION):
        '''
        初始化输入
            videoName:视频名称(包含路径)
            opts:选项，详细见_DEFAULT_VideoReader_OPTION
        '''
        cap = cv2.VideoCapture(videoName)  # 打开视频文件
        # 检查路径是否存在
        if cap.isOpened():
            self.end = False
        else:
            print('Video File [',videoName ,'] open failed')
            self.end = True
            return None

        self.videoName = videoName
        self.n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 视频的帧数
        self.fps = cap.get(cv2.CAP_PROP_FPS)  # 视频的帧率
        self.dur = self.n_frames/self.fps  # 视频的时间
        self.cap = cap
        
        # 检查opts start合法性
        start = opts['start']
        start = 0 if start == 'first' else start
        start = 0 if start<0 else start
        start = self.n_frames-2 if start > self.n_frames-2 else start
        opts['start'] = start

        # 检查opts end合法性
        end = opts['end']
        end = self.n_frames if end == 'last' else end
        end = 0 if end<0 else end
        end = self.n_frames if end > self.n_frames else end
        opts['end'] = end

        self.opts = opts
        if opts['info']:
            self.Print()

        self.count = 0
        self.current_frame = start

    def GetFrame(self):
        if self.end:
            return None
        self.cap.set(cv2.CAP_PROP_POS_MSEC, self.current_frame)
        success,image = self.cap.read()



    def Print(self):
        print("opts INFO:")
        [print(f'{opt[0]}:{opt[1]}') for opt in self.opts.items()]
        print("\nVideo INFO:")
        print("Duration of the video: {} seconds".format(self.dur))
        print("Number of frames: {}".format(self.n_frames))
        print("Frames per second (FPS): {}".format(self.fps))
