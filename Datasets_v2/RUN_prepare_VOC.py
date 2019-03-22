# -*- coding: utf-8 -*-
from VOC_lib import DEFAULT_GenMaterial_OPTIONS,\
        ReadSegList, GetAnnoList, GetImgList,\
        GetMaskList, ListMannager, GenMaterial
import os
import copy

if __name__ == '__main__':
    # 设置输入路径
    devkit_dir = 'E:\\data\\VOCtrainval_11-May-2012\\VOCdevkit\\VOC2012\\'
    abs_parent_path = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
    print('abs_parent_path:', abs_parent_path)
    # abs_parent_path 上级目录
    # 这里设置输出目录
    out_path = os.path.join(abs_parent_path, 'data', 'ds_v2_material', 'voc')
    opts = copy.deepcopy(DEFAULT_GenMaterial_OPTIONS)
    opts['out_path'] = out_path

    # 读取各个列表
    segList = ReadSegList(devkit_dir)
    segAnnoList = GetAnnoList(devkit_dir, segList)
    segImgList = GetImgList(devkit_dir, segList)
    segMaskList = GetMaskList(devkit_dir, segList)
    myAnno = ListMannager()

    # 进行运算
    count = 0
    assert os.path.exists(devkit_dir)
    assert os.path.exists(out_path)
    for sN, anN, imN, maN in zip(
            segList, segAnnoList, segImgList, segMaskList):
        localAnno = GenMaterial(sN, anN, imN, maN, opts)
        myAnno.Merging(localAnno)
        count += 1
        if count > 0:
            break

    myAnno_path = os.path.join(out_path, '_Annotations')
    if not os.path.exists(myAnno_path):
        print(f'INFO: GenMaterialName: Create folder {myAnno_path}')
        os.makedirs(myAnno_path)
    myAnno.QuickSave(myAnno_path)
