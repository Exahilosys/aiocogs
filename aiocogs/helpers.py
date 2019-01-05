

__all__ = ()


def rank(compare, iterable, root, key = None):

    """
    Determine the root's rank in an iterable.
    """

    index = 0

    for value in iterable:

        args = (root, value)

        if key:

            args = map(key, args)

        if not compare(*args):

            break

        index += 1

    return index


def decorate(value, position = 0):

    """
    Turn a function into a decorator.
    Assumes its first argument is callable.
    """

    def decorator(*args, **kwargs):

        def wrapper(function):

            return value(function, *args, **kwargs)

        return wrapper

    return decorator
