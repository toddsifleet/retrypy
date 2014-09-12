A python retry wrapper/decorator
=============

A simple way to auto retry a funciton that has the possibility of raising an error.  You can either call retry directly or decorate a function to get it to retry.  Intelligent matching logic allows you to retry certain exception while raising other exceptions.


Using retry as a function:
-------
    from retry import retry
    def dummy_func():
        print "dummy_func called..."
        raise Exception("House")

    retry.retry(
      dummy_func,
      times=2
    )

    dummy_func called...
    dummy_func called...
    Exception: House

Params:
-------
      func: The function you want to call.
      args: Positional args to be passed to func
      kwargs: keywords args to be passed to func
      exceptions: an array of Exception types you want to retry on.
      check_for_retry: A function that excepts Exception and Count and
          returns true if the function should be retried.
      times: number of times to retry
      wait: number of seconds to wait between tries


Or you can use it as a decorator:
-------
    @retry(Exception, times=2)
    def dummy_func():
        print "dummy_func called..."
        raise Exception("House")
    dummy_func()

    dummy_func called...
    dummy_func called...
    Exception: House


Params:
-------
      positional_args: All position arguments must be Exception types, these
          are the only types of exceptions we will retry.
      check_for_retry: A function that excepts Exception and Count and
          returns true if the function should be retried.
      times: number of times to retry
      wait: number of seconds to wait between tries
License:
-------

See LICENSE
