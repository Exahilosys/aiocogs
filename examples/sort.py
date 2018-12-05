
"""
Simple `sort` demonstration.
Call with `[size] [limit]` like: `10 5`
"""

import asyncio
import aiocogs
import random

loop = asyncio.get_event_loop()

async def convert(generator):

    """
    Generator to async-generator conversion.
    """

    for value in generator:

        yield value

async def main(size, limit):

    """
    Calculate random periods and convert their container to an async-generator.
    Sort the generator in reverse.
    """

    # tuple-ing for demonstration purposes only; could be a generator
    values = tuple(random.randrange(1, limit) for index in range(size))

    print('values', *values)

    generator = convert(values)

    # this also accepts a key just like builtins.sorted
    final = await aiocogs.sort(generator, reverse = True)

    print('finals', *final)

if __name__ == '__main__':

    import sys

    args = map(int, sys.argv[1:])

    coroutine = main(*args)

    try:

        loop.run_until_complete(coroutine)

    except KeyboardInterrupt:

        pass
