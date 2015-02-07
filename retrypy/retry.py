from time import sleep
from functools import partial, wraps
from numbers import Number


try:
    xrange
except NameError:
    xrange = range


def _wait(wait, count):
    if not isinstance(wait, Number):
        wait = wait(count)

    sleep(wait)


def _retry(func, exceptions, check, times, wait):
    previous_exception = None
    for n in xrange(1, times + 1):
        try:
            return func()
        except tuple(exceptions) as e:
            if check and not check(e, n):
                raise e
            previous_exception = e
        if n < times:
            _wait(wait, n)
    raise previous_exception


def call(
    func,
    exceptions=None,
    args=None,
    kwargs=None,
    check=None,
    times=5,
    wait=0,
):
    ''' A wrapper to automatically retry a function call if it raises an
        exception

        :param func func: The function you want to call.
        :param list args: Positional args to be passed to func
        :param dict kwargs: keywords args to be passed to func
        :param list exceptions: an array of Exception types you to retry on
        :param func check: A function that excepts Exception and
            Count and returns true if the function should be retried
        :param int times: number of times to try the function
        :param int wait: number of seconds to wait between tries
        :returns: The return value form the supplied function or raises.
    '''

    args = [] if args is None else args
    kwargs = {} if kwargs is None else kwargs
    exceptions = [Exception] if not exceptions else exceptions
    return _retry(
        partial(func, *args, **kwargs),
        exceptions,
        check,
        times,
        wait,
    )


def decorate(*exceptions, **retry_args):
    """ Decorates a function to automatically retry it when it is called

        :param type exceptions: A variable number of exception types that
            should be retried.
        :param dict kwargs:  kwargs that should be passed on to ``call``
            see retrypy.call for details.
        :returns: A wrapped function
        :rtype: func
    """

    def inner(func):
        return wrap(
            func,
            exceptions=exceptions,
            **retry_args
        )

    return inner


def wrap(func, **retry_args):
    """ Wraps a function to automatically retry it when it is called

        Accepts the same arguments as ``call``.
        :returns: The return value form the supplied function or raises.
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
