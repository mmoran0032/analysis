#!/usr/bin/env python3


import os

import pyne
import sap


cal_data = pyne.EVTData('../data_np/run289')
cal_data.load_data()
cal = sap.Calibrator(cal_data)

raw = sorted('../data/{}'.format(f)
             for f in os.listdir('../data') if f.endswith('.evt'))
out = sorted('../data_np/{}'.format(f.split('/')[-1].split('-')[0])
             for f in raw)

for r, o in zip(raw, out):
    print('calibrating {}...'.format(o))
    data = pyne.EVTData(o, r)
    data.load_data()
    cal.calibrate(data)

