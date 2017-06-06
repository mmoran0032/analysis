#!/usr/bin/env python3


import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad


try:
    plot = sys.argv[1] == '--p'
except IndexError:
    plot = False

array_file = np.load('arrays/array_test.npz')
counts = array_file['counts']  # n bin contents
energies = array_file['energies']  # n bin fronts

low = 0  # keV
high = 7000  # keV
energy_width = 20  # keV
# (100, 6000, 10) -- 591 bins
bin_count = int((high - low) / energy_width + 1)
energy_array = np.linspace(low, high, bin_count)
bin_locations = np.searchsorted(energies, energy_array)

# create array for counts
rebinned_counts = np.zeros(bin_count)

for value, bin_low, bin_high in zip(counts, energies, energies[1:]):
    bin = (bin_low, bin_high)
    # print(value, bin)
    if bin_low > high:
        break
    insert = np.searchsorted(energy_array, bin)
    if insert[0] == insert[1]:  # all contained in a single new bin
        rebinned_counts[insert[0]] += value
    else:  # need to split counts
        if value != 0:
            e_range = [bin[0] - 2 * energy_width, bin[0] + 2 * energy_width]
            locations = np.searchsorted(energies, e_range)
            x = energies[locations[0]:locations[1]]
            y = counts[locations[0]:locations[1]]
            pars = np.polyfit(x, y, deg=3)

            # estimate p
            poly = np.poly1d(pars)
            p = (quad(poly, bin_low, energy_array[insert[0]])[0] /
                 quad(poly, *bin)[0])
            # print('p = ', p, energy_array[insert], bin)
            front_bin = np.random.binomial(1, p, size=value).sum()
            back_bin = value - front_bin
            rebinned_counts[insert[0]] += front_bin
            rebinned_counts[insert[1]] += back_bin

if plot:
    plt.semilogy(energy_array, rebinned_counts,
                 nonposy='clip', lw=1, linestyle='steps-mid')
    plt.semilogy(energies, counts,
                 nonposy='clip', lw=1, linestyle='steps-mid')
    plt.ylim(1, 10000)
    plt.xlim(low, high)
    plt.show()

assert rebinned_counts.sum() == counts.sum()
print(energy_array[rebinned_counts.argmax()], energies[counts.argmax()])

np.savez('arrays/relocated_check.npz',
         counts=rebinned_counts, energies=energy_array)
