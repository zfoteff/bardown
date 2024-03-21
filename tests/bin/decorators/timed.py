import functools
import time

from src.logger import Logger


def timed(logger: Logger = None):
    def inner_timer_decorator(func):
        @functools.wraps(func)
        def timer_wrapper(*args, **kwargs):
            start_time = time.perf_counter() 
            func(*args, **kwargs)
            end_time = time.perf_counter() - start_time
            return f"Finished {func.__name__} in {end_time:.3f} seconds"
        logger.info()
        return timer_wrapper
    return inner_timer_decorator