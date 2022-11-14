import unittest
import dis
from numerical_methods.lamb_waves import IsotropicMain

def add(a):
    for _ in range(0, 100):
        a+=a
    return a

class MyTestCase(unittest.TestCase):
    def test_something(self):
        dis.dis(add)
        dis.dis(IsotropicMain.__init__)
        dis.dis(IsotropicMain._lamb_wave_numerical)



if __name__ == '__main__':
    unittest.main()
