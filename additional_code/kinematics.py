

from collections import namedtuple

import numpy as np


Isotope = namedtuple('Isotope', 'symbol mass delta')
AMU_TO_MEV = 931.494061


class KinCalc:
    def __init__(self, beam, target, ejectile, recoil, *,
                 ejectile_excitation=0, recoil_excitation=0, lab_angle=0):
        self.beam = beam
        self.target = target
        self.ejectile = ejectile
        self.ejectile_excitation = ejectile_excitation
        self.recoil = recoil
        self.recoil_excitation = recoil_excitation
        self.lab_angle = lab_angle
        self.convert_masses()

    def convert_masses(self):
        self.beam = self._convert_single(self.beam)
        self.target = self._convert_single(self.target)
        self.ejectile = self._convert_single(self.ejectile)
        self.recoil = self._convert_single(self.recoil)

    def _convert_single(self, iso):
        return Isotope(iso.symbol, iso.mass * AMU_TO_MEV, iso.delta)

    def calculation(self, beam_energy):
        w15 = np.sqrt(self.mu_in**2 + 2 * beam_energy * self.target.mass)
        x15 = w15 + self.q_value - self.mu_in + self.mu_out
        y15 = (x15**2 + self.mu_out *
               (self.ejectile.mass - self.recoil.mass)) / (2 * x15)
        v15 = (np.sqrt(beam_energy**2 + 2 * beam_energy * self.beam.mass) /
               (self.mu_in + beam_energy))
        aa15 = (y15 / self.ejectile.mass)**2 * (1 - v15**2)
        angle = np.cos(self.lab_angle)
        ac16 = -v15 * angle
        ad16 = aa15 + ac16**2
        af16 = ac16**2 - ad16 * (1 - aa15)
        ag16 = (np.sqrt(af16) - ac16) / ad16
        return self.ejectile.mass * (1 / np.sqrt(1 - ag16**2) - 1)

    @property
    def mu_in(self):
        return self.beam.mass + self.target.mass

    @property
    def mu_out(self):
        return self.ejectile.mass + self.recoil.mass

    @property
    def lab_angle(self):
        return self._lab_angle

    @lab_angle.setter
    def lab_angle(self, value):
        if 0 <= value <= 180:
            self._lab_angle = np.radians(value)
        else:
            print('Value {} out of bounds [0, 180], using 0'.format(value))
            self._lab_angle = 0

    @property
    def q_value(self):
        return (self.beam.delta + self.target.delta -
                self.ejectile.delta - self.recoil.delta)


if __name__ == '__main__':
    import sys

    beam = Isotope('H1', 1.00782503207, 7.289)
    target = Isotope('Al27', 26.981538627, -17.196)
    ejectile = Isotope('He4', 4.00260325415, 2.425)
    recoil = Isotope('Mg24', 23.985041699, -13.933)

    calc = KinCalc(beam, target, ejectile, recoil)
    energy = float(sys.argv[1])
    print(calc.calculation(energy))
