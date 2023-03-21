"""
=========================================================================
Tool for dispersion calculation

Created by Bartlomiej Jargut
https://github.com/dee7ine

Lamb wave class implemented by Francisco Rotea
https://github.com/franciscorotea
-------------------------------------------------------------------------
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

=========================================================================
"""


import time
from datetime import datetime
from functools import wraps
from typing import Callable


def timeit(func: Callable) -> Callable:
    @wraps(func)
    def timeit_wrapper(*args, **kwargs) -> Callable:
        start_time = time.perf_counter()
        results = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Function {func.__name__}{args}{kwargs} took {total_time:.4f} seconds to execute")
        return results
    return timeit_wrapper


def ui_log(func: Callable) -> Callable:
    """
    Decorator used for logging to
    GUI console. For some reason it
    is not working when used any kind
    of event


    :param func:
    :return:
    """

    def logger_wrapper(*args, **kwargs) -> Callable:

        results = func(*args, **kwargs)
        print(f"{datetime.now().isoformat(' ', 'seconds')}:"
              f" Function {func.__name__} is running")

        return results
    return logger_wrapper
