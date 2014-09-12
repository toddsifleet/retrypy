import time
from functools import partial, wraps


def _retry(func, exceptions, should_retry, times, wait):
    previous_exception = None
    for n in xrange(times):
        try:
            return func()
        except tuple(exceptions) as e:
            if should_retry and not should_retry(e, n):
                raise e
            previous_exception = e
        time.sleep(wait)
    raise previous_exception


def retry(*args, **kwargs):
    if not args or isinstance(args[0], type):
        return _decorator(*args, **kwargs)
    return _function(*args, **kwargs)


def _function(
    func,
    args=None,
    kwargs=None,
    exceptions=None,
    should_retry=None,
    times=5,
    wait=0,
):
    '''
        A wrapper to automagically retry a function call if it fails

        Parameters:
            func: The function you want to call.
            args: Positional args to be passed to func
            kwargs: keywords args to be passed to func
            exceptions: an array of Exception types you want to retry on.
            should_retry: A function that excepts Exception and Count and
            returns true if the function should be retried.
            times: number of times to retry
            wait: number of seconds to wait between tries
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
        should_retry,
        times,
        wait,
    )


def _decorator(*exceptions, **decorator_kwargs):

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
