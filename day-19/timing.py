from functools import wraps
from time import time
from typing import Callable


def timing(f: Callable):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f"Time taken for {f.__name__} [sec]: {te - ts}")
        return result
    return wrap
