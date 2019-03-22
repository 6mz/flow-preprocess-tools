# -*- coding: utf-8 -*-
import os
from PIL import Image

path = '../data/ds_v2_material/download/sky'
save = '../data/ds_v2_material/sky'
fileList = os.listdir(path)
n = len(fileList)
for i, file in enumerate(fileList):
    try:
        pic = Image.open(os.path.join(path, file))
    except OSError as Argument:
        print(Argument)
        continue
    size = pic.size
    x = size[0]
    y = size[1]
    pic = pic.crop((0, 0, x, int(y*0.9)))
    pic.save(os.path.join(save, 'sky_'+str(i)+'.png'))
    print(f'finish{i+1}/{n}')
print('all finish')
