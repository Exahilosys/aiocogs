import asyncio
import threading
import operator

from . import helpers

__version__ = '0.0.0'

__all__ = ('sort', 'thread', 'ready', 'valve', 'cache', 'reduce', 'flatten')


__marker = object()


async def sort(generator, key = None, reverse = False):

    """
    Get a list if values sorted as yielded.
    """

    values = []

    compare = operator.lt if reverse else  operator.gt

    async for value in generator:

        index = helpers.rank(compare, values, value, key = key)

        values.insert(index, value)

    return values


async def thread(function, loop = None, factory = threading.Thread):

    """
    Run a function in a thread, wait for it to complete and get the result.
    """

    if not loop:

        loop = asyncio.get_event_loop()

    event = asyncio.Event(loop = loop)

    result = NotImplemented

    def observe():

        nonlocal result

        result = function()

        loop.call_soon_threadsafe(event.set)

    thread = factory(target = observe)

    thread.start()

    await event.wait()

    return result


async def ready(*tasks, loop = None):

    """
    Yield tasks as they complete.
    """

    if not loop:

        loop = asyncio.get_event_loop()

    left = len(tasks)

    queue = asyncio.Queue(loop = loop)

    for task in tasks:

        task.add_done_callback(queue.put_nowait)

    while left:

        yield await queue.get()

        left -= 1


@helpers.decorate
def valve(function, determine, state = set(), loop = None):

    """
    Only allow a function's execution during a period.
    `determine` returns seconds, called with the same arguments.
    """

    if not loop:

        loop = asyncio.get_event_loop()

    async def manage(coroutine):

        limit = await coroutine

        await asyncio.sleep(limit, loop = loop)

        state.remove(function)

    def observe(*args, **kwargs):

        if function in state:

            return

        state.add(function)

        functions = (determine, function)

        fetcher, execute = (function(*args, **kwargs) for function in functions)

        coroutines = (manage(fetcher), execute)

        managing, task = map(loop.create_task, coroutines)

        return task

    return observe


@helpers.decorate
def cache(function, determine, maxsize = float('inf'), loop = None):

    """
    Similar to an LRU cache except it can wait before deciding whether to cache
    results from the same inputs with a timeout; can be limited to a max size.
    `determine` returns seconds, called with state arguments.
    """

    if not loop:

        loop = asyncio.get_event_loop()

    states = {}

    events = {}

    async def wrapper(*args, **kwargs):

        state = (*args, *kwargs.items())

        try:

            event = events[state]

        except KeyError:

            pass

        else:

            timeout = await determine(*state)

            try:

                await asyncio.wait_for(event.wait(), timeout, loop = loop)

            except asyncio.TimeoutError:

                pass

        try:

            result = states[state]

        except KeyError:

            events[state] = asyncio.Event(loop = loop)

            try:

                result = await function(*args, **kwargs)

            finally:

                events.pop(state).set()

            if len(states) < maxsize:

                states[state] = result

        return result

    return wrapper


async def reduce(function, iterable, first = __marker):

    """
    Similar to an async version of functools.reduce except it's a generator
    yielding all results as they are computed. Iterate through for the final.
    """

    if first is __marker:

        result = await iterable.__anext__()

    else:

        result = first

    async for value in iterable:

        result = await function(result, value)

        yield result


async def flatten(generator,
                  apply = lambda value: value,
                  predicate = lambda value: True):

    """
    Convenience async version of builtins.list with apply and predicate.
    """

    return [apply(value) async for value in generator if predicate(value)]
