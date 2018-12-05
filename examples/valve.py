
"""
Simple `valve` demonstration.
Call with `[size] [limit]` like: `10 5`
This should always take no more than `size + limit` seconds.
"""

import asyncio
import aiocogs
import random

loop = asyncio.get_event_loop()

wait = 4

async def period(*args, **kwargs):

    """
    Dynamically return timeouts according to the state.
    """

    return wait

@aiocogs.valve(period)
async def execute(wait):

    """
    Just wait for a bit.
    """

    await asyncio.sleep(wait)

    print('complete')

async def main(size, limit):

    index = 0

    tasks = []

    while True:

        # careful, this is not a coroutine function!
        # it will always return either None or a task,
        # signifiying whether the attched function was
        # executed or ignored respectively
        task = execute(limit)

        if not task is None:

            # this mean the valve
            # was open, got called
            tasks.append(task)

        print(index, not task is None)

        index += 1

        if index > size:

            break

        await asyncio.sleep(1)

    # the reason we don't use aiocogs.ready here is
    # that we know tasks that got in first will finish
    # first as well, all of them wait for the same time
    for task in tasks:

        # sanity check
        result = await task

if __name__ == '__main__':

    import sys

    args = map(int, sys.argv[1:])

    coroutine = main(*args)

    try:

        loop.run_until_complete(coroutine)

    except KeyboardInterrupt:

        pass
