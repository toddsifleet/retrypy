import time
from functools import partial, wraps


def _retry(func, exceptions, check_for_retry, times, wait):
    previous_exception = None
    for n in xrange(times):
        try:
            return func()
        except tuple(exceptions) as e:
            if check_for_retry and not check_for_retry(e, n):
                raise e
            previous_exception = e
        time.sleep(wait)
    raise previous_exception


def retry(*args, **kwargs):
    """Wrapper around _function and _decorator

    If there are no arguments or the first argument is a type this behaves
    as a decorator, otherwise this will retry the function supplied.
    """
    if not args or isinstance(args[0], type):
        return _decorator(*args, **kwargs)
    return _function(*args, **kwargs)


def _function(
    func,
    args=None,
    kwargs=None,
    exceptions=None,
    check_for_retry=None,
    times=5,
    wait=0,
):
    ''' A wrapper to automagically retry a function call if it fails

        :param func func: The function you want to call.
        :param list args: Positional args to be passed to func
        :param dict kwargs: keywords args to be passed to func
        :param list exceptions: an array of Exception types you to retry on
        :param func check_for_retry: A function that excepts Exception and
            Count and returns true if the function should be retried
        :param int times: number of times to retry
        :param int wait: number of seconds to wait between tries
    '''
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}
    if exceptions is None:
        exceptions = [Exception]
    if times < 1:
        raise TypeError("Cannot try less than 1 time")

    return _retry(
        partial(func, *args, **kwargs),
        exceptions,
        check_for_retry,
        times,
        wait,
    )


def _decorator(*exceptions, **decorator_kwargs):
    """Decorates a function to automatically retry it when it is called"""

    def wrap(func):
        @wraps(func)
        def wrapped(*func_args, **func_kwargs):
            return retry(
                func,
                args=func_args,
                kwargs=func_kwargs,
                exceptions=exceptions or None,
                **decorator_kwargs
            )

        return wrapped
    return wrap
