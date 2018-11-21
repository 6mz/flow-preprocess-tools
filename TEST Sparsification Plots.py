# -*- coding: utf-8 -*-
from myflowlib import open_flo_file,Sparplot,readPFM
import matplotlib.pyplot as plt

path= './data/flow_file/SparPlotTest/'
#flow_name = 'a_frame_0001_forward.flo'
#res_name = 'a_frame_0001_forward_res.flo'
#gt_name = 'flow_frame_0001.flo'
flow_name = '0006_forward.flo'
res_name = '0006_forward_res.flo'
gt_name = 'OpticalFlowIntoFuture_0006_L.pfm'

flow_name = path + flow_name
res_name = path + res_name
gt_name = path + gt_name

flow = open_flo_file(flow_name)
res = open_flo_file(res_name)
#gt = open_flo_file(gt_name)
gt = readPFM(gt_name)

Sparplot(flow,res,gt,is_print=True,steps=200)

#best=gt-flow
#
#total_steps=100
#
#assert flow.shape==res.shape==gt.shape
#
#aepe0=EPE(flow,gt)
#print('AEPE:'+str(aepe0))
#
#totalpixs=int(flow.size/2)
#remainpixs=np.linspace(totalpixs,0,total_steps,endpoint=False,dtype='int')
#
#res=abs_flow(res)
#best=abs_flow(best)
#
#
#
#res_sort=res.flatten()
#best_sort=best.flatten()
#
##n, bins, patches =plt.hist(res,bins=100)
##plt.show()
##n, bins, patches =plt.hist(best,bins=100)
##plt.show()
#
#res_sort_index=np.argsort(res_sort)
#best_sort_index=np.argsort(best_sort)
#
#res_aepe=[]
#res_threshold=[]
#for p in remainpixs:
#    threshold_id=res_sort_index[p-1]
#    threshold=res_sort[threshold_id]
#    aepe=EPE_usingmask(flow,gt,res<threshold)
#    res_aepe.append(aepe)
#    res_threshold.append(threshold)
#
#best_aepe=[]
#best_threshold=[]
#for p in remainpixs:
#    threshold_id=best_sort_index[p-1]
#    threshold=best_sort[threshold_id]
#    aepe=EPE_usingmask(flow,gt,best<threshold)
#    best_aepe.append(aepe)
#    best_threshold.append(threshold)
#
#x=(totalpixs-remainpixs)/totalpixs
#y1=res_aepe/aepe0
#y2=best_aepe/aepe0
#
#plt.plot(x, y1, mec='r', mfc='w',label='Pred-Merged')
#plt.plot(x, y2, ms=10,label='Oracle')
#plt.legend()  # 让图例生效
#plt.margins(0)
#plt.xlabel('Fraction of Removed Pixels') #X轴标签
#plt.ylabel('Average EPE (Normalized)') #Y轴标签
#plt.title('Sparsification Plots') #标题
#plt.show()
