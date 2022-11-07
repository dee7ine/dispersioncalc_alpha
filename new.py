from scipy import misc
from scipy import optimize
import matplotlib.pyplot as plt
#from sympy import symbols
from math import sqrt, tan
from Decorators import timeit, test_func


@timeit
def show_image() -> None:

    img = misc.face()

    plt.imshow(img)
    plt.show()

#@timeit
def test_function(x: float) -> float:

    return (x**2 - 1)

'''

DO NOT DELETE THIS COMMENT

the wavenumber k is numerically equal to ω/cp, where cp is the phase velocity of the
Lamb wave mode and ω is the circular frequency. The phase velocity is related to the
wavelength by the simple relation cp = (ω/2π)λ
'''
@timeit
def evaluate_sign(expression : float) -> int:
    '''

    :param expression:
    :return:
    '''

    if(expression < 0):
        return 1
    elif(expression > 0):
        return 0
    else: return 2

@timeit
def calculate_p(w: float, cl: float, k: float) -> float:

    return sqrt((w/cl)**2 - k**2)

@timeit
def calculate_q(w: float, ct: float, k: float) -> float:

    return sqrt((w/ct)**2 - k**2)

"""
(1) Choose a frequency–thickness product (ωh)0.
(2) Make an initial estimate of the phase velocity (cp)0.
(3) Evaluate the signs of each of the left-hand sides of (6.38) or (6.39) (assuming
they do not equal zero).
(4) Choose another phase velocity (cp)1 > (cp)0 and re-evaluate the signs of (6.38)
or (6.39).
88 Waves in Plates
(5) Repeat steps (3) and (4) until the sign changes. Because the functions involved
are continuous, a change in sign must be accompanied by a crossing through
zero. Therefore, a root m exists in the interval where a sign change occurs.
Assume that this happens between phase velocities (cp)n and (cp)n+1.
(6) Use some sort of iterative root-finding algorithm (e.g., Newton–Raphson,
bisection, …) to locate precisely the phase velocity in the interval (cp)n < cp <
(cp)n+1 where the LHS of the required equation is close enough to zero.
(7) After finding the root, continue searching at this ωh for other roots according
to steps (2) through (6).
(8) Choose another ωh product and repeat steps (2) through (7).
"""
@timeit
def lamb_wave_numerical(wh0: float, cp0: float, h: float, p: float, q: float, k: float) -> None:

    '''
    :param wh0:
    :param cp0:
    :param h:
    :param p:
    :param q:
    :return:
    '''

    LHS1 = tan(q*h) / q + 4 * k**2 * p * tan(p*h)/(q**2 - k**2)
    LHS2 = q*tan(q * h) / q + (q**2 - k**2) * tan(p * h) / 4 * k**2 * p

    if(LHS1 and LHS2 != 0):
        evaluate_sign(LHS1)
        evaluate_sign(LHS2)








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