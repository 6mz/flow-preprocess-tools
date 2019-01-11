# -*- coding: utf-8 -*-
import copy
import os
from glob import glob
import re
import datetime
from PIL import Image,ExifTags
import math 
import numpy as np

from VideoReader import _DEFAULT_VideoReader_OPTION,VideoReader,GetAllGroups


_DEFAULT_NameAnalyzer_OPTION = {
        'radio_change':True,
        'height':1440, # 提取的图像高度
        'width':1080, # 提取的图像宽度
        'path_in':'RAW DIR', # 原始文件夹
        'path_out':'TARGET DIR', # 目标文件夹
        'out_style':'group', # 输出格式，在['split','group']中选择一个
        # 对于splite，指定创建n个文件夹(split_n)后把每组图片分置在各个文件夹中
        'split_n':3 , # 必须小于等于下面的img_min_group_num参数
        'split_start_fileid':0 ,# 起始图片编号
        # 对于group ，各组图片存在同一个文件夹中，允许不同的组中的图片数目不同
        'dir_prefix': '' , # 输出文件夹前缀名
        'dir_suffix': '' , # 输出文件夹后缀名
        'dir_digits': 4,     # 输出文件夹编号位数
        'group_start_dirid':0 , # 起始文件夹编号
        'file_prefix': '', # 输出文件前缀名
        'file_suffix': '.jpg', # 输出文件后缀名
        'file_digits': 4,    # 输出文件编号位数
        'img_max_interval': 3, # 判定两张图片为同一组图片的最大间距，单位为秒（s）
        'img_min_group_num': 3, # 一组图像最少的元素数目
        'auto_rotate':False, # 部分手机视频图像需要旋转，在遇到长宽比倒置的情况下会执行旋转操作
        'rotate_angle': 270,
        'processing_type':'zoom' # ['zoom','slice']
        }


_NAME_FORMAT_LIST = ['img','raw','video']
_IMGTYPE_LIST = ['jpg','bmp','png','jpeg','rgb','tif']
_DEFAULT_NAME_FORMAT = {
        'img':{'date':['IMG_\d{8}_',(4,12),'%Y%m%d']  ,
               'time':['_\d{6}\.'  ,(1,7) ,'%H%M%S']} ,#%f微秒
        'raw':[],
        'video':[]
        }


class NameAnalyzer(object):
    '''
    这是一个小工具，用于提高效率，减少重复工作，没有什么算法
    
    本类用于快速将手机或其他设备拍摄完之后的图片、视频、RAW格式图片等文件批量重命名形成数据集
    每个对象只能用于处理一种类型的源文件（图片对、视频、RAW图片对）
    所有的原始文件放在同一文件夹下
    
    本类主要解决的问题是：
        1.由于从手机中复制出来的图像文件是混合的，因此需要根据文件名的拍摄时间来对图像进行分组
        2.拍摄的视频需要转化为图片对
        3.拍摄的RAW图像需要转化为RGB图像
        4.图像的尺寸需要统一，特别是长宽比
    '''
    def __init__(self,dtype = 'img' , opts = _DEFAULT_NameAnalyzer_OPTION):
        '''
        初始化输入
            dtype:源数据格式
            opts:选项，详细见_DEFAULT_NameAnalyzer_OPTION
        '''
        assert(dtype in _NAME_FORMAT_LIST)
        self.dtype = dtype
        self.opts = opts
        self.skip = 0
        self.raw_files = 0
        self.OptCheck()

    def OptCheck(self):
        opts = self.opts
        assert(opts['out_style'] in ['split','group'])
        assert(opts['processing_type'] in ['zoom','slice'])
        assert(opts['img_min_group_num'] >= opts['split_n'])
        assert(opts['path_in'] is not 'RAW DIR')
        assert(opts['path_out'] is not 'TARGET DIR')

    def Run(self):
        '''
        核心函数，实现自动分类
        1.根据文件名中的时间进行分类
        2.对图像尺寸进行切片
        3.创建目标文件夹,保存图片（与2在同一个函数进行）
        '''
        if self.dtype is 'img':
            self.ImgClassify()
        image_groups = self.image_groups
        self.ImgProcessing(image_groups)


    def ImgProcessing(self,image_groups):
        '''
        对图像进行处理、重命名、分类保存
            1.对image_groups中的每个图片进行处理使得符合标准尺寸（标准尺寸在opts中定义）
            2.根据不同的分类类型创建文件夹并保存图像文件
        输入：
            image_groups：已经按时间分完组的列表，列表的每个元素代表一组图像
        输出：
            无
        '''
        # 读取相关参数
        out_style = self.opts['out_style']
        path_out = self.opts['path_out']
        dir_prefix = self.opts['dir_prefix']
        dir_suffix = self.opts['dir_suffix']
        dir_digits = self.opts['dir_digits']
        file_prefix = self.opts['file_prefix']
        file_suffix = self.opts['file_suffix']
        file_digits = self.opts['file_digits']
        s_fileid = self.opts['split_start_fileid']
        s_dirid = self.opts['group_start_dirid']
        # 判断输出文件夹存不存在
        if not os.path.exists(path_out):
            print(f"Dir {path_out} not exists , Create folder...")
            os.makedirs(path_out)
        
        # 如果是分离模式，在循环外创建文件夹
        if(out_style == 'split'):
            print(' out_style : split ')
            split_n = self.opts['split_n']
            
            split_dir_names = []
            for i in range(split_n):
                ids = str(i).zfill(dir_digits)
                dir_name = dir_prefix + ids + dir_suffix
                dir_name = os.path.join(path_out,dir_name)
                if not os.path.exists(dir_name):
                    print(f"Dir {dir_name} not exists , Create folder...")
                    os.makedirs(dir_name)
                split_dir_names.append(dir_name)
        else:
            print(' out_style : group ')

        count = 0
        for gi,group in enumerate(image_groups):
            if(out_style == 'group'):
                # 组模式，给每个组创建文件夹
                ids = str( gi + s_dirid ).zfill(dir_digits)
                dir_name = dir_prefix + ids + dir_suffix
                dir_name = os.path.join(path_out,dir_name)
                if not os.path.exists(dir_name):
                    print(f"Dir {dir_name} not exists , Create folder...")
                    os.makedirs(dir_name)
            # 读取、处理图像
            for gj,img_name in enumerate(group):
                #如果是分离模式，一组图片数量超过上限就应停止
                if(out_style == 'split' and gj >= split_n):
                    print('skip img')
                    self.skip += 1
                    continue
                count += 1
                print('ImgProcessing ',count,'/',self.raw_files-self.skip)
                img = Image.open(img_name)
                # 通过ExifTags标志判断是否需要旋转
                img = OrientationCorrection(img)
                img = self.Processing(img)
                
                #命名
                if(out_style == 'group'):
                    # 使用内层编号
                    ids = str( gj ).zfill(file_digits)
                    file_name = file_prefix + ids + file_suffix
                    # 直接使用外层循环创建的文件夹名称
                    file_name = os.path.join(dir_name,file_name)
                else:
                    # 使用外层编号
                    ids = str( gi + s_fileid ).zfill(file_digits)
                    file_name = file_prefix + ids + file_suffix
                    file_name = os.path.join(split_dir_names[gj],file_name)
                
                print(file_name)
                img.save(file_name)



    def Processing(self,im):
        '''
        对图像进行旋转缩放切片操作使得符合标准尺寸(标准尺寸在opts中定义)
        思路是：
            1.判断是否需要旋转
                只针对视频使用，图片通过ExifTags标志判断是否需要旋转
            2.进行缩放，使缩放后的图像的能覆盖目标尺寸的图像,即
              w>=tw,h>=th
            3.进行切片,切除长边
        输入：
            im：图像，类型是Image
        输出：
            img：处理完后的图像，类型是Image
        '''
        th = self.opts['height']
        tw = self.opts['width']
        auto_rotate = self.opts['auto_rotate']
        rotate_angle = self.opts['rotate_angle']
        processing_type = self.opts['processing_type']

        target_hw_ratio = th / tw
        w, h = im.size 
        hw_ratio = h / w
        ## step1. 在遇到长宽比倒置的情况下会执行旋转操作
        flag = ((hw_ratio > 1 and target_hw_ratio < 1)or
                (hw_ratio < 1 and target_hw_ratio > 1))
        if(auto_rotate and flag):
            print('rotate',hw_ratio,' ',target_hw_ratio)
            img = im.rotate(rotate_angle,expand = True)
            w, h = img.size
        else:
            img = im
        ## step2. 进行缩放，使缩放后的图像的能覆盖目标尺寸的图像
        if(w == tw and h == th):
            # 特殊情况直接返回
            return img
        if(w == tw and h > th):
            # 直接切片情形
            hs = int((h - th) /2)
            box=(0,hs,tw,hs+th) 
            return img.crop(box)
        if(h == th and w > tw):
            ws = int((w - tw) /2)
            box=(ws,0,ws+tw,th) 
            return img.crop(box)
        # 计算放大率
        rw = w / tw
        rh = h / th
        if(rh < 1 or rw < 1):
            r = max(rw,rh)
        if(rh > 1 and rw > 1):
            if(processing_type == 'slice'):
                # 切片模式不缩小
                r = 1
            else:
                r = min(rw,rh)
        #缩放
        img = img.resize((math.ceil(w / r), math.ceil(h / r)), Image.ANTIALIAS)
        w, h = img.size
        hs = int((h - th) /2)
        ws = int((w - tw) /2)
        box=(ws,hs,ws+tw,hs+th) 
        return img.crop(box)

    def ImgClassify(self):
        '''
        对img进行分类
        1.获得文件夹中的所有【图像】文件,图像的后缀名列表在文件开头定义
        2.获取文件名中的时间,按时间进行分组,判断组内图像数目是否符合要求
        输入：
            无
        输出：
            image_groups：已经按时间分完组的列表，列表的每个元素代表一组图像
        '''
        ## step1.获得文件夹中的所有图像文件
        img_dir = self.opts['path_in']
        if not os.path.exists(img_dir):
            print(f'Dir [{img_dir}] not exist')
            return False
        self.image_list = sorted(glob(os.path.join(img_dir, '*')))
        self.raw_files = len(self.image_list)
        # 判断是不是图像格式
        for item in self.image_list:
            _,ext = os.path.splitext(item)
            if(ext[1:] not in _IMGTYPE_LIST):
                self.skip += 1
                self.image_list.remove(item)
        ## step2.获取文件名中的时间，按时间进行分组，判断组内图像数目是否符合要求
        image_groups = []
        group = []
        last_item_dt = datetime.datetime.strptime('10000101000000','%Y%m%d%H%M%S')
        for item in self.image_list:
            date_time = self.GetTimeFromName(item)
            if(False == date_time):
                #如果文件名不符合则跳过
                self.skip += 1
                continue
            # 计算时间差
            ddt = abs((date_time-last_item_dt).total_seconds())
            last_item_dt = date_time
            if ddt < self.opts['img_max_interval']:
                group.append(item)
            else:
                # 判断组内图像数目是否符合要求
                if(len(group) >= self.opts['img_min_group_num']):
                    image_groups.append(group)
                group = [item]

        self.image_groups = image_groups
        return image_groups

    def GetTimeFromName(self,name):
        '''
        利用正则表达式从文件名中获得文件的时间
        表达式的表述在_DEFAULT_NAME_FORMAT中定义
        文件一般指手机中拍摄得到的文件
        
        输入：
            name：文件名
        输出：
            date_time: datetime类，包含日期和时间
        异常输出：
            如果遇到文件名中没有匹配的字段，则返回False
        '''
        # 获取类型，名称格式用于正则匹配
        dtype = self.dtype
        name_format = _DEFAULT_NAME_FORMAT[dtype]
        date_format = name_format['date']
        time_format = name_format['time']
        # 创建匹配器
        pattern_date = re.compile(date_format[0])
        pattern_time = re.compile(time_format[0])
        # 分离文件名
        _, name = os.path.split(name)
        # 进行匹配，提取有效部分
        date = pattern_date.findall(name)
        if len(date) == 0:
            return False
        else:
            date=date[0]
        date = date[date_format[1][0] : date_format[1][1]]

        time = pattern_time.findall(name)
        if len(time) == 0:
            return False
        else:
            time=time[0]
        time = time[time_format[1][0] : time_format[1][1]]
        date_time = datetime.datetime.strptime(date+time,date_format[2]+time_format[2])
        return date_time

def OrientationCorrection(img):
    '''
    利用PIL读取exif中的orientation信息，
    然后根据这个信息将图片转正后，再进行后续操作
    
    Ref：https://blog.csdn.net/mizhenpeng/article/details/82794112
    '''
    for orientation in ExifTags.TAGS.keys() : 
        if ExifTags.TAGS[orientation]=='Orientation' : break 
    exif=dict(img._getexif().items())
    if   exif[orientation] == 3 : 
        img=img.rotate(180, expand = True)
    elif exif[orientation] == 6 : 
        img=img.rotate(270, expand = True)
    elif exif[orientation] == 8 : 
        img=img.rotate(90, expand = True)
    return img



### 测试 ###
opts = copy.deepcopy(_DEFAULT_NameAnalyzer_OPTION)
opts['path_in']='E:/data/图片预处理/img/20190108/RGB/'
opts['path_out']='../data/Real/test1/'
opts['out_style']='split'
opts['dir_prefix']= 'im'
opts['dir_digits']= 0
opts['file_digits']= 0
#opts['auto_rotate']=True

a = NameAnalyzer('img',opts)
a.Run()
image_groups = a.image_groups
#a.ImgProcessing(image_groups[3:6])
#img = Image.open(image_groups[9][2])
#img = OrientationCorrection(img)
#d=np.array(img)
#c=a.Processing(img)
#c.save('E:/data/图片预处理/img/20190108/RGB/test1.jpg')
