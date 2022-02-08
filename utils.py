from time import time


def _time(func):
    def wrapper(*args, **dargs):
        start = time()
        result = func(*args, **dargs)
        end = time()
        print(f"{func.__name__} timed: {(end - start)}")
        return result

    return wrapper
