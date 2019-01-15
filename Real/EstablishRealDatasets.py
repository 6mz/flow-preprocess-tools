# -*- coding: utf-8 -*-
"""
EstablishRealDatasets.py

Written by Liu Mingzhe

Licensed under the MIT License (see LICENSE for details)

把手机拍摄的图片自动分组、变换旋转尺寸、重命名、整理成测试数据集，
把手机拍摄的视频自动读取、变换旋转尺寸、分组、重命名、整理成测试数据集

"""


import copy
import os
from glob import glob
import re
import datetime
from PIL import Image,ExifTags
import math 
import numpy as np

from VideoReader import _DEFAULT_VideoReader_OPTION,VideoReader


_DEFAULT_NameAnalyzer_OPTION = {
        # 输出图像期望尺寸设置
        'height':1440, # 提取的图像高度
        'width':1080, # 提取的图像宽度
        # 输入输出路径设置
        'path_in':'RAW DIR', # 源文件夹
        'path_out':'TARGET DIR', # 目标文件夹
        # 输出分组策略设置
        'out_style':'concentrate', # 输出分组策略，在['split','group','concentrate']中选择一个
            # 对于 'split'，指定创建n个文件夹(split_n)后把每组图片相同序号的图片放在同一个文件夹中
            # 下方的 split_n 参数用于设置文件夹数目，某组超过这个数目的其他图片会被舍弃，想保留请先人工筛选
                # 如对于两组图片： g1_1,g1_2 ;g2_1,g2_2,g2_3
                # 分类成 folder1:[g1_1,g2_1] ,folder2:[g1_2,g2_2],舍弃g2_3
                # 注意保存后将重命名
            # 对于 'group' ，同组图片存在同一个文件夹中，允许不同文件夹中的图片数目不同
                # 如对于两组图片： g1_1,g1_2 ;g2_1,g2_2,g2_3
                # 分类成 folder1:[g1_1,g1_2] ,folder2:[g2_1,g2_2,g2_3],保留g2_3
                # 注意保存后将重命名
            # 对于 'concentrate' ，保存在同一个文件夹中，不再创建子文件夹，
                # 因此重命名的时候自动带有组号和序列号,
                # 编号的组位数由dir_digits确定，序列号位数由file_digits确定
        # 对于split 模式下的设置
        'split_n':3 , # 设置文件夹数目，
            # 必须小于等于下面的img_min_ele_num参数(img模式) 或
            # 必须小于等于下面的video_ele_num参数(video模式)
        'split_keep_serial':False, # 是否保留图像文件的序列号，
            # 如果不保留只能通过文件夹名称来判断图像在序列中的编号
        'split_keep_serial_style':'number', # 序列号的格式,默认使用数字
            # 在['number','underline']中选择
            #            文件夹1     文件夹2     文件夹3
            # 不使用:     g1.jpg ,   g1.jpg ,   g1.jpg
            # number:  g1_0.jpg , g1_1.jpg , g1_2.jpg
            # underline: g1.jpg ,  g1_.jpg , g1__.jpg
        # 文件和文件夹名称设置
        'start_id':0 , #起始图片组编号,默认是0,一般用于扩展数据集
        'dir_prefix': '' , # 输出文件夹前缀名
        'dir_suffix': '' , # 输出文件夹后缀名
        'dir_digits': 0,   # 输出文件夹编号位数
        'file_prefix': '', # 输出文件前缀名
        'file_suffix': '.jpg', # 输出文件后缀名（包含系统意义上的后缀名）
        'file_digits': 0,    # 输出文件编号位数
        # 图像处理设置
        'auto_rotate':False, # 部分手机视频图像需要旋转，在遇到长宽比倒置的情况下会执行旋转操作
        'rotate_angle': 270, # 和auto_rotate一起设置，定义旋转的角度
        'processing_type':'zoom', # 切片策略，在['zoom','slice']中选择一个
            # 'zoom' 表示如果原图的尺寸大于期望尺寸，则先进行缩放到接近期望尺寸后再切片，尽可能保留多的内容
            # 'slice' 表示如果原图的尺寸大于期望尺寸，直接在中心进行切片，大小为期望尺寸
        ## =========================================
        # 输入格式为 直接拍摄图像 的设置（dtype=='img'）
        'img_max_interval': 3, # 判定两张图片为同一组图片的最大间距，单位为秒（s）
        'img_min_ele_num': 3, # 一组图像最少的元素数目
        # 输入格式为 视频 的设置（dtype=='video'）
        'video_vr_opts': _DEFAULT_VideoReader_OPTION, 
            # 视频读取器参数，详细见_DEFAULT_VideoReader_OPTION
            # 'info':False , # 是否在初始化时输出视频信息
            # 'start': 'first' , # 开始帧,first默认第一帧 ，也可输入数字，
            #    # 如果是整数则代表第n帧，
            #    # 如果是一个大于0小于1的浮点数m，则代表第 floor(m*总帧数) 帧
            #    # 其他输入情形默认为第0帧
            # 'end':'last', # 结束帧，last默认最后一帧，也可输入数字，
            #    # 如果是整数则代表第n帧，
            #    # 如果是一个大于0小于1的浮点数m，则代表第 ceil(m*总帧数) 帧
            #    # 其他输入情形默认为第0帧
            # 'interval': 1 , # (组间)间隔,默认1帧
            #    # 在这里，间隔一般由video_group_num计算得到，除非将其设置为0
            # 'group_ele': 3 , # 一组提取的帧数
            # 'group_interval': 1  # 组内间隔
        'video_group_num': 2, # 从每个视频中提取多少组图像;如果设置为零则不使用此参数，改用
            # video_vr_opts中的interval参数（即帧间间隔）来读取
        'video_ele_num': 3, # 一组提取的帧数,会覆盖video_vr_opts中的group_ele参数
        'video_image_dir':'default',  # 存放从视频中读取的图片的目录，
            # 默认情况下在opts['path_in'] 下的 VIDEO_IMAGE 文件夹中
        'video_image_ext':'.jpg', # 从视频中提取的临时图片的后缀名，
            # 注意，最终文件的后缀名由file_suffix决定
        'video_wait':False, # 在读取完视频之后是否暂停，供手动选择图片
        }


# 定义图像后缀名，img模式下，后缀名不在列表中的文件都会被忽略
_IMGTYPE_LIST = ['jpg','bmp','png','jpeg','rgb','tif']
# 定义视频后缀名，video模式下，后缀名不在列表中的文件都会被忽略
_VIDTYPE_LIST = ['mp4',]
# 原始输入类型列表
# img:输入的是直接拍摄的序列图像
# raw：输入的是raw格式（纯数据矩阵）图像
# video：输入的是视频
_NAME_FORMAT_LIST = ['img','raw','video','img_group','img_from_video']
# 定义从文件名中读取时间的方式
    # date表示日期,time表示时间;后面的列表中的
    # 第一项表示正则表达式的提取规则，
    # 第二项表示提取后的字符串中有效字段的起始结束位置
    # 第三项表示datatime类读取有效字段时的格式
_DEFAULT_NAME_FORMAT = {
        'img':{'date':['IMG_\d{8}_\d{6}',(4,12),'%Y%m%d']  ,
               'time':['IMG_\d{8}_\d{6}',(14,20) ,'%H%M%S']} ,#%f微秒
        'raw':[],
        'video':{'group':[".*_g\d*_id",(0,-3),]}, # 视频不按照时间分类
        'img_group':{'group':['\d*_',(0,-1),]},
        'img_from_video':{'group':[".*_g\d*_id",(0,-3),]},
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
        self.opts = copy.deepcopy(opts)
        self.skip = 0
        self.raw_files_num = 0
        self.img_num = 0
        self.OptCheck()

    def OptCheck(self):
        opts = self.opts
        assert(opts['out_style'] in ['split','group','concentrate'])
        assert(opts['processing_type'] in ['zoom','slice'])
        assert(opts['split_keep_serial_style'] in ['number','underline'])
        if(opts['out_style'] is 'split'):
            if(self.dtype is 'img'):
                assert(opts['img_min_ele_num'] >= opts['split_n'])
            elif(self.dtype is 'video'):
                assert(opts['video_ele_num'] >= opts['split_n'])
        assert(opts['path_in'] is not 'RAW DIR')
        assert(opts['path_out'] is not 'TARGET DIR')
        
        if(opts['video_image_dir'] is 'default'):
            opts['video_image_dir'] = os.path.join(opts['path_in'],'VIDEO_IMAGE')
        opts['video_vr_opts']['group_ele'] = opts['video_ele_num']
        self.RefleshStartId()


    def Run(self):
        '''
        核心函数，实现图片自动分组、视频读取并分组等核心功能
        主要流程：
            0.预先工作：打印信息，检查源文件夹
            1.根据文件名中的时间进行分组
            2.对图像尺寸进行切片
            3.创建目标文件夹,保存图片（与2在同一个函数进行）
        输入输出：无
        '''
        # 打印配置信息
        self.Print()
        # 检查源文件夹是否存在
        if not os.path.exists(self.opts['path_in']):
            print(f"ERROR: Dir [{self.opts['path_in']}] not exist")
            return

        if self.dtype in ['img' , 'img_group' , 'img_from_video']:
            image_groups = self.ImageClassify()
        elif self.dtype is 'video':
            self.ReadVideos()
            image_groups = self.ImageClassify()

        self.image_groups = image_groups
        self.ImageGroupsProcessing(image_groups)


    def ImageGroupsProcessing(self,image_groups):
        '''
        对图像进行处理、重命名、分组保存
            1.对image_groups中的每个图片进行处理使得符合标准尺寸（标准尺寸在opts中定义）
            2.根据不同的分组类型创建文件夹并保存图像文件
        函数输入：
            image_groups：已经按时间分完组的列表，列表的每个元素代表一组图像
        隐藏输入：
             self.opts: 见下方 读取相关参数 模块
        函数输出：
            无
        自定义函数调用：
            self.ImageProcessing
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
        s_groupid = self.opts['concentrate_start_groupid']
        split_keep_serial = self.opts['split_keep_serial']
        split_keep_serial_style = self.opts['split_keep_serial_style']
        # 判断输出文件夹存不存在
        if not os.path.exists(path_out):
            print(f"INFO: Dir {path_out} not exists , Create folder...")
            os.makedirs(path_out)
        # 如果是分离模式，在循环外创建文件夹
        print(f'\nINFO:Out_style : {out_style}')
        if(out_style is 'split'):
            # 文件夹数目
            split_n = self.opts['split_n']
            split_dir_names = []
            for i in range(split_n):
                ids = str(i).zfill(dir_digits)
                dir_name = dir_prefix + ids + dir_suffix
                dir_name = os.path.join(path_out,dir_name)
                if not os.path.exists(dir_name):
                    print(f"INFO: Dir {dir_name} not exists , Create folder...")
                    os.makedirs(dir_name)
                split_dir_names.append(dir_name)
        count = 0
        self.img_save_image_groups = []
        for gi,group in enumerate(image_groups):
            if(out_style is 'group'):
                # 组模式，给每个组创建文件夹
                ids = str( gi + s_dirid ).zfill(dir_digits)
                dir_name = dir_prefix + ids + dir_suffix
                dir_name = os.path.join(path_out,dir_name)
                if not os.path.exists(dir_name):
                    print(f"INFO: Dir {dir_name} not exists , Create folder...")
                    os.makedirs(dir_name)
            # 读取、处理、保存一组图像
            for gj,img_name in enumerate(group):
                #如果是分离模式，一组图片数量超过上限就应停止
                if(out_style is 'split' and gj >= split_n):
                    print('INFO:Ignore the excess image in the group: [',
                           os.path.basename(img_name),']')
                    self.skip += 1
                    continue
                count += 1
                print('INFO:ImgProcessing ',count,'/',self.img_num -self.skip)
                img = Image.open(img_name)
                # 通过ExifTags标志判断是否需要旋转
                img = OrientationCorrection(img)
                # 对图像进行旋转缩放切片操作使得符合标准尺寸
                img = self.ImageProcessing(img)
                #对图像命名并保存
                if(out_style is 'group'):
                    # 组模式,使用内层(组内序号)编号
                    ids = str( gj ).zfill(file_digits)
                    file_name = file_prefix + ids + file_suffix
                    # 直接使用外层循环创建的文件夹名称
                    file_name = os.path.join(dir_name,file_name)
                elif(out_style is 'split'):
                    # 分离模式,使用外层(组序号)编号
                    ids = str( gi + s_fileid ).zfill(file_digits)
                    # 如果设置了split_keep_serial参数，文件名除了组序号之外再加上组内序列号
                    if(split_keep_serial):
                        if(split_keep_serial_style is 'number'):
                            ids = ids + f'_{gj}'
                        elif(split_keep_serial_style is 'underline'):
                            ids = ids + '_'*gj
                    file_name = file_prefix + ids + file_suffix
                    file_name = os.path.join(split_dir_names[gj],file_name)
                elif(out_style is 'concentrate'):
                    # 集中模式，不创建文件夹，同时使用两个序号
                    suf_ids = str( gj ).zfill(file_digits)
                    pre_ids = str( gi + s_groupid ).zfill(file_digits)
                    ids = pre_ids + '_' + suf_ids
                    file_name = file_prefix + ids + file_suffix
                    file_name = os.path.join(path_out,file_name)

                print('INFO:Image [',os.path.basename(img_name),
                      '] save as [',os.path.basename(file_name),
                      '] in directory [',os.path.dirname(file_name),']')
                img.save(file_name)


    def ImageProcessing(self,im):
        '''
        对图像进行旋转缩放切片操作使得符合标准尺寸(标准尺寸在opts中定义)
        思路是：
            1.判断是否需要旋转
                只针对视频导出的图片使用，手机直接拍摄的图片通过ExifTags标志判断是否需要旋转
            2.进行缩放，使缩放后的图像的能覆盖目标尺寸的图像,即
              w>=tw,h>=th
            3.进行切片,切除长边
        函数输入：
            im：待处理图像，类型是Image
        隐藏输入：
            self.opts：
                'height','width','auto_rotate',
                'rotate_angle','processing_type'
        函数输出：
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
            print('INFO:rotate ,hw_ratio :',hw_ratio,' target_hw_ratio:',target_hw_ratio)
            img = im.rotate(rotate_angle,expand = True)
            w, h = img.size
        else:
            img = im
        ## step2. 进行缩放，使缩放后的图像的能覆盖目标尺寸的图像
        if(w == tw and h == th):
            # 尺寸一样大直接返回
            return img
        if(w == tw and h > th):
            # 有一边（h或w）一样大的情形
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
        ## step3. 进行切片,切除长边
        box=(ws,hs,ws+tw,hs+th) 
        return img.crop(box)


    def ImageClassify(self):
        '''
        根据文件名中的时间或组编号对图像进行分组
        1.获得文件夹中的所有【图像】文件,图像的后缀名列表在文件开头定义
        2.获取文件名中的时间,按时间进行分组,判断组内图像数目是否符合要求
        输入：
            无
        隐藏输入：
            self.opts:
        输出：
            image_groups：已经按时间分完组的列表，列表的每个元素代表一组图像
        隐藏输出：
            self.img_num
            self.image_list
            self.video_image_groups
        自定义函数调用：
            self.GetFiles
            self.ClassifyUsingGroupId
            self.ClassifyUsingDateTime
        '''
        # 获得文件夹中的所有图像文件
        if (self.dtype is 'video'):
            file_list = self.GetFiles(self.opts['video_image_dir'])
        else:
            file_list = self.GetFiles()

        print(f'INFO:Find {len(file_list)} Files with ',end='')
        # 判断是不是图像格式
        self.image_list = FilesFilter(file_list,_IMGTYPE_LIST)
        self.img_num = len(self.image_list)
        print(f'{self.img_num} Images')
        # 获取文件名中的时间，按时间进行分组，判断组内图像数目是否符合要求
        if(self.dtype is 'img'):
            image_groups = self.ClassifyUsingDateTime(
                    self.image_list,self.opts['img_min_ele_num'])
        elif(self.dtype in ['img_group' , 'img_from_video']):
            image_groups = self.ClassifyUsingGroupId(
                    self.image_list,self.opts['img_min_ele_num'])
        elif(self.dtype is 'video'):
            image_groups = self.ClassifyUsingGroupId(
                self.image_list ,self.opts['video_ele_num'])

        self.img_image_groups = image_groups
        return image_groups


#    def VideoClassify(self):
#        '''
#        用于对ReadVideos函数输出的图像进行分组
#        函数输入：无
#        隐藏输入：
#            self.opts:
#                'video_image_dir'
#                'video_vr_opts':'group_ele'
#        函数输出：
#            image_groups：分组完成后的组列表
#        隐藏输出：
#            self.img_num
#            self.image_list
#            self.video_image_groups
#        自定义函数调用：
#            self.GetFiles
#            self.ClassifyUsingGroupId
#        '''
#        # 
#        dir_path = self.opts['video_image_dir']
#        file_list = self.GetFiles(dir_path)
#        print(f'INFO: Find {len(file_list)} Files with ',end='')
#        # 判断是不是图像格式
#        self.image_list = FilesFilter(file_list,_IMGTYPE_LIST)
#        self.img_num = len(self.image_list)
#        print(f'{self.img_num} Images')
#        image_groups = self.ClassifyUsingGroupId(
#                self.image_list ,self.opts['video_ele_num'])
#        self.video_image_groups = image_groups
#        return image_groups


    def ClassifyUsingDateTime(self,image_list,min_ele = 1):
        '''
        基于文件名中的日期和时间对图像进行分组
        函数输入：
            image_list：待分类的图像名列表
            min_ele：每组最少元素数目（含）
        隐藏输入：
            self.dtype
            _DEFAULT_NAME_FORMAT
        函数输出：
            image_groups：分完组后的组列表
        隐藏输出：
            self.skip：由于名称不匹配或组内元素数目不足忽略的图片数目
        调用自定义函数：
            self.GetTimeFromName
        '''
        # 初始化参数
        image_groups = []
        current_group = []
        last_item_dt = datetime.datetime.strptime('10000101000000','%Y%m%d%H%M%S')
        for image_name in self.image_list:
            # 获取日期时间
            date_time = self.GetTimeFromName(image_name)
            if(False == date_time):
                #如果文件名不符合则跳过
                self.skip += 1
                continue
            # 计算时间差
            ddt = abs((date_time-last_item_dt).total_seconds())
            # 更新上一项日期时间
            last_item_dt = date_time
            # 判断是否同一组
            if ddt < self.opts['img_max_interval']:
                current_group.append(image_name)
            else:
                # 判断组内图像数目是否符合要求
                if(len(current_group) >= min_ele ):
                    image_groups.append(current_group)
                elif(len(current_group) >= 1):
                    ignore_group = list(map(os.path.basename,current_group))
                    print(f'INFO:Insufficient number of images in group,ignore images {ignore_group}')
                    self.skip += len(ignore_group)
                # 初始化新组
                current_group = [image_name]
        # 处理最后一组
        if(len(current_group) >= min_ele):
            image_groups.append(current_group)
        elif(len(current_group) >= 1):
            ignore_group = list(map(os.path.basename,current_group))
            print(f'INFO:Insufficient number of images in group,ignore images {ignore_group}')
            self.skip += len(ignore_group)
        return image_groups


    def ClassifyUsingGroupId(self,image_list,min_ele = 1):
        '''
        基于文件名中的组编号对图像进行分组
        函数输入：
            image_list：待分类的图像名列表
            min_ele：每组最少元素数目（含）
        隐藏输入：
            self.dtype
            _DEFAULT_NAME_FORMAT
        函数输出：
            image_groups：分完组后的组列表
        隐藏输出：
            self.skip：由于名称不合法或组内元素数目不足忽略的图片数目
        '''
        # 构建正则表达式
        dtype = self.dtype
        name_format = _DEFAULT_NAME_FORMAT[dtype]
        group_format = name_format['group']
        pattern_group = re.compile(group_format[0])
        # 初始化参数
        image_groups = []
        current_group = []
        current_group_name = None
        for image_name in image_list:
            image_basename = os.path.basename(image_name)
            group_name = pattern_group.findall(image_basename)
            # 判断字段是否成功
            if len(group_name) == 0:
                # 如果字段匹配失败则跳过
                self.skip += 1
                continue
            else:
                # 如果成功则提取有效字段
                group_name = group_name[0]
                group_name = group_name[group_format[1][0] : group_format[1][1]]
            # 判断是否同一组
            if(current_group_name == group_name):
                current_group.append(image_name)
            else:
                # 判断组内元素数量是否充足
                if(len(current_group) >= min_ele):
                    image_groups.append(current_group)
                elif(len(current_group) >= 1):
                    ignore_group = list(map(os.path.basename,current_group))
                    print(f'INFO:Insufficient number of images in group,ignore images {ignore_group}')
                    self.skip += len(ignore_group)
                # 更新
                current_group_name = group_name
                current_group = [image_name]
        # 处理最后一组
        if(len(current_group) >= min_ele):
            image_groups.append(current_group)
        elif(len(current_group) >= 1):
            ignore_group = list(map(os.path.basename,current_group))
            print(f'INFO:Insufficient number of images in group,\
                  ignore images {ignore_group}')
            self.skip += len(ignore_group)
        return image_groups


    def ReadVideos(self):
        '''
        主要功能是从视频中读取图像并重命名后保存在指定的文件夹中
        函数输入：无
        隐藏输入：
            self.opts：'video_image_dir','video_vr_opts','video_group_num',
                'video_wait'
        函数输出：无
        隐藏输出：
            self.video_list , self.video_num
        自定义函数调用：
            self.GetFiles
            self.SaveVideoImages
            VideoReader
        '''
        # 获得文件夹中的所有视频文件
        file_list = self.GetFiles()
        print(f'INFO:Find {len(file_list)} Files with ',end='')
        # 判断是不是视频格式
        self.video_list = FilesFilter(file_list,_VIDTYPE_LIST)
        self.video_num = len(self.video_list)
        print(f'{len(self.video_list)} Videos')
        # 在源文件目录下创建存放源图像文件的目录，此目录及其中的文件会被保留
        video_image_dir = self.opts['video_image_dir']
        if not os.path.exists(video_image_dir):
            os.makedirs(video_image_dir)
        # 对每个视频进行读取、保存
        for video_name in self.video_list:
            vr_opts = copy.deepcopy(self.opts['video_vr_opts'])
            vr = VideoReader(video_name , opts = vr_opts)
            if self.opts['video_group_num']:
                vr.AutoSet(self.opts['video_group_num'])
            vr.PrintVideoInfo()
            image_groups_arrays = vr.GetAllGroups()
            self.SaveVideoImages(image_groups_arrays,video_name)

        # 询问是否暂停来检查输出是否符合预期
        if(self.opts['video_wait']):
            print('\nINFO:Video read complete ',
                  f', Please check the pictures in folder {video_image_dir} ',
                  ',input Y or y to continue')
            while(True):
                cin = input()
                if(cin is 'Y' or cin is 'y'):
                    break
                else:
                    print('input Y or y to continue')


    def SaveVideoImages(self,image_groups_arrays,video_name):
        '''
        重命名、保存视频输出的图片到指定文件夹
        '''
        video_name_ = os.path.basename(video_name)
        video_name, _ = os.path.splitext(video_name_)
        ext = self.opts['video_image_ext']
        count = 0
        for i,image_group_arrays in enumerate(image_groups_arrays):
            for j,image_array in enumerate(image_group_arrays):
                image_name_ = video_name + '_g' + str(i) + '_id' + str(j) + ext
                dir_path = self.opts['video_image_dir']
                image_name = os.path.join(dir_path,image_name_)
                image = Image.fromarray(image_array)
                image.save(image_name)
                count += 1
        print(f'INFO:Video [{video_name_}] output {count}({len(image_groups_arrays)}) images')


    def GetFiles(self,img_dir = None):
        '''
        获取指定目录下的全部文件和文件夹
        '''
        img_dir = self.opts['path_in'] if img_dir is None else img_dir
        if not os.path.exists(img_dir):
            print(f'INFO:Dir [{img_dir}] not exist')
            return []
        file_list = sorted(glob(os.path.join(img_dir, '*')))
        self.raw_files_num = len(file_list)
        return file_list


    def GetTimeFromName(self,name):
        '''
        利用正则表达式从文件名中获得文件的时间
        表达式的表述在_DEFAULT_NAME_FORMAT中定义
        文件一般指手机中拍摄得到的文件
        输入：
            name：文件名
        隐藏输入：
            self.dtype
            _DEFAULT_NAME_FORMAT
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


    def Print(self):
        '''
        打印相关信息：类配置，视频信息
        '''
        print("opts INFO:")
        [print(f'{opt[0]}:{opt[1]}') for opt in self.opts.items() if opt[0] is not 'video_vr_opts']
        if (self.dtype is 'video'):
            print("VideoReader opts INFO:")
            [print(f'{opt[0]}:{opt[1]}') for opt in self.opts['video_vr_opts'].items()]

    def GetContinueId(self):
        id_ = self.opts['start_id']
        new_add = len(self.image_groups)
        return int(id_ + new_add)
#        if(self.opts['out_style'] is 'split'):
#            s_fileid = self.opts['split_start_fileid']
#            new_add = len(self.image_groups)
#            return int(s_fileid + new_add)
#        elif(self.opts['out_style'] is 'group'):
#            s_dirid = self.opts['group_start_dirid']
#            new_add = len(self.image_groups)
#            return int(s_dirid + new_add)
#        elif(self.opts['out_style'] is 'concentrate'):
#            s_groupid = self.opts['concentrate_start_groupid']
#            new_add = len(self.image_groups)
#            return int(s_groupid + new_add)


    def SetContinueId(self,id_):
        self.opts['start_id'] = id_
        self.RefleshStartId()
#        if(self.opts['out_style'] is 'split'):
#            self.opts['split_start_fileid'] = id_
#        elif(self.opts['out_style'] is 'group'):
#            self.opts['group_start_dirid'] = id_
#        elif(self.opts['out_style'] is 'concentrate'):
#            self.opts['concentrate_start_groupid'] = id_


    def ContinueId(self,na):
        # 从上一个类继续编号
        self.SetContinueId(na.GetContinueId())


    def RefleshStartId(self):
        #'split_start_fileid':0, # 起始图片组编号,默认是0,一般用于扩展数据集(同start_id)
        #'group_start_dirid':0 , # 起始文件夹（组）编号   (同start_id)
        # 'concentrate_start_groupid':0, # 起始组编号   (同start_id)
        self.opts['group_start_dirid'] = self.opts['start_id']
        self.opts['concentrate_start_groupid'] = self.opts['start_id']
        self.opts['split_start_fileid'] = self.opts['start_id']

def OrientationCorrection(img):
    '''
    利用PIL读取exif中的orientation信息，
    然后根据这个信息将图片转正后，再进行后续操作
    
    Ref：https://blog.csdn.net/mizhenpeng/article/details/82794112
    '''
    for orientation in ExifTags.TAGS.keys() : 
        if ExifTags.TAGS[orientation]=='Orientation' : break 
    if(img._getexif() is None):
        return img
    exif=dict(img._getexif().items())
    if   exif[orientation] == 3 : 
        img=img.rotate(180, expand = True)
    elif exif[orientation] == 6 : 
        img=img.rotate(270, expand = True)
    elif exif[orientation] == 8 : 
        img=img.rotate(90, expand = True)
    return img

def FilesFilter(file_list,type_list = _IMGTYPE_LIST):
    '''
    通过后缀名过滤列表中的文件
    '''
    target_list = []
    for item in file_list:
        _,ext = os.path.splitext(item)
        if(ext[1:] not in type_list):
            pass
        else:
            target_list.append(item)
    return target_list



### 测试 ###
# 直接图像类型
#opts = copy.deepcopy(_DEFAULT_NameAnalyzer_OPTION)
#opts['path_in']='E:/data/图片预处理/img/20190108/RGB/'
#opts['path_out']='../data/Real/test1/'
#opts['out_style']='split'
#opts['split_keep_serial']=True
#opts['split_keep_serial_style']= 'underline'
#opts['dir_prefix']= 'im'
#opts['dir_digits']= 0
#opts['file_digits']= 0
##opts['auto_rotate']=True
#a = NameAnalyzer('img',opts)
#a.Run()
#image_groups = a.img_image_groups

# 视频类型
#opts = copy.deepcopy(_DEFAULT_NameAnalyzer_OPTION)
#opts['path_in']='E:/data/图片预处理/img/20190108/VIDEO/'
#opts['path_out']='../data/Real/test2/'
#opts['out_style']='split'
#opts['split_keep_serial']=True
#opts['split_keep_serial_style']= 'underline'
#opts['dir_prefix']= 'im'
#opts['dir_digits']= 0
#opts['file_digits']= 0
#opts['auto_rotate']=True
#
#vr_opts = copy.deepcopy(_DEFAULT_VideoReader_OPTION)
#vr_opts['start'] = 0.05
#vr_opts['end'] = 0.95
#opts['video_vr_opts'] = vr_opts
#opts['video_group_num'] = 1
#opts['video_wait'] = False
#
#a = NameAnalyzer('video',opts)
#a.Run()
#image_groups = a.video_image_groups