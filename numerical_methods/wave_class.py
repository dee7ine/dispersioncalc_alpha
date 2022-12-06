from math import sqrt
from numba import jit
from decorators import timeit
from abc import ABC, abstractmethod
import numpy as np

class Wave(ABC):
    _omega: float
    _longitudinal_velocity: float
    _wave_number: float

    _wh0: float
    _cp0: float
    _h: float

    _p: float
    _q: float

    def __init__(self, omega: float, longitudinal_velocity: float, wave_number: float, thickness: float, material):
        """

        :param omega:
        :param longitudinal_velocity:
        :param wave_number:
        :param thickness:
        """

        self._material = material


        self._d = thickness/1e3
        self._h = (thickness / 2) / 1e3
        self._omega = omega
        self._longitudinal_velocity = longitudinal_velocity
        self._wave_number = wave_number
        self._p = self._calculate_q(self, self._omega, self._longitudinal_velocity, self._wave_number)
        self._q = self._calculate_q(self, self._omega, self._longitudinal_velocity, self._wave_number)

    @timeit
    @jit(nopython=True)
    def _calculate_constants(self, vp: float, fd: float) -> float:
        """

        :param vp: phase velocity
        :param fd: frequency-thickness product
        :return:
        """

        omega = 2 * np.pi * (fd/self._d)

        k = omega/vp

        p = sqrt((omega / longitudinal_velocity) ** 2 - wave_number ** 2)
        q = sqrt((omega / ct) ** 2 - k ** 2)

        return k, p, q


    @abstractmethod
    def _calculate(self, freq_thickness_product: float,
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

        pass


@timeit
def main():
    '''
    recursive root finding function
    :return:
    '''
    pass


if __name__ == "__main__":
    main()