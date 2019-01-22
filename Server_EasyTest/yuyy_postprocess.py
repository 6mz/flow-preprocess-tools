import numpy as np
from PIL import Image
import cv2
import time
import glob,os,sys
import numpy as np
from scipy.misc import imread,imsave

# to output the visualization, please download flow_io.py and viz_flow.py from https://github.com/jswulff/pcaflow/tree/master/pcaflow/utils
from flow_io import flow_read, open_flo_file
# import sys
# sys.path.append("..")


def warp_judge_(im, flow, im2, mode='replace'):
    '''
    warp image2 to image1
    mode:
      repalce: replace pixels in occlusion area(big mask) and small hole with pixes from im2.
      interpolate: replace pixels in occlusion area(big mask) with pixels from im2, and 
        interpolate pixels in small holes.
      esay: fill holes with zero.
    '''
    assert(mode == 'replace' or mode == 'esay' or mode == 'judge')
    image_height = im.shape[0]
    image_width = im.shape[1]
    flow_height = flow.shape[0]
    flow_width = flow.shape[1]

    (iy, ix) = np.mgrid[0:image_height, 0:image_width]
    (fy, fx) = np.mgrid[0:flow_height, 0:flow_width]
    fx=np.float64(fx)
    fy=np.float64(fy)
    fx += flow[:,:,0]
    fy += flow[:,:,1]

    fx = np.minimum(np.maximum(fx, 0), flow_width-1)
    fy = np.minimum(np.maximum(fy, 0), flow_height-1)

    fx=np.rint(fx)
    fy=np.rint(fy)
    fx=fx.astype(np.int)
    fy=fy.astype(np.int)

    # print('fx.shape:', fx.shape)
    print('max flow:',np.max(np.max(flow[:,:,1])))
    print('min flow:',np.min(np.min(flow[:,:,1])))

    warp = np.zeros((image_height, image_width, im.shape[2]))
    # mask_hole = np.zeros((image_height, image_width))
    mask = np.zeros((image_height, image_width)) # suspected area
    mask_edge = np.zeros((image_height, image_width))   ###

    if mode == 'esay':
        warp[iy,ix]=im2[fy,fx]
        returned_warp = warp
    else:
        mask_twice = np.zeros((image_height, image_width, 2)) # areas be applied for multiple times in im2
        mask_diff = np.zeros((image_height, image_width))  # diff with im of candidate pixels
        for fj, fi, ij, ii in zip(fy.flat, fx.flat, iy.flat, ix.flat):
            if fi > 0 and fi < flow_width - 1 and fj > 0 and fj < flow_height - 1:
                if not mask_twice[fj,fi].any():
                    warp[ij, ii] = im2[fj, fi]
                    # record first place in im1, if (fj, fi) be called for the second time, both two places will be recoded in mask
                    mask_twice[fj,fi] = ij, ii  
                    mask_diff[fj,fi] = np.sum(np.abs(im2[fj,fi] - im[ij,ii]))
                else:
                    warp[ij, ii] = im2[fj, fi]
                    # mask[ij, ii] = 1
                    # mask[np.int(mask_twice[fj,fi,0]), np.int(mask_twice[fj,fi,1])]=1
                    diff = np.sum(np.abs(im2[fj,fi] - im[ij,ii]))
                    # keep the pixels more similar to target im
                    if diff < mask_diff[fj,fi]:
                        mask[np.int(mask_twice[fj,fi,0]), np.int(mask_twice[fj,fi,1])]=1
                        mask_diff[fj,fi] = diff
                    else:
                        mask[ij, ii] = 1
            else:
                warp[ij,ii] = 0 #im[ij,ii]

        mask = np.uint8(mask)
        # Duplicate region
        if mode == 'replace':
            kernel = np.uint8(np.ones((4,4)))
            kernel2 = np.uint8(np.ones((8,8)))
            mask = cv2.erode(mask, kernel)
            # mask = cv2.dilate(mask, kernel)
            # mask = cv2.erode(mask, kernel2)
            # mask = cv2.erode(mask, kernel)
            # mask = cv2.dilate(mask, kernel2)
            mask = cv2.dilate(mask, kernel2)
            mask = cv2.dilate(mask, kernel2)
            mask = cv2.dilate(mask, kernel2)
            mask = mask.astype(np.int)
        elif mode == 'judge':
            kernel = np.uint8(np.ones((2,2)))
            kernel2 = np.uint8(np.ones((8,8)))
            mask = cv2.erode(mask, kernel)
            # mask = cv2.dilate(mask, kernel2)
            # # mask = cv2.erode(mask, kernel)
            # # mask = cv2.erode(mask, kernel)
            # mask = cv2.dilate(mask, kernel2)
            # mask = cv2.dilate(mask, kernel2)

        mask = mask[:, :, np.newaxis]
        mask = mask.repeat(3, axis=2)
        # warp[mask>0] = 255  ###
        warp[mask>0] = im[mask>0]
        returned_warp = np.uint8(warp)
        tmp = im2.copy()
        im2[mask>0] = 255
        returned_mask = np.uint8(tmp/2.+im2/2.)

    # return warp.astype(np.uint8), mask
    return returned_warp, returned_mask


def warp_judge(im, flow, im2, mode='replace'):
    '''
    warp im1 to im2
    mode:
      repalce: replace pixels in occlusion area(big mask) and small hole with pixes from im2.
      interpolate: replace pixels in occlusion area(big mask) with pixels from im2, and 
        interpolate pixels in small holes.
      esay: fill holes with zero.
    '''
    assert(mode == 'replace' or mode =='interpolate' or mode == 'esay')
    image_height = im.shape[0]
    image_width = im.shape[1]
    flow_height = flow.shape[0]
    flow_width = flow.shape[1]

    (iy, ix) = np.mgrid[0:image_height, 0:image_width]
    (fy, fx) = np.mgrid[0:flow_height, 0:flow_width]
    fx=np.float64(fx)
    fy=np.float64(fy)
    fx += flow[:,:,0]
    fy += flow[:,:,1]

    fx = np.minimum(np.maximum(fx, 0), flow_width-1)
    fy = np.minimum(np.maximum(fy, 0), flow_height-1)

    fx=np.rint(fx)
    fy=np.rint(fy)
    fx=fx.astype(np.int)
    fy=fy.astype(np.int)

    # print('fx.shape:', fx.shape)
    print('max flow:',np.max(np.max(flow[:,:,1])))
    print('min flow:',np.min(np.min(flow[:,:,1])))

    warp = np.zeros((image_height, image_width, im.shape[2]))
    mask_twice = np.zeros((image_height, image_width))

    if mode == 'esay':
        warp[fy,fx]=im[iy,ix]
        mask_big_twice = mask_twice # 0
        returned_warp = warp
    else:
        # compare = np.zeros((image_height, image_width, im.shape[2]))
        for fj, fi, ij, ii in zip(fy.flat, fx.flat, iy.flat, ix.flat):
            if not warp[fj,fi].any():
                warp[fj, fi] = im[ij, ii]
                # compare[fj, fi] = abs(im[ij, ii]-im2[fj, fi])
            else:
                mask_twice[fj, fi] = 1
                # if np.mean(abs(im[ij, ii]-im2[fj, fi])) <= np.mean(compare[fj, fi]):
                #     # print('true')
                #     warp[fj, fi] = im[ij, ii]
                #     compare[fj, fi] = abs(im[ij, ii]-im2[fj, fi])

        # detect areas which have been occupied for several times.
        mask_twice = np.uint8(mask_twice)
        kernel0 = np.uint8(np.ones((2,2)))
        kernel = np.uint8(np.ones((4,4)))
        kernel2 = np.uint8(np.ones((8,8)))
        mask_twice = cv2.erode(mask_twice, kernel0)
        mask_twice = cv2.dilate(mask_twice, kernel)
        # mask_twice = cv2.erode(mask_twice, kernel0)
        mask_twice = cv2.erode(mask_twice, kernel)
        mask_twice = cv2.dilate(mask_twice, kernel2)
        mask_twice = cv2.dilate(mask_twice, kernel2)
        # mask_twice = cv2.erode(mask_twice, kernel2)
        # mask_twice = cv2.erode(mask_twice, kernel2)
        mask_twice = cv2.dilate(mask_twice, kernel)
        # mask_twice = cv2.dilate(mask_twice, kernel2)
        mask_twice = mask_twice.astype(np.int)

        # detect big holes (usually in occlution areas)
        mask_hole = np.logical_and(warp[:,:,0] == 0, warp[:,:,1] == 0, warp[:,:,2] == 0)
        mask_big = np.uint8(mask_hole)
        # big hole mask
        kernel = np.uint8(np.ones((4,4)))
        mask_big = cv2.dilate(mask_big, kernel)
        mask_big = cv2.erode(mask_big, kernel)
        mask_big = cv2.erode(mask_big, kernel)
        mask_big = cv2.dilate(mask_big, kernel)
        mask_big = mask_big.astype(np.int)

        mask_or = mask_hole | mask_big | mask_twice
        mask_big_twice = mask_big | mask_twice
        if mode == 'replace':
            mask_or = mask_or[:, :, np.newaxis]
            mask_or = mask_or.repeat(3, axis=2)
            # mask_big_twice = mask_big_twice[:, :, np.newaxis]  ####
            # mask_big_twice = mask_big_twice.repeat(3, axis=2)   ####
            warp[mask_or>0] = im2[mask_or>0]
            # warp[mask_big_twice>0] = 255  ####
            returned_warp = np.uint8((warp+im2)/2.)
        elif mode == 'interpolate':
            # small hole mask: | firstly then ^(exclusive or)
            mask_small = mask_or ^ mask_big_twice
            for i in range(1,flow_height-1):
                for j in range(1,flow_width-1):
                    if mask_small[i][j] > 0:
                        a=[]
                        if warp[i-1][j-1].any():
                            a.append(warp[i-1][j-1]) 
                        if warp[i-1][j  ].any():
                            a.append(warp[i-1][j  ]) 
                        if warp[i-1][j+1].any():
                            a.append(warp[i-1][j+1])
                        if warp[i  ][j+1].any():
                            a.append(warp[i  ][j+1]) 
                        if warp[i+1][j+1].any():
                            a.append(warp[i+1][j+1])
                        if warp[i+1][j  ].any():
                            a.append(warp[i+1][j  ]) 
                        if warp[i+1][j-1].any():
                            a.append(warp[i+1][j-1]) 
                        if warp[i  ][j-1].any():
                            a.append(warp[i  ][j-1])                 
                        b=np.array(a)
                        if a:
                            warp[i, j, :]=np.mean(b, axis=0)
            # mask_small = np.uint8(mask_small)
            mask_big_twice = mask_big_twice[:, :, np.newaxis]
            mask_big_twice = mask_big_twice.repeat(3, axis=2)
            returned_warp = warp
            mask_big_twice = mask_big_twice.astype(np.bool)
#            warp[mask_big_twice>0] = im2[mask_big_twice>0]
#            returned_warp = np.uint8((warp+im2)/2.)

    # return warp.astype(np.uint8), mask_big_twice
    return returned_warp, mask_big_twice


def warp_easy(im, flow, im2=None):
    image_height = im.shape[0]
    image_width = im.shape[1]
    flow_height = flow.shape[0]
    flow_width = flow.shape[1]

    (iy, ix) = np.mgrid[0:image_height, 0:image_width]
    (fy, fx) = np.mgrid[0:flow_height, 0:flow_width]
    fx=np.float64(fx)
    fy=np.float64(fy)
    fx += flow[:,:,0]
    fy += flow[:,:,1]

    fx = np.minimum(np.maximum(fx, 0), flow_width-1)
    fy = np.minimum(np.maximum(fy, 0), flow_height-1)

    warp = np.zeros((image_height, image_width, im.shape[2]))
    
    fx=np.rint(fx)
    fy=np.rint(fy)
    fx=fx.astype(np.int)
    fy=fy.astype(np.int)

    print('max flow:',np.max(np.max(flow[:,:,1])))
    print('min flow:',np.min(np.min(flow[:,:,1])))

    warp[fy,fx]=im[iy,ix]
    mask = np.logical_and(warp[:,:,0] == 0, warp[:,:,1]==0, warp[:,:,2]==0)
    mask = np.uint8(mask)

    # big hole mask
    kernel = np.uint8(np.ones((4,4)))
    mask = cv2.dilate(mask, kernel)
    mask = cv2.erode(mask, kernel)
    mask = cv2.erode(mask, kernel)
    mask = cv2.dilate(mask, kernel)
    mask = mask.astype(np.int)
    mask = mask[:, :, np.newaxis]
    mask = mask.repeat(3, axis=2)

    if im2 is not None:
        warp[mask>0] = im2[mask>0]

    return warp.astype(np.uint8), mask


if __name__=="__main__":
    image1_list     = './real_img1.txt';
    image2_list     = './real_img2.txt';
    out_flow_file   = './out_real.txt';
    out_vis_file    = './viz.txt';
    out_warp_file   = './warp.txt';

    with open(image1_list, 'r') as f:
        images1 = [line.strip() for line in f.readlines() if len(line.strip()) > 0]
    with open(image2_list, 'r') as f:
        images2 = [line.strip() for line in f.readlines() if len(line.strip()) > 0]
    if len(images1) != len(images2):
        print("Unequal amount of images in the given lists (%d vs. %d)" % (len(images1), len(images2)))
        sys.exit(1)

    with open(out_flow_file, 'r') as f:
        out_flow_list = [line.strip() for line in f.readlines() if len(line.strip()) > 0]
    if out_vis_file != None:
        with open(out_vis_file, 'r') as f:
            out_vis_list = [line.strip() for line in f.readlines() if len(line.strip()) > 0]
    else:
        out_vis_list = None
    if out_warp_file != None:
        with open(out_warp_file, 'r') as f:
            out_warp_list = [line.strip() for line in f.readlines() if len(line.strip()) > 0]
    else:
        out_warp_list = None

    assert(len(out_flow_list)==len(out_warp_list))
    assert(len(images1)==len(out_flow_list))
    for i in range(len(out_flow_list)):
        im_1=imread(images1[i])
        im_2=imread(images2[i])
        flow_=open_flo_file(out_flow_list[i])
        warped, mask0=warp_judge_(im_1,flow_,im_2,'judge')
        imsave(out_warp_list[i],warped)
        imsave(str(i*2+10)+'tmp.png',mask0)
