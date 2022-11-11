from scipy import misc
from scipy import optimize
from dataclasses import dataclass
import matplotlib.pyplot as plt
from math import sqrt, tan
from Decorators import timeit, test_func
from numba import jit

@dataclass
class IsotropicMain():

    _w: float
    _cl: float
    _k: float

    _wh0: float
    _cp0: float
    _h: float

    _p: float
    _q: float

    def __init__(self,  w: float, cl: float, k: float):
        """
        :param w:
        :param cl:
        :param k:
        """

        self._w = w
        self._cl = cl
        self._k = k
        self._p = self._calculate_q(self, self._w, self._cl , self._k)
        self._q = self._calculate_q(self, self._w, self._cl, self._k)

    @timeit
    @jit(nopython = True)
    def _calculate_p(self,
                     w: float,
                     cl: float,
                     k: float) -> float:
        return sqrt((w / cl) ** 2 - k ** 2)

    @timeit
    @jit(nopython = True)
    def _calculate_q(self,
                     w: float,
                     ct: float,
                     k: float)-> float:
        return sqrt((w / ct) ** 2 - k ** 2)

    @timeit
    @jit(nopython = True)
    def _evaluate_sign(self,
                      expression: float) -> int:
        if (expression < 0):
            return True
        elif (expression > 0):
            return False

    def _sign_changed(self,
                      p1: bool,
                      c1: bool) -> bool:
        return p1 is c1

    @timeit
    @jit(nopython=True)
    def _lamb_wave_numerical(self, wh0: float,
                            cp0: float,
                            h: float,
                            p: float,
                            q: float,
                            k: float) -> None:
        '''
        :param wh0:
        :param cp0:
        :param h:
        :param p:
        :param q:
        :return:
        '''

        lhs_1 = tan(q * h) / q + 4 * k ** 2 * p * tan(p * h) / (q ** 2 - k ** 2)
        lhs_2 = q * tan(q * h) / q + (q ** 2 - k ** 2) * tan(p * h) / 4 * k ** 2 * p

        current1 = self._evaluate_sign(self, lhs_1)
        current2 = self._evaluate_sign(self, lhs_2)

        while(self._sign_changed(self, prev1, current1) or self._sign_changed(prev2, current2)):
            """
            
            DO NOT DELETE THIS COMMENT
            
            loop until the sign of one of the
            evaluated left hands sides changes sign
            """
            if ((lhs_1 and lhs_2) != 0):
                prev1 = self._evaluate_sign(self, lhs_1)
                prev2 = self._evaluate_sign(self, lhs_2)
            else:
                raise ArithmeticError
            self._sign_changed(prev1, prev2)

@timeit
def show_image() -> None:
    """
    :return:
    """

    img = misc.face()

    plt.imshow(img)
    plt.show()

#@timeit
def test_function(x: float) -> float:
    """
    :param x:
    :return:
    """

    return (x**2 - 1)

@timeit
def main():
    '''
    recursive root finding function
    :return:
    '''
    root  = optimize.bisect(test_function, 0, 2)
    print(root)

if __name__ == "__main__":
    main()