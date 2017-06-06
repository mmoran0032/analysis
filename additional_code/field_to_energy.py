#!/usr/bin/env python3


import sys

import numpy as np


K = 45.684  # 5U
K_gwen = (45.493 + 45.502 + 45.512) / 3

field = float(sys.argv[1])
charge = 1
mass = 1.007825

energy = (field * charge / (K * np.sqrt(mass)))**2
energy_gwen = (field * charge / (K_gwen * np.sqrt(mass)))**2
print('Energy [keV]: {:10.6f} ({:6.3f})'.format(energy, K))
print('Energy [keV]: {:10.6f} ({:6.3f}, Gwen)'.format(energy_gwen, K_gwen))

