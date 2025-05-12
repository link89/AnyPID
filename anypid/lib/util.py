import asyncio
import functools


def async_to_sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(func(*args, **kwargs))
        else:
            coro = func(*args, **kwargs)
            return loop.run_until_complete(coro)
    return wrapper
