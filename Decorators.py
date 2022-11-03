import time
from functools import wraps


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        results = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Function {func.__name__}{args}{kwargs} took {total_time:.8f} seconds to execute")
        return results
    return timeit_wrapper

@timeit
def test_func(a, b):
    return a+b

test_func(1,2)
