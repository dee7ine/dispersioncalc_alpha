import unittest
import dis
from numerical_methods.lamb_waves import LambWave

def add(a):
    for _ in range(0, 100):
        a+=a
    return a

class MyTestCase(unittest.TestCase):
    def test_something(self):
        dis.dis(add)
        dis.dis(LambWave.__init__)
        dis.dis(LambWave._lamb_wave_calculate)



if __name__ == '__main__':
    unittest.main()
