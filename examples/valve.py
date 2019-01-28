
"""
Call with `[size]` like: `10`
This should always take no more than `size ` seconds.
"""

import asyncio
import aiocogs
import random

loop = asyncio.get_event_loop()

wait = 4

@aiocogs.valve(wait)
async def execute(index):

    """
    Just wait for a bit.
    """

    print('called', index)

async def main(size, limit):

    """
    Call the valve, check if there was a call and handle the tasks returned.
    """

    index = 0

    while True:

        # this is not the result of the call!
        # it's either a coroutine or None,
        # depending on whether the attached function
        # was executed or ignored respectively
        coroutine = execute(index)

        if coroutine:

            # this means the valve
            # was open, we can await
            await coroutine

        index += 1

        if index > size:

            break

        await asyncio.sleep(1)

if __name__ == '__main__':

    import sys

    args = map(int, sys.argv[1:])

    coroutine = main(*args)

    try:

        loop.run_until_complete(coroutine)

    except KeyboardInterrupt:

        pass
