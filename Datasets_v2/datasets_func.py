# -*- coding: utf-8 -*-
"""

"""
import numpy as np


# ====================== 随机函数 ========================
def FindMinAndMax(in1, in2):
    # 返回的元组小数在前大数在后
    if(in1 > in2):
        return (in2, in1)
    else:
        return (in1, in2)


def RandomScale(minScale, maxScale):
    '''
    返回一个scale矩阵(1*2)
    输入：
        minScale: 格式：(x,y)，表示最小的x和y缩放倍数
        maxScale: 格式：(x,y)，表示最大的x和y缩放倍数
    '''
    assert(len(minScale) == len(maxScale) == 2)
    (minx, maxx) = FindMinAndMax(minScale[0], minScale[0])
    (miny, maxy) = FindMinAndMax(minScale[1], minScale[1])
    assert((maxx >= minx >= 0)and(maxy >= miny >= 0))
    x = np.random.uniform(minx, maxx)
    y = np.random.uniform(miny, maxy)
    return np.array([x, y])


def NormalScale(meanScale, sigmaScale):
    scale = np.random.normal(meanScale, sigmaScale, 2)
    return np.array(scale)


def RandomSize(minSize, maxSize):
    '''
    返回一个size矩阵(1*2)
    输入：
        minSize: 格式：(x,y)，表示最小的x和y
        maxSize: 格式：(x,y)，表示最大的x和y
    '''
    assert(len(maxSize) == len(minSize) == 2)
    (minx, maxx) = FindMinAndMax(maxSize[0], minSize[0])
    (miny, maxy) = FindMinAndMax(maxSize[1], minSize[1])
    assert((maxx >= minx >= 0)and(maxy >= miny >= 0))
    x = np.random.random_integers(minx, maxx)
    y = np.random.random_integers(miny, maxy)
    return np.array([x, y])


def RandomDis(minDis, maxDis):
    '''
    返回一个dis矩阵(1*2)
    输入：
        minDis: 格式：(x,y)，表示最小的x和y
        maxDis: 格式：(x,y)，表示最大的x和y
    '''
    if(isinstance(minDis, (int, float))):
        minx = miny = minDis
    if(isinstance(maxDis, (int, float))):
        maxx = maxy = maxDis
    (minx, maxx) = FindMinAndMax(maxDis[0], minDis[0])
    (miny, maxy) = FindMinAndMax(maxDis[1], minDis[1])
    assert (maxx >= minx) and (maxy >= miny)
    x = np.random.random_integers(minx, maxx)
    y = np.random.random_integers(miny, maxy)
    return np.array([x, y])


def NormalDis(meanDis, sigmaDis):
    if(isinstance(meanDis, (int, float))):
        meanx = meany = meanDis
    if(isinstance(sigmaDis, (int, float))):
        sigmax = sigmay = sigmaDis
    x = np.rint(np.random.normal(meanx, sigmax, 1)[0])
    y = np.rint(np.random.normal(meany, sigmay, 1)[0])
    return np.array([x, y], dtype=np.int)


def RandomAngle(minAngle, maxAngle=None, unit='r'):
    '''
    返回一个弧度为单位的角度
    输入：
        minDis: 格式：(x,y)，表示最小的x和y
        maxDis: 格式：(x,y)，表示最大的x和y
    '''
    if maxAngle is None and minAngle > 0:
        maxAngle = minAngle
        minAngle = 0
    if unit == 'd' or unit == 'degree':
        maxAngle = maxAngle / 180 * np.pi
        minAngle = minAngle / 180 * np.pi
    angle = np.random.normal(minAngle, maxAngle)
    return angle


def NormalAngle(mean=0, sigma=1, unit='r'):
    if unit == 'd' or unit == 'degree':
        mean = mean / 180 * np.pi
        sigma = sigma / 180 * np.pi
    return np.random.normal(mean, sigma, 1)[0]


def RandomLevel(levelDict):
    lvN = list(levelDict.keys())
    lvP = np.array(list(levelDict.values()))
    lvP = lvP / np.sum(lvP)
    return np.random.choice(lvN, p=lvP)


# ==================== txt文件读写 ===========================
def SaveList(fname, listname):
    with open(fname, 'w') as f:
        for line in listname:
            f.write(str(line)+'\n')


def ReadList(fname):
    with open(fname, 'r') as f:
        lists = [line.strip()
                 for line in f.readlines() if len(line.strip()) > 0]
    return lists


# ================== 光流输出 ==========================
def flow_write(filename, uv, v=None):
    """ Write optical flow to file.
    If v is None, uv is assumed to contain both u and v channels,
    stacked in depth.
    Original code by Deqing Sun, adapted from Daniel Scharstein.
    """
    nBands = 2

    if v is None:
        assert(uv.ndim == 3)
        assert(uv.shape[2] == 2)
        u = uv[:, :, 0]
        v = uv[:, :, 1]
    else:
        u = uv

    assert(u.shape == v.shape)
    height, width = u.shape
    f = open(filename, 'wb')
    TAG_CHAR = b'PIEH'
    f.write(TAG_CHAR)
    np.array(width).astype(np.int32).tofile(f)
    np.array(height).astype(np.int32).tofile(f)
    # arrange into matrix form
    tmp = np.zeros((height, width*nBands))
    tmp[:, np.arange(width)*2] = u
    tmp[:, np.arange(width)*2 + 1] = v
    tmp.astype(np.float32).tofile(f)
    f.close()


def viz_flow_color(uv, v=None, logscale=True, scaledown=6, output=False):
    """
    topleft is zero, u is horiz, v is vertical
    red is 3 o'clock, yellow is 6, light blue is 9, blue/purple is 12
    """
    if v is None:
        assert(uv.ndim == 3)
        assert(uv.shape[2] == 2)
        u = uv[:, :, 0]
        v = uv[:, :, 1]
    else:
        u = uv
    colorwheel = makecolorwheel()
    ncols = colorwheel.shape[0]

    radius = np.sqrt(u**2 + v**2)
    if output:
        print("Maximum flow magnitude: %04f" % np.max(radius))
    if logscale:
        radius = np.log(radius + 1)
        if output:
            print("Maximum flow magnitude (after log): %0.4f" % np.max(radius))
    radius = radius / scaledown
    if output:
        print(
            "Maximum flow magnitude (after scaledown): %0.4f" % np.max(radius))
    rot = np.arctan2(-v, -u) / np.pi

    fk = (rot+1)/2 * (ncols-1)  # -1~1 maped to 0~ncols
    k0 = fk.astype(np.uint8)       # 0, 1, 2, ..., ncols

    k1 = k0+1
    k1[k1 == ncols] = 0

    f = fk - k0

    ncolors = colorwheel.shape[1]
    img = np.zeros(u.shape+(ncolors,))
    for i in range(ncolors):
        tmp = colorwheel[:, i]
        col0 = tmp[k0]
        col1 = tmp[k1]
        col = (1-f)*col0 + f*col1

        idx = radius <= 1
        # increase saturation with radius
        col[idx] = 1 - radius[idx]*(1-col[idx])
        # out of range    
        col[~idx] *= 0.75
        img[:,:,i] = np.floor(255*col).astype(np.uint8)

    return img.astype(np.uint8)


def makecolorwheel():
    # Create a colorwheel for visualization
    RY = 15
    YG = 6
    GC = 4
    CB = 11
    BM = 13
    MR = 6

    ncols = RY + YG + GC + CB + BM + MR

    colorwheel = np.zeros((ncols, 3))

    col = 0
    # RY
    colorwheel[0:RY, 0] = 1
    colorwheel[0:RY, 1] = np.arange(0, 1, 1./RY)
    col += RY

    # YG
    colorwheel[col:col+YG, 0] = np.arange(1, 0, -1./YG)
    colorwheel[col:col+YG, 1] = 1
    col += YG

    # GC
    colorwheel[col:col+GC, 1] = 1
    colorwheel[col:col+GC, 2] = np.arange(0, 1, 1./GC)
    col += GC

    # CB
    colorwheel[col:col+CB, 1] = np.arange(1, 0, -1./CB)
    colorwheel[col:col+CB, 2] = 1
    col += CB

    # BM
    colorwheel[col:col+BM, 2] = 1
    colorwheel[col:col+BM, 0] = np.arange(0, 1, 1./BM)
    col += BM

    # MR
    colorwheel[col:col+MR, 2] = np.arange(1, 0, -1./MR)
    colorwheel[col:col+MR, 0] = 1

    return colorwheel
