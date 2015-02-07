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

**Random**::

    import time
    from retrypy import retry, delay

    def dummy_func():
        print time.time()
        raise Exception("House")

    retry.call(dummy_func, wait=delay.random(
        min_seconds=1,
        max_seconds=5,
    ))

Output (wait times: .66s, .84s, 3.42s, .33s)::

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

**Exponential**::

    import time
    from retrypy import retry, delay

    def dummy_func():
        print time.time()
        raise Exception("House")

    retry.call(dummy_func, wait=delay.exponential(
        start_at=1,
    ))

Output (wait times: 1s, 2s, 4s, 8s)::

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

**Incremental**::

    import time
    from retrypy import retry, delay

    def dummy_func():
        print time.time()
        raise Exception("House")

    retry.call(dummy_func, wait=delay.incremental(
      start_at=1,
      step=1,
    ))

Output (wait times: 1s, 2s, 3s, 4s)::

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


Custom Delay Functions:
-----------------------
You can write your own delay functions, their only requirements are that they take an ``Integer`` and return a ``Number`` of seconds to wait.

::

    def custom_delay(call_count):
        if call_count == 1:
            # don't wait at all the first time
            return 0

        # wait 4, 8, 16, 32
        return 2 ** call_count

        
Builtin Exception Checkers:
---------------------------

Exception Checkers can be used to check if you want to retry a specific exception.  If the check function returns true then the exception is retryable otherwise we will not catch the exception and retry.  The available **checkers** are: ``message_equals``, ``message_contains``, and ``message_matches``.

**message_equals**, will match any ``Exception`` with a message that is identical to the string provided.

**message_contains**, will match any ``Exception`` with a message that contains the string provided.

**message_matches**, will match any ``Exception`` with a message that matches the regex provided.  The regex may be passed as a string or a compiled regex pattern.


Custom Exception Checkers:
--------------------------

You can write your own exception checkers, their only requirements are that they: take an ``Exception`` and an ``Integer`` as parameters.  They should return True if the exception is retryable otherwise False.

::

    def custom_matcher(e, call_count):
        # never fail their first time no matter what
        if call_count == 1:
            return True

        # only retry errors with Bob Barker in the message.
        return "Bob Barker" in str(e):


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
