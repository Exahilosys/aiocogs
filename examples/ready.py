
"""
Simple `ready` demonstration.
Call with `[size] [limit]` like: `10 5`
This should always take no more than `limit` seconds.
"""

import asyncio
import aiocogs
import random

loop = asyncio.get_event_loop()

async def execute(wait):

    """
    Just wait for a bit.
    """

    await asyncio.sleep(wait)

async def main(size, limit):

    """
    Calculate random periods and pass them to execute.
    Yield their tasks as they complete.
    """

    # need this to be index-able for later
    waits = tuple(random.randrange(1, limit) for index in range(size))

    print('order', *waits)

    coroutines = map(execute, waits)

    # this too so we can track our waits
    tasks = tuple(map(loop.create_task, coroutines))

    async for task in aiocogs.ready(*tasks):

        # sanity check
        result = task.result()

        index = tasks.index(task)

        wait = waits[index]

        print(f'finished {wait}')

if __name__ == '__main__':

    import sys

    args = map(int, sys.argv[1:])

    coroutine = main(*args)

    try:

        loop.run_until_complete(coroutine)

    except KeyboardInterrupt:

        pass
