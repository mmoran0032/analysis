#!/usr/bin/env python3


import os
import sys

import pyne

raw_files = os.listdir('../data')

if sys.argv[1] == '--evt':
    raw_evt = [f for f in raw_files if f.endswith('.evt')]
    raw_path = ['../data/{}'.format(f) for f in raw_evt]
    new_path = ['../data_np/{}'.format(f.split('-')[0]) for f in raw_evt]

    for raw, new in zip(raw_path, new_path):
        data = pyne.EVTData(new, raw)
        data.load_data()
        data.save_data()

if sys.argv[1] == '--chn':
    raw_chn = [f for f in raw_files if f.endswith('Chn')]
    raw_path = ['../data/{}'.format(f) for f in raw_chn]
    new_path = ['../data_np/{}'.format(f.split('.')[0]) for f in raw_chn]

    for raw, new in zip(raw_path, new_path):
        data = pyne.CHNData(new, raw)
        data.load_data()
        data.save_data()

