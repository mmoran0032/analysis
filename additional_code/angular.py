#!/usr/bin/env python3


from collections import namedtuple

from mpmath import coulombf, coulombg
import numpy
import sympy.physics.wigner as wigner
# from sympy import legendre


Particle = namedtuple('particle', 'mass charge spin parity')


def coefficients(j_1, l_1, J, l_2, j_2, *,
                 particles=None, r=0, pure_1=True, pure_2=True):
    n_max = min(2 * l_1, 2 * l_2, 2 * J)
    print('n_max: {}'.format(n_max))
    return [b(n, l_1, l_2, j_1, j_2, J, pure_1, pure_2)
            for n in range(0, n_max + 2, 2)]


def b(n, L_1, L_2, j_1, j_2, J, pure_1=True, pure_2=True):
    if n == 0:
        return 1
    else:
        temporary = 1
        if pure_1:
            temporary *= a_pure(n, L_1) * A_pure(n, L_1, j_1, J)
        else:
            temporary *= mixed(n)
        if pure_2:
            temporary *= a_pure(n, L_2) * A_pure(n, L_2, j_2, J)
        else:
            temporary *= mixed(n)
        return temporary


def F(n, L_1, L_2, j, J):
    root = numpy.sqrt((2 * L_1 + 1) * (2 * L_2 + 1) * (2 * J + 1))
    clebsch = wigner.clebsch_gordan(L_1, L_2, n, 1, -1, 0)
    racah = wigner.racah(J, J, L_1, L_2, n, j)
    return (-1)**(j - J - 1) * root * clebsch * racah


def a_pure(n, L):
    return 2 * L * (L + 1) / ((2 * L * (L + 1) - n * (n + 1)))


def A_pure(n, L, j, J):
    return F(n, L, L, j, J)


def mixed(n):
    raise NotImplemented


def phase_shift(L, r, p_1, p_2, E):
    _eta, _rho = sommerfeld(p_1, p_2, E), rho(r, p_1, p_2, E)
    sum_term = sum(numpy.arctan(_eta / n) for n in range(1, L))
    return sum_term - numpy.atan(coulombf(L, _eta, _rho) /
                                 coulombg(L, _eta, _rho))


def rho(r, p_1, p_2, E):
    root = numpy.sqrt(p_1.mass * p_2.mass * E / (p_1.mass + p_2.mass))
    return 0.218735 * r * root


def sommerfeld(p_1, p_2, E):
    root = numpy.sqrt(p_1.mass * p_2.mass / ((p_1.mass + p_2.mass) * E))
    return 0.157489 * p_1.charge * p_2.charge * root
