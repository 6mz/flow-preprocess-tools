import mynumpy as m
import numpy as np
from PIL import Image
from datasets_lib1 import Point, Rect, RectArray, Obj, Trans, Board
import datasets_func as func


def DisplayObject(obj):
    imArray = obj.data * obj.dataMask + obj.data * 0.2
    imArray = imArray / np.max(imArray) * 255
    imArray = np.uint8(imArray)
    im = Image.fromarray(imArray)
    im.show()




pos = func.RandomPoint([50, 50], [250, 250])
# size = func.RandomSize([10, 10], [50, 50])
size1 = [200, 200]
size = size1
size2 = [50, 50]

obj1_rect = Rect(pos, size)
obj1_data = RectArray(obj1_rect, 3)
obj1_data.SetColor([255, 0, 255])


obj1_datamask = RectArray(obj1_rect, 1, dtype=np.bool)
obj1_datamask.SetValue(True)

obj1_mask_rect = Rect(Point(75, 75), size2)
obj1_true_datamask = RectArray(obj1_mask_rect, 1, dtype=np.bool)
obj1_true_datamask.SetValue(False)

obj1_datamask.AddRectArray(obj1_true_datamask, CSYS='local')


obj1 = Obj(obj1_data, obj1_datamask)
trans = Trans(obj1)
pts = trans.GenTrans('py')
trans.ImposeTrans(pts)
#DisplayObject(obj1)
mainboard = Board([640, 480])
mainboard.addTrans(trans)
mainboard.Gen()
mainboard.Display('imA')
mainboard.Display('imB')
#print(obj1)
#look = obj1.data_
#look2 = obj1.dataMask_
