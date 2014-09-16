A python retry wrapper/decorator
=============

[![Travis Test Status](https://travis-ci.org/toddsifleet/retrypy.svg?branch=master)](https://travis-ci.org/toddsifleet/retrypy)

A simple way to auto retry a funciton that has the possibility of raising an error.  You can either call retry directly or decorate a function to get it to retry.  Intelligent matching logic allows you to retry certain exception while raising other exceptions.


Using retry as a function:
-------
    from retrypy import retry, check
    def dummy_func():
        print "dummy_func called..."
        raise Exception("House")

    retry.call(
        dummy_func,
        times=2
    )

    dummy_func called...
    dummy_func called...
    Exception: House

    # usign a check method
    retry.call(
        dummy_func,
        check = check.message_equals("foobar")
    )
    dummy_func called...
    Exception: House


Params:
-------
      func: The function you want to call.
      args: Positional args to be passed to func
      kwargs: keywords args to be passed to func
      exceptions: an array of Exception types you want to retry on.
      check: A function that excepts Exception and Count and
          returns true if the function should be retried.
      times: number of times to try the function (default=5)
      wait: number of seconds to wait between tries (default=0) or a function
          that accepts try_count and returns a number of seconds to wait


Or you can use it as a decorator:
-------
    @retry.decorate(Exception, times=2)
    def dummy_func():
        print "dummy_func called..."
        raise Exception("House")
    dummy_func()

    dummy_func called...
    dummy_func called...
    Exception: House

    # custom wait function
    @retry.decorate(Exception, times=2, wait=lambda n: 2*n)
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
      check: see retrypy.call
      times: see retrypy.call
      wait: see retrypy.call

Or you can use it to wrap a function and return a new callable
-------
    def dummy_func():
        print "dummy_func called..."
        raise Exception("House")

    func = retry.wrap(
        dummy_func,
        times=2
    )
    func()

    dummy_func called...
    dummy_func called...
    Exception: House

Params:
    See Docs for retry.call


Installation
-------

    >> pip install retrypy
License:
-------

See LICENSE
