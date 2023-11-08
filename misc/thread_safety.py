import functools
from threading import Lock

global_lock = Lock()


def thread_safe_function(lock: Lock = None):
    if lock is None:
        lock = global_lock

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper

    return decorator
