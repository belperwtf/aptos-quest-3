import asyncio
import random

from config import RETRY_ATTEMPTS

def async_retry(async_func):
    async def wrapper(*args, **kwargs):
        tries, delay = RETRY_ATTEMPTS, 1.5
        while tries > 0:
            try:
                return await async_func(*args, **kwargs)
            except Exception:
                tries -= 1
                if tries <= 0:
                    raise
                await asyncio.sleep(delay)

                delay *= 2
                delay += random.uniform(0, 1)
                delay = min(delay, 10)

    return wrapper
