# -*- coding: utf-8 -*-
from program.datasetslib import EasyTest
test=EasyTest('/home/a/public1/flow/data/Sintel/training/',num=5)
test.GenerateRandomlist()
test.GenerateOutVizWarplist()
test.print_all()
