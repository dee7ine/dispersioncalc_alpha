from dataclasses import dataclass
from math import sqrt, tan
from numba import jit
import matplotlib.pyplot as plt
from scipy import optimize
from Decorators import timeit
from numerical_methods.wave_class import Wave

@dataclass
class ShearWave(Wave):
    _omega: float
    _longitudinal_velocity: float
    _wave_number: float

    _wh0: float
    _cp0: float
    _h: float

    _p: float
    _q: float

    def __init__(self, omega: float,
                 longitudinal_velocity: float,
                 wave_number: float):
        """
        :param omega:
        :param longitudinal_velocity:
        :param wave_number:
        """

        self._omega = omega
        self._longitudinal_velocity = longitudinal_velocity
        self._wave_number = wave_number
        self._p = self._calculate_q(self, self._omega, self._longitudinal_velocity, self._wave_number)
        self._q = self._calculate_q(self, self._omega, self._longitudinal_velocity, self._wave_number)

    @timeit
    @jit(nopython=True)
    def _findzeros(self, freq_thickness_product: float,
                   phase_velocity: float,
                   thickness: float,
                   p: float,
                   q: float,
                   wave_number: float) -> None:

        '''
        RETURNS PHASE VELOCITY IN GIVEN INTERVAL
        :param freq_thickness_product:
        :param phase_velocity:
        :param thickness:
        :param p:
        :param q:
        :return:
        '''

@timeit
def main():
    '''
    recursive root finding function
    :return:
    '''
    pass

if __name__ == "__main__":
    main()