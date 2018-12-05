
"""
Simple `thread` demonstration.
Call with `[size] [limit]` like: `10 5`
This should always take no more than `limit` seconds.
"""

import asyncio
import aiocogs
import time
import functools
import random

loop = asyncio.get_event_loop()

def execute(wait):

    """
    Just wait blockingly for a bit.
    """

    time.sleep(wait)

async def main(size, limit):

    """
    Calculate random periods and create functions needing no more arguments.
    Use `thread` and `ready` to wait and yield their tasks as they complete.

    The idea here is that if the functions truly block; 3 should, for example,
    complete 4 seconds after start following a 1. Which does not happen here.
    """

    functions = []

    for index in range(size):

        wait = random.randint(1, limit)

        # aiocogs.thread will call the function
        # with no arguments, hence why we set it up
        # beforehand using empty-argument functions
        function = functools.partial(execute, wait)

        functions.append(function)

    # careful, thread returns coroutines!
    coroutines = map(aiocogs.thread, functions)

    # need this to be index-able for later
    tasks = tuple(map(loop.create_task, coroutines))

    # will yield tasks as they complete
    async for task in aiocogs.ready(*tasks):

        # sanity check
        result = task.result()

        function = functions[tasks.index(task)]

        (wait,) = function.args

        print(f'finished {wait}')

if __name__ == '__main__':

    import sys

    args = map(int, sys.argv[1:])

    coroutine = main(*args)

    try:

        loop.run_until_complete(coroutine)

    except KeyboardInterrupt:

        pass
