import functools
import time
from src.logger import Logger

def timed(func, logger: Logger):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter() 
        value = func(*args, **kwargs)
        end_time = time.perf_counter() - start_time
        logger.info(f"Finished {func.__name__} in {end_time:.3f} seconds")
        return value
    return wrapper_timer