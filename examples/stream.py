
"""
Call with something.
This will take 3 secs.
On average, this should take less than `Σx` seconds where `x ∈ [1, limit]`
"""

import asyncio
import aiocogs

loop = asyncio.get_event_loop()

stream = aiocogs.Stream(loop = loop)

@stream.sub(True)
async def execute(value):

    print(0, value)

    await asyncio.sleep(1)

@stream.sub(False)
async def execute(value):

    print(1, value)

    await asyncio.sleep(1)

@stream.sub(True)
async def execute(value):

    print(2, value)

    await asyncio.sleep(1)

@stream.sub(True)
async def execute(value):

    print(3, value)

    await asyncio.sleep(1)

@stream.sub(False)
async def execute(value):

    print(4, value)

    await asyncio.sleep(1)

async def main(value):

    """
    Start the stream.
    """

    await stream.start(value)

if __name__ == '__main__':

    import sys

    value = ' '.join(sys.argv[1:])

    coroutine = main(value)

    try:

        loop.run_until_complete(coroutine)

    except KeyboardInterrupt:

        pass
