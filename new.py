from scipy import misc
from scipy import optimize
import matplotlib.pyplot as plt
from sympy import symbols
from math import sqrt

def show_image() -> None:

    img = misc.face()

    plt.imshow(img)
    plt.show()


def test_function(x: float) -> float:
    return (x**2 - 1)

'''

DO NOT DELETE THIS COMMENT

the wavenumber k is numerically equal to ω/cp, where cp is the phase velocity of the
Lamb wave mode and ω is the circular frequency. The phase velocity is related to the
wavelength by the simple relation cp = (ω/2π)λ
'''
def calculate_p(w: float, cl: float, k: float) -> float:

    return math.sqrt((w/cl)**2 - k**2)

def calculate_q(w: float, ct: float, k: float) -> float:

    return math.sqrt((w/ct)**2 - k**2)

def main():
    '''
    recursive root finding function
    :return:
    '''
    root  = optimize.bisect(test_function, 0, 2)
    print(root)


if __name__ == "__main__":
    main()