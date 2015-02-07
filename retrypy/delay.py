from random import uniform as _random


def random(min_seconds=0, max_seconds=5):
    """Return a random number of seconds

    :param float min_seconds: Minimum delay in seconds
    :param float max_seconds: Maximum delay in seconds
    :rtype func:
    """
    def func(_):
        return _random(min_seconds, max_seconds)

    return func


def exponential(start_at):
    """Return and exponentially increasing value

    :param float start_at: Initial delay in seconds
    :rtype func:
    """
    def func(count):
        count -= 1
        return start_at * (2**count)

    return func


def incremental(start_at, step=1):
    """Return and incrementally larger value

    :param float start_at: Initial delay in seconds
    :param float step: Amount to increase delay by in seconds
    :rtype func:
    """
    def func(count):
        count -= 1
        return start_at + count*step

    return func
