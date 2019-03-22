# -*- coding: utf-8 -*-

from datasets_lib2 import MainBoard, DEFAULT_MAINBOARD_OPTS, TransOptsManager
from datasets_lib3 import Sequence


mo = DEFAULT_MAINBOARD_OPTS
sequence = Sequence(1,3,'../data/ds_v2/TEST7')

for i in sequence:
    print(next(i))
    print(next(i))
    print(next(i))

