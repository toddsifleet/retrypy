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

Wrap a function and retrun a new callable:
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

Params: See Docs for retry.call

Installation
------------

::

    >> pip install retrypy

License:
--------

See LICENSE

.. |Travis Test Status| image:: https://travis-ci.org/toddsifleet/retrypy.svg?branch=master
   :target: https://travis-ci.org/toddsifleet/retrypy

.. |PyPi Version| image:: https://travis-ci.org/toddsifleet/retrypy.svg?branch=master
   :target: http://badge.fury.io/py/retrypy
