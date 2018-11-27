# -*- coding: utf-8 -*-
import sys
import subprocess


commendname = 'commend.txt'
if len(sys.argv) > 1:
    commendname = sys.argv[1]

with open(commendname,'r') as f:
    args = [line.strip() for line in f.readlines() if len(line.strip()) > 0]
args = args[0].split()
cmd = str.join(' ', args)
print('Executing %s' % cmd)
subprocess.call(args)       