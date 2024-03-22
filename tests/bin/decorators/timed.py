import functools
import time

from src.logger import Logger


def timed(logger: Logger = None):
    def inner_timer_decorator(func):
        start_time = time.perf_counter()

        @functools.wraps(func)
        def timer_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        end_time = time.perf_counter() - start_time
        logger.debug(f"Finished {func.__name__} in {end_time:.5f} seconds")
        return timer_wrapper

    return inner_timer_decorator
