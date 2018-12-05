
"""
Simple `cache` demonstration.
Call with `[size] [limit]` like: `10 5`
On average, this should take `Σx` where `x ∈ [1, limit]`
"""

import asyncio
import aiocogs
import random

loop = asyncio.get_event_loop()

async def period(*state):

    """
    Dynamically return timeouts according to the state.
    """

    # wait until last function calls have completed
    # passing 0 would have the cache not wait at all
    return None

@aiocogs.cache(period)
async def execute(wait):

    """
    Just wait for a bit.
    """

    await asyncio.sleep(wait)

async def main(size, limit):

    """
    Calculate random periods and pass them to the cached function.
    """

    for index in range(size):

        wait = random.randint(1, limit)

        start = loop.time()

        # this should finish right away (without waiting)
        # for periods that have already been used, 3 will
        # wait 3 seconds first time and then 0 afterwards
        await execute(wait)

        elapsed = round(loop.time() - start, 1)

        print(f'finished {wait}', f'after {elapsed}')

if __name__ == '__main__':

    import sys

    args = map(int, sys.argv[1:])

    coroutine = main(*args)

    try:

        loop.run_until_complete(coroutine)

    except KeyboardInterrupt:

        pass
