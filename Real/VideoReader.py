# -*- coding: utf-8 -*-
"""
VideoReader.py

Written by Liu Mingzhe

Modifications licensed under the MIT License 

用于从视频中读取图像
"""
import cv2
import matplotlib.pyplot as plt
import copy
import math


_DEFAULT_VideoReader_OPTION = {
        'info':False , # 是否在初始化时输出视频信息
        'start': 'first' , # 开始帧,first默认第一帧 ，也可输入数字，
            # 如果是整数则代表第n帧，
            # 如果是一个大于0小于1的浮点数m，则代表第 floor(m*总帧数) 帧
            # 其他输入情形默认为第0帧
        'end':'last', # 结束帧，last默认最后一帧，也可输入数字，
            # 如果是整数则代表第n帧，
            # 如果是一个大于0小于1的浮点数m，则代表第 ceil(m*总帧数) 帧
            # 其他输入情形默认为第0帧
        'interval': 1 , # 间隔,默认1帧
        'group_ele': 3 , # 一组提取的帧数
        'group_interval': 1  # 组内间隔
        }

class VideoReader(object):
    '''
    主要工作：
        读取视频中的图像帧
    '''
    def __init__(self,videoName,opts = _DEFAULT_VideoReader_OPTION):
        '''
        初始化输入
            videoName:视频名称(包含路径)
            opts:选项，详细见_DEFAULT_VideoReader_OPTION
        '''
        self.cap = cv2.VideoCapture(videoName)  # 打开视频文件
        # 检查路径是否存在
        if self.cap.isOpened():
            self.end = False
        else:
            print('Video File [',videoName ,'] open failed')
            self.end = True
            return None

        self.videoName = videoName
        self.n_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 视频的帧数
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)  # 视频的帧率
        self.dur = self.n_frames/self.fps  # 视频的时间
        self.opts = opts

        self.CheckOpts()
        if self.opts['info']:
            self.Print()

        self.current_frame = self.opts['start']
        self.current_group_frame = self.opts['start']

    def CheckOpts(self):
        '''
        检查opts参数的范围
        '''
        opts = self.opts
        # 检查opts start
        start = opts['start']
        start = 0 if start is 'first' else start
        start = math.floor(self.n_frames * start) \
            if isinstance(start,float) and 0<start<1 else start
        start = min(self.n_frames-1,max(0,start)) \
            if isinstance(start,int) else 0
        opts['start'] = start

        # 检查opts end
        end = opts['end']
        end = self.n_frames if end is 'last' else end
        end = math.ceil(self.n_frames * end) \
            if isinstance(end,float) and 0<end<1 else end
        end = min(self.n_frames,max(start,end)) \
            if isinstance(end,int) else self.n_frames
        opts['end'] = end

        # 检查opts interval
        interval = opts['interval']
        interval = min(self.n_frames-1,max(1,interval)) 
        opts['interval'] = interval
        
        self.opts = opts

    def GetFrame(self,additional_add_frame = 0):
        '''
        相当于拥有自动指针：
        获取视频中的当前帧图像，读取完毕后更新当前帧到下一帧（间距由opts['interval']指定）
        输入：
            additional_add_frame(可选):读取前额外增加的帧数，默认为0，作用于读取之前;
                注意opts['interval']作用于读取之后，且每次调用都会执行;
                一般用于非均匀间隔读取时
        正常输出：
            (指定帧,指定帧图像) 
        异常输出：
            (False,None)：遇到视频结束
        '''
        if self.end:
            return ( False , None )
        self.current_frame += additional_add_frame
        current_frame = self.current_frame 
        self.cap.set(cv2.CAP_PROP_POS_FRAMES , current_frame)
        success,image = self.cap.read()
        if success:
            self.current_frame += self.opts['interval']
            if self.current_frame > self.opts['end']:
                self.end = True
            return ( current_frame , image )
        else:
            self.end = True
            return ( False , None )
        '''
        笔记:
        int cvSetCaptureProperty( CvCapture* capture, int property_id, double value );
        capture 
        视频获取结构。 
        property_id 
        属性标识符。可以是下面之一： 
        CV_CAP_PROP_POS_MSEC - 从文件开始的位置，单位为毫秒 
        CV_CAP_PROP_POS_FRAMES - 单位为帧数的位置（只对视频文件有效） 
        CV_CAP_PROP_POS_AVI_RATIO - 视频文件的相对位置（0 - 影片的开始，1 - 影片的结尾) 
        CV_CAP_PROP_FRAME_WIDTH - 视频流的帧宽度（只对摄像头有效） 
        CV_CAP_PROP_FRAME_HEIGHT - 视频流的帧高度（只对摄像头有效） 
        CV_CAP_PROP_FPS - 帧率（只对摄像头有效） 
        CV_CAP_PROP_FOURCC - 表示codec的四个字符（只对摄像头有效
        上述的“从文件开始的位置，单位为毫秒
        '''

    def GetFrame_n(self,current_frame):
        '''
        指定获取视频中的某帧图像，不受设置中的start和end参数影响
        输入：
            current_frame：指定帧
        正常输出：
            (指定帧,指定帧图像) 
        异常输出：
            (False,None)：遇到视频结束
        '''
        if self.end:
            return ( False , None )
        self.cap.set(cv2.CAP_PROP_POS_FRAMES , current_frame)
        success,image = self.cap.read()
        if success:
            return ( current_frame , image )
        else:
            return ( False , None )

    def GetGroup(self,additional_add_frame = 0):
        '''
        相当于拥有自动指针,与GetFrame的指针不共享
        推荐不要混用两种模式
        获取视频中的当前帧后的一组图像（组内图像间距由opts['group_interval']指定）
        读取完毕后当前帧更新为下一组的开始帧（组间间距由opts['interval']指定,组间间距的定义是两组开头帧直接的差）
        输入：
            additional_add_frame(可选):读取前额外增加的帧数，默认为0，作用于读取之前;
                注意opts['interval']作用于读取之后，且每次调用都会执行;
                一般用于非均匀间隔读取时
        正常输出：
            (当前组开始帧,[当前组图像列表])
        异常输出：
            (False,None): 某一帧遇到视频结束 或 帧序号大于opts['end']
        '''
        self.current_group_frame += additional_add_frame
        current_group_frame = self.current_group_frame 
        c_g_f = current_group_frame
        group_frames = []
        
        for _ in range(self.opts['group_ele']):
            if self.end:
                return ( False , None )
            self.cap.set(cv2.CAP_PROP_POS_FRAMES , current_group_frame)
            success,image = self.cap.read()
            if success:
                group_frames.append(image)
                current_group_frame += self.opts['group_interval']
                if current_group_frame > self.opts['end']:
                    self.end = True
            else:
                self.end = True
                return ( False , None )

        self.current_group_frame = \
            self.current_group_frame + self.opts['interval']
        if self.current_group_frame > self.opts['end']:
            self.end = True
        return ( c_g_f , group_frames )


    def GetGroup_n(self,current_group_frame):
        '''
        指定获取视频中指定帧后的一组图像，不受设置中的start和end参数影响
        输入：
            current_frame：指定帧
        正常输出：
            (当前组开始帧,[当前组图像列表]) 
        异常输出：
            (False,None): 某一帧遇到视频结束 或 帧序号大于opts['end']
        '''
        group_frames = []
        c_g_f = current_group_frame
        for _ in range(self.opts['group_ele']):
            if self.end:
                return ( False , None )
            self.cap.set(cv2.CAP_PROP_POS_FRAMES , current_group_frame)
            success,image = self.cap.read()
            if success:
                group_frames.append(image)
                current_group_frame += self.opts['group_interval']
                if current_group_frame > self.opts['end']:
                    self.end = True
            else:
                self.end = True
                return ( False , None )
        return ( c_g_f , group_frames )


    def AutoSet(self,num = 5):
        '''
        用于在不知道视频的帧数的情形下，给定要采集的数目，自动设置采集的帧（组间）间距，
        采集的帧均匀分布于start帧到end帧之间,同时间距向上取整，因此end帧几乎不可能取到
        输入：
            num：采集数目
        输出：
            无
        '''
        start = self.opts['start']
        end = self.opts['end']
        n_frames = self.n_frames
        assert(n_frames >= end >= start >= 0)
        assert(num > 0)
        interval = (end-start)/num
        if interval < 1:
            print(num,'is too big')
            interval = 1
        self.opts['interval'] = math.ceil(interval)


    def GetAllGroups(self):
        return GetAllGroups(self)

    def GetAllFrames(self):
        return GetAllFrames(self)

    def Print(self):
        '''
        打印相关信息：类配置，视频信息
        '''
        print("opts INFO:")
        [print(f'{opt[0]}:{opt[1]}') for opt in self.opts.items()]
        self.PrintVideoInfo()

    def PrintVideoInfo(self):
        print("\nVideo INFO:")
        print("Duration of the video: {} seconds".format(self.dur))
        print("Number of frames: {}".format(self.n_frames))
        print("Frames per second (FPS): {}".format(self.fps))

def GetAllFrames(VR):
    '''
    根据输入的VideoReader对象设置，一次性获得视频中的所有指定帧，免去了迭代
    输入：
        VR：VideoReader类的对象
    输出：
        列表，存有返回的所有帧
    '''
    res = []
    while(True):
        s,im = VR.GetFrame()
        if im is None:
            break
        print(f'INFO: get Frame:{s}/{VR.n_frames}')
        res.append(im)
    return res

def GetAllGroups(VR):
    '''
    根据输入的VideoReader对象设置，一次性获得视频中的所有指定组，免去了迭代
    输入：
        VR：VideoReader类的对象
    输出：
        列表，包含返回的所有图像组；列表的每个元素都是列表，包含每个组中的几帧图像
    '''
    res = []
    while(True):
        s,ims = VR.GetGroup()
        if ims is None:
            break
        gf = VR.opts['group_interval'] * VR.opts['group_ele']
        print(f"INFO: get Group:{s}/{VR.n_frames}\t{VR.opts['group_ele']}({gf}) frame every group")
        res.append(ims)
    return res




## 测试模块 ###
#opts = copy.deepcopy(_DEFAULT_VideoReader_OPTION)
#opts['start'] = 40
##opts['interval'] = 10
#opts['end'] = 'last'
#opts['info'] = 'True'
#a = VideoReader('../data/Real/test.mp4',opts = opts)
#a.AutoSet(2)
#a.Print()
#res = a.GetAllGroups()
#plt.imshow(res[1][2],cmap='gray')
#plt.show()

