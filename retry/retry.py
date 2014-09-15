import time
from functools import partial, wraps
from numbers import Number
from random import random


def random_delay(min_seconds=0, max_seconds=5):
    def func(count):
        return random(min_seconds, max_seconds)

    return func


def doubling_delay(start_at):
    def func(count):
        return start_at * (2**count)

    return func


def linear_delay(start_at, step=1):
    def func(count):
        return start_at + count*step

    return func


def _sleep(n):
    time.sleep(n)


def _wait(wait, count):
    if not isinstance(wait, Number):
        wait = wait(count - 1)

    _sleep(wait)


def _retry(func, exceptions, check_for_retry, times, wait):
    previous_exception = None
    for n in xrange(1, times + 1):
        try:
            return func()
        except tuple(exceptions) as e:
            if check_for_retry and not check_for_retry(e, n):
                raise e
            previous_exception = e
        _wait(wait, n)
    raise previous_exception


def call(
    func,
    args=None,
    kwargs=None,
    exceptions=None,
    check_for_retry=None,
    times=5,
    wait=0,
):
    ''' A wrapper to automatically retry a function call if it raises an
        exception

        :param func func: The function you want to call.
        :param list args: Positional args to be passed to func
        :param dict kwargs: keywords args to be passed to func
        :param list exceptions: an array of Exception types you to retry on
        :param func check_for_retry: A function that excepts Exception and
            Count and returns true if the function should be retried
        :param int times: number of times to retry
        :param int wait: number of seconds to wait between tries
    '''

    args = [] if args is None else args
    kwargs = {} if kwargs is None else kwargs
    exceptions = [Exception] if exceptions is None else exceptions
    return _retry(
        partial(func, *args, **kwargs),
        exceptions,
        check_for_retry,
        times,
        wait,
    )


def decorate(*exceptions, **retry_args):
    """ Decorates a function to automatically retry it when it is called

        :param type exception: A variable number of exception types that should
            be retried.
        :param dict kwargs:  kwargs that should be passed on to _function
    """

    def inner(func):
        return wrap(
            func,
            exceptions=exceptions or None,
            **retry_args
        )

    return inner


def wrap(func, **retry_args):
    """ Wraps a function to automatically retry it when it is called

        Accepts the same arguments as ``retry``.
    """

    @wraps(func)
    def inner(*args, **kwargs):
        return call(
            func,
            args=args,
            kwargs=kwargs,
            **retry_args
        )
    return inner
