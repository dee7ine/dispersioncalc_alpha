import unittest
from Decorators import timeit, log

@timeit
@log
def test_func(a : int, b : int, times: int) -> int:
    """
    :param a:
    :param b:
    :return:
    """
    for _ in range(0, times):
        a+=b

    return a

class MyTestCase(unittest.TestCase):
    def test_timeit_basic(self):

        test_func(1, 2, times = 1000)
        test_func(58, 59, times = 1000)
        test_func(412, 0, times = 1000)
        test_func(581958215, 51285285050, times = 41248888)

if __name__ == '__main__':
    unittest.main()
