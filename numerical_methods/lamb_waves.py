from dataclasses import dataclass
from math import sqrt, tan
from numba import jit
import matplotlib.pyplot as plt
from scipy import optimize
from decorators import timeit

@dataclass
class IsotropicMain():
    _omega: float
    _longitudinal_velocity: float
    _wave_number: float

    _wh0: float
    _cp0: float
    _h: float

    _p: float
    _q: float

    def __init__(self, omega: float, longitudinal_velocity: float, wave_number: float):
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
    def _calculate_p(self,
                     omega: float,
                     longitudinal_velocity: float,
                     wave_number: float) -> float:
        return sqrt((omega / longitudinal_velocity) ** 2 - wave_number ** 2)

    @timeit
    @jit(nopython=True)
    def _calculate_q(self,
                     omega: float,
                     ct: float,
                     k: float) -> float:
        return sqrt((omega / ct) ** 2 - k ** 2)

    @timeit
    @jit(nopython=True)
    def _evaluate_sign(self,
                       expression: float) -> bool:
        return expression > 0

    def _sign_changed(self,
                      p1: bool,
                      c1: bool) -> bool:
        return p1 is c1

    @timeit
    @jit(nopython=True)
    def _lamb_wave_numerical(self, freq_thickness_product: float,
                             phase_velocity: float,
                             thickness: float,
                             p: float,
                             q: float,
                             wave_number: float) -> None:
        '''
        :param freq_thickness_product:
        :param phase_velocity:
        :param thickness:
        :param p:
        :param q:
        :return:
        '''

        lhs_1 = tan(q * thickness) / q + 4 * wave_number ** 2 * p * tan(p * thickness) / (q ** 2 - wave_number ** 2)
        lhs_2 = q * tan(q * thickness) / q + (q ** 2 - wave_number ** 2) * tan(p * thickness) / 4 * wave_number ** 2 * p

        current1 = self._evaluate_sign(self, lhs_1)
        current2 = self._evaluate_sign(self, lhs_2)

        while (not self._sign_changed(self, prev1, current1) or not self._sign_changed(prev2, current2)):
            """

            DO NOT DELETE THIS COMMENT

            loop until the sign of one of the
            evaluated left hands sides changes sign
            """
            if ((lhs_1 and lhs_2) != 0):
                prev1 = self._evaluate_sign(self, lhs_1)
                prev2 = self._evaluate_sign(self, lhs_2)
            else:
                pass
            self._sign_changed(current1, prev1)
            self._sign_changed(current2, prev2)
@timeit
def main():
    '''
    recursive root finding function
    :return:
    '''
    pass

if __name__ == "__main__":
    main()