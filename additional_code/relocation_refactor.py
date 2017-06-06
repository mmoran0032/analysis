#!/usr/bin/env python3


import numpy as np
from scipy.integrate import quad


array_file = np.load('arrays/array_test.npz')
counts = array_file['counts']  # n bin contents
energies = array_file['energies']  # n bin fronts

low = 0  # keV
high = 7000  # keV
energy_width = 20  # keV
# (100, 6000, 10) -- 591 bins
bin_count = int((high - low) / energy_width + 1)
energy_array = np.linspace(low, high, bin_count)
rebinned_counts = np.zeros(bin_count)
assert energy_array.size == rebinned_counts.size

energies = np.append(energies, 2 * energies[-1] - energies[-2])
energies_stack = np.vstack((energies[:-1], energies[1:])).T
insert = np.searchsorted(energy_array, energies_stack)

# print(energies_stack)
# print(insert)
# print(insert[:, 0] == insert[:, 1])
mask = insert[:, 0] == insert[:, 1]
values = counts[mask]

easy_counts = np.where(mask, counts, 0)
hard_counts = np.where(mask, 0, counts)
print(easy_counts.size, easy_counts.sum(), counts.sum())
print(counts.sum() - easy_counts.sum())  # about 10% of the counts

# rebinned_counts[insert_index] += easy_counts[mask_index]
# handle easy counts
easy = np.vstack((insert[:, 0], easy_counts)).T
easy = easy[np.where(easy[:, 1])]
for insert_index, value in easy:
    rebinned_counts[insert_index] += value
print(rebinned_counts.sum())

# handle hard counts

# create multi-D array that contains all necessary information
full = np.vstack((*insert.T, hard_counts, *energies_stack.T)).T
full = full[np.where(full[:, 2] != 0)]

for front_index, back_index, value, front_energy, back_energy in full:
    # print(front_index, back_index, value, front_energy, back_energy)
    locations = [energy_array[int(front_index) - 2],
                 energy_array[int(front_index) + 2]]
    energy_locations = np.searchsorted(energies, locations)
    pars = np.polyfit(np.take(energies, np.arange(*energy_locations)),
                      np.take(counts, np.arange(*energy_locations)),
                      deg=3)

    # estimate p
    poly = np.poly1d(pars)
    p = (quad(poly, front_energy, energy_array[int(front_index)])[0] /
         quad(poly, front_energy, back_energy)[0])
    # print('p = ', p, energy_array[insert], bin)
    front_bin = np.random.binomial(1, p, size=int(value)).sum()
    back_bin = value - front_bin
    rebinned_counts[int(front_index)] += front_bin
    rebinned_counts[int(back_index)] += back_bin
print(rebinned_counts.sum())

array_file = np.load('arrays/relocated_check.npz')
counts = array_file['counts']  # n bin contents
energies = array_file['energies']  # n bin fronts

assert counts.size == rebinned_counts.size
assert (energies == energy_array).all()

diffs = (counts - rebinned_counts)
print(diffs.sum(), counts.max())
