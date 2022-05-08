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


def fibonacci(n):
    """Return value of (n)th index of fibonacci sequence
    :param int n: index of the last fibonacci sequence
    :rtype func:
    """
    #################################################################
    #
    # Fast doubling Fibonacci algorithm (Python)
    #
    # Copyright (c) 2015 Project Nayuki. Public domain.
    # https://www.nayuki.io/page/fast-fibonacci-algorithms
    #

    # (Public) Returns F(n).
    def func(n):
        if n < 0:
            raise ValueError("Negative arguments not implemented")
        return _fib(n)[0]

    # (Private) Returns the tuple (F(n), F(n+1)).
    def _fib(n):
        if n == 0:
            return (0, 1)
        else:
            a, b = _fib(n // 2)
            c = a * (b * 2 - a)
            d = a * a + b * b
            if n % 2 == 0:
                return (c, d)
            else:
                return (d, c + d)

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
