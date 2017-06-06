

import h5py


filename = 'run270.h5'

with h5py.File(filename, 'r') as f:
    print(list(f.attrs.items()))
    print(list(f.items()))

    adc_31 = f['adc_31']
    print(list(adc_31.attrs.items()))
    print(list(adc_31.items()))

