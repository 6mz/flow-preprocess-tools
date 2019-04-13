# -*- coding: utf-8 -*-
import os


def read_list(fname):
    with open(fname,'r') as f:
        lists = [line.strip() for line in f.readlines() if len(line.strip()) > 0]
    return lists

def save_list(fname,listname):
    with open(fname,'w') as f:
        for line in listname:
            f.write(str(line)+'\n')


def ChangePath(path, old_path, new_path):
    path = '/'.join(path.split('\\'))
    if new_path in path:
        return path
    elif old_path in path:
        relpath = os.path.relpath(path, old_path)
        newapth = os.path.join(new_path, relpath)
        return newapth
    else:
        print('Path ERROR')
        assert(1==0)
        return


if __name__ == '__main__':
    path = '/home/a/public1/flow/data/FlyingThings2D'
    old_path = "/4T_/flow/FlyingThings2D"
    new_path = '/home/a/public1/flow/data/FlyingThings2D'  # 来自dataset_material
    subdirs = ['version_2_5000', 'version_2_22000']
    alist = []
    blist = []
    clist = []
    balist = []
    bclist = []
    savepath = os.path.join(path, 'version_2_22000_file_lists')
    aname = 'img1_list.txt'
    bname = 'img0_list.txt'
    cname = 'img2_list.txt'
    baname = 'flo_list.txt'
    bcname = 'flo_list_.txt'
    Aname = 'img1.txt'
    Bname = 'img2.txt'
    gtname = 'flo.txt'
    for sdir in subdirs:
        file = os.path.join(sdir, 'file_list.txt')
        lists = read_list(os.path.join(path, file))
        for line in lists:
            spline = line.split()
            spline = map(ChangePath, spline,
                         [old_path]*len(spline), [new_path]*len(spline))
            a, b, c, ba, bc = spline
            alist.append(a)
            blist.append(b)
            clist.append(c)
            balist.append(ba)
            bclist.append(bc)
    save_list(os.path.join(savepath, aname), alist)
    save_list(os.path.join(savepath, bname), blist)
    save_list(os.path.join(savepath, cname), clist)
    save_list(os.path.join(savepath, baname), balist)
    save_list(os.path.join(savepath, bcname), bclist)
    save_list(os.path.join(savepath, Aname), blist)
    save_list(os.path.join(savepath, Bname), clist)
    save_list(os.path.join(savepath, gtname), bclist)
    print('!!')