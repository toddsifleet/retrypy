import re
import time
from functools import partial

always_true = lambda *_: True

def _parse_search(input):
    if isinstance(input, str):
        return lambda x: x in input
    elif isinstance(input, re._pattern_type):
        return lambda x: input.search(x)
    elif hasattr(input, '__call__'):
        return input
    raise TypeError("Matches must be strings, regex, or functions")

def _parse_exceptions(input):
    matches = []
    for e in input:
        if isinstance(e, (tuple, list)):
            matches.append((e[0], _parse_search(e[1])))
        else:
            matches.append((e, always_true))

    exceptions = map(lambda x: x[0], matches)
    return tuple(exceptions), matches

def _retryable(e, matches):
    for e_type, test in matches:
        if isinstance(e, e_type):
            return test(e.message)
    return False

def _retry(func, exceptions, times, wait, include_error_and_count):
    exceptions, matches = _parse_exceptions(exceptions)
    previous_exception = None
    for n in xrange(times):
        if n: time.sleep(wait)
        try:
            if include_error_and_count:
                return func(
                    count = n, 
                    previous_exception = previous_exception
                )
            else:
                return func()
        except exceptions as e:
            if not _retryable(e, matches):
                raise e
            previous_exception = e
    raise previous_exception

def retry(func, args = None, kwargs = None, exceptions = None, times = 5, wait = 1, include_error_and_count = False):
    '''
        A wrapper to automagically retry a function call if it fails

        Parameters:
            func: The function you want to call.  
            args: Positional args to be passed to func
            kwargs: keywords args to be passed to func
            exceptions: an array of Exception types you want to retry on. this can be in the form of
                [ExceptionType1, ExceptionType2 ... ]
                [(ExceptionType1, RegEx) ...] => test if the error matches the RegEx
                [(ExceptionType1, String) ...] => test if the error includes String
                [(ExceptionType1, Function) ...] => A custom test function that returns true or false
            times: number of times to retry
            wait: number of seconds to wait between tries
            include_error_and_count: If this is set the func must accept atleast two args in addition to the ones supplied:
                1.) count => The attempt number
                2.) previous_exception => the previous exception raised
    '''
    if args is None: args = []
    if kwargs is None: kwargs = {}
    if exceptions is None: exceptions = [Exception]

    if times < 1:
        raise TypeError("Cannot try less than 1 time")
    elif times == 1:
        return func(*args, **kwargs)

    return _retry(partial(func, *args, **kwargs), exceptions, times, wait, include_error_and_count)

def retry_me(**decorator_kwargs):
    def wrap(func):
        def wrapped(*func_args, **func_kwargs):
            return retry(func, args = func_args, kwargs = func_kwargs, **decorator_kwargs)

        return wrapped
    return wrap
