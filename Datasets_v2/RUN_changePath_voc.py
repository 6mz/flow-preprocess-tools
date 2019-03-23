# -*- coding: utf-8 -*-
from VOC_lib import ListMannager
import os


if __name__ == '__main__':
    rawtxtpath = '/4T_/liumz/ds_v2_material/voc/_Annotations_old'
    targettxtpath = '/4T_/liumz/ds_v2_material/voc/_Annotations'
    old_path = "E:/GitProgram/preprocess-tools/data/ds_v2_material"
    new_path = '/4T_/liumz/ds_v2_material'  # 来自dataset_material
    is_need_process = 1
    listManager = ListMannager()
    listManager.QuickOpen(rawtxtpath)
    for name, lists in listManager.names.items():
        if len(lists) > 0:
            pic, mask = lists[0].split('+')
            pic = '/'.join(pic.split('\\'))
        else:
            continue
        if new_path in pic:
            is_need_process = 0
        elif old_path in pic:
            is_need_process = 1
        else:
            print(pic, old_path)
            is_need_process = 2
        break

    if is_need_process == 0:
        print('不需要处理')
    elif is_need_process == 2:
        print('错误的格式，无法处理')
    elif is_need_process == 1:
        newlistManager = ListMannager()
        for name, lists in listManager.names.items():
            newlistManager.NewList(name)
            for l in lists:
                pic, mask = l.split('+')
                pic = '/'.join(pic.split('\\'))
                mask = '/'.join(mask.split('\\'))
                relpic = os.path.relpath(pic, old_path)
                relmask = os.path.relpath(mask, old_path)
                newpic = os.path.join(new_path, relpic)
                newmask = os.path.join(new_path, relmask)
                newlistManager.Add(name, newpic + '+' + newmask)
        newlistManager.QuickSave(targettxtpath)
        print('完成')
