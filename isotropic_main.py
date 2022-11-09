from scipy import misc
from scipy import optimize
import matplotlib.pyplot as plt
#from sympy import symbols
from math import sqrt, tan
from Decorators import timeit, test_func
from numba import jit

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
        self._w = w
        self._cl = cl
        self._k = k

        self._p = self._calculate_q(self, self._w, self._cl , self._k)
        self._q = self._calculate_q(self, self._w, self._cl, self._k)
        #self._lamb_wave_numerical(self)

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
        '''
        :param expression:
        :return:
        '''

        if (expression < 0):
            return 1
        elif (expression > 0):
            return 0
        else:
            return 2

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

        if (lhs_1 and lhs_2 != 0):
            self._evaluate_sign(self, lhs_1)
            self._evaluate_sign(self, lhs_2)
        else:
            pass

@timeit
def show_image() -> None:

    img = misc.face()

    plt.imshow(img)
    plt.show()

#@timeit
def test_function(x: float) -> float:

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