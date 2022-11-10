"""
11.10 - deefi

testing optimization capabilities of numba
"""

import time
import unittest
from numba import jit

start1 = time.perf_counter()
@jit(nopython = True)
def jit_func(a, b):
    for _ in range(100):
         a+=b
stop1 = time.perf_counter()


start2 = time.perf_counter()
@jit
def jit_python(a, b):
    for _ in range(100):
         a+= b
stop2 = time.perf_counter()


start3 = time.perf_counter()
def no_jit(a, b):
    for _ in range(100):
         return a + b
stop3 = time.perf_counter()


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertGreater(stop1 - start1, stop2 - start2,
                           f"Jit_python : {jit_python(5,4)} s, jit {jit_func(5,4)} s")  # add assertion here
        self.assertGreater(stop1 - start1, stop3 - start3, "test")

if __name__ == '__main__':
    unittest.main()
