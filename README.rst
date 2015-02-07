A python retry wrapper/decorator
================================

|PyPi Version|
|Travis Test Status|

A simple way to auto retry a funciton that has the possibility of
raising an error. You can either call retry directly or decorate a
function to get it to retry. Intelligent matching logic allows you to
retry certain exception while raising other exceptions.

Call a function directly:
-------------------------

::

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

Decorating a function:
----------------------

::

    # Only retry IOErrors
    @retry.decorate(IOError, times=2)
    def dummy_func():
        print "dummy_func called..."
        raise IOError("House")
    dummy_func()

    dummy_func called...
    dummy_func called...
    IOError: House

    # Retry any Exception, use a custom wait function
    @retry.decorate(times=2, wait=lambda n: 2*n)
    def dummy_func():
        print "dummy_func called..."
        raise Exception("House")
    dummy_func()

    dummy_func called...
    dummy_func called...
    Exception: House

Wrap a function and return a new callable:
------------------------------------------

::

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

Delay Helpers:
--------------

Functions to implement some common backoff strategies: random, exponential, and incremental.

__Random__::

    import time
    from retrypy import retry, delay

    def dummy_func():
        print time.time()
        raise Exception("House")

    retry.call(dummy_func, wait=delay.random(
        min_seconds=1,
        max_seconds=5,
    ))

Output, wait between 1 and 5 seconds (chosen randomly)::

    1423297137.49
    1423297138.15
    1423297138.99
    1423297142.41
    1423297142.74
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "retrypy/retry.py", line 63, in call
        wait,
      File "retrypy/retry.py", line 29, in _retry
        raise previous_exception
    Exception: House

__Exponential__::

    import time
    from retrypy import retry, delay

    def dummy_func():
        print time.time()
        raise Exception("House")

    retry.call(dummy_func, wait=delay.exponential(
        start_at=1,
    ))

Output, wait: 1, 2, 4, 8 seconds::

    1423297238.49
    1423297239.49
    1423297241.49
    1423297245.5
    1423297253.5
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "retrypy/retry.py", line 63, in call
        wait,
      File "retrypy/retry.py", line 29, in _retry
        raise previous_exception
    Exception: House

__Incremental__::

    import time
    from retrypy import retry, delay

    def dummy_func():
        print time.time()
        raise Exception("House")

    retry.call(dummy_func, wait=delay.incremental(
      start_at=1,
      step=1,
    ))

Output, wait: 1, 2, 3, 4 seconds::

    1423297301.64
    1423297302.64
    1423297304.64
    1423297307.65
    1423297311.65
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "retrypy/retry.py", line 63, in call
        wait,
      File "retrypy/retry.py", line 29, in _retry
        raise previous_exception
    Exception: House

Installation:
-------------

::

    >> pip install retrypy

Development:
------------

::

    >> git clone https://github.com/toddsifleet/retrypy
    >> cd retrypy
    >> make bootstrap
    >> make

License:
--------

See LICENSE

.. |Travis Test Status| image:: https://travis-ci.org/toddsifleet/retrypy.svg?branch=master
   :target: https://travis-ci.org/toddsifleet/retrypy

.. |PyPi Version| image:: https://badge.fury.io/py/retrypy.svg
   :target: http://badge.fury.io/py/retrypy
