
"""
Call with nothing.
This will take 2 seconds to start and continue in perpetuity.
"""

import asyncio
import aiocogs

loop = asyncio.get_event_loop()

signal = asyncio.sleep(2)

count = 0

@aiocogs.infinite(signal = signal)
async def execute(): # no arguments

    global count

    print('sleep', count)

    count += 1

    await asyncio.sleep(count)

if __name__ == '__main__':

    import sys

    print('start')

    try:

        loop.run_forever()

    except KeyboardInterrupt:

        pass
