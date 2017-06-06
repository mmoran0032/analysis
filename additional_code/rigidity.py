#!/usr/bin/env python3


import sys

import numpy as np


amu_to_MeV = 931.49432  # MeV/c^2
c = 299792458.0  # m/s


def Brho(E, A, q):  # Tm
    return A * np.sqrt((E / A)**2 + 2 * E * amu_to_MeV / A) / (q * c) * 1e6


def Erho(E, q):  # MV
    return 2 * E / q


if __name__ == '__main__':
    E, A, q = map(float, sys.argv[1:])
    print(sys.argv)
    Br = Brho(E, A, q)
    Er = Erho(E, q)
    print('Bp = {:.4f} Tm\nEp = {:.4f} MV'.format(Br, Er))

