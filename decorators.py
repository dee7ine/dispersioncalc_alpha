import time
from datetime import datetime
from functools import wraps

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        results = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Function {func.__name__}{args}{kwargs} took {total_time:.4f} seconds to execute")
        return results
    return timeit_wrapper


def log(func):
    @wraps(func)
    def logger_wrapper(*args, **kwargs):
        called_time = datetime.now()
        results = func(*args, **kwargs)
        print(f"Function {func.__name__} called at {called_time.time()}")
        return results
    return logger_wrapper

