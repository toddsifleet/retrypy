A python retry wrapper/decorator
=============

A simple way to auto retry a funciton that has the possibility of raising an error.  You can either call retry directly or decorate a function to get it to retry.  Intelligent matching logic allows you to retry certain exception while raising other exceptions.


How to use it
-------
    from retry import retry
    def dummy_func():
        print "dummy_func called..."
        raise Exception("House")
    retry.retry(dummy_func)
    
    dummy_func called...
    dummy_func called...
    dummy_func called...
    dummy_func called...
    dummy_func called...
    Traceback (most recent call last):
      File "test.py", line 5, in <module>
        retry.retry(dummy_func)
      File "/Users/toddsifleet/Dropbox/github/retry/retry/retry.py", line 80, in retry
        return _retry(partial(func, *args, **kwargs), exceptions, times, wait, include_error_and_count)
      File "/Users/toddsifleet/Dropbox/github/retry/retry/retry.py", line 50, in _retry
        raise previous_exception
    Exception: House

    #or decorate a function.  this behaves the same as above
    @retry.retry_me()
    def dummy_func():
        print "dummy_func called..."
        raise Exception("House")
    dummy_func()

Params:
-------
    func[required]: The function you want to call.  
    args: Positional args to be passed to func
    kwargs: keywords args to be passed to func
    exceptions [default: [Exception]]: an array of Exception types you want to retry on. this can be in the form of
        [ExceptionType1, ExceptionType2 ... ]
        [(ExceptionType1, RegEx) ...] => test if the error matches the RegEx
        [(ExceptionType1, String) ...] => test if the error includes String
        [(ExceptionType1, Function) ...] => A custom test function that returns true or false
    times [default:5]: number of times to retry
    wait [default: 1]: number of seconds to wait between tries
    include_error_and_count [default: False]: If this is set the func must accept atleast two args in addition to the ones supplied:
        1.) count => The attempt number
        2.) previous_exception => the previous exception raised


License:
-------

See LICENSE
