from pytest import raises

from retry import retry


def get_dummy_func(raise_count=4):
    calls = []

    def func(*args, **kwargs):
        calls.append(True)
        if len(calls) < raise_count:
            raise Exception('Test Error {count}'.format(count=len(calls)))
        return len(calls), args, kwargs
    return func


def test_func_with_no_args():
    assert retry.retry(get_dummy_func(0)) == (1, (), {})


def test_retry_func_with_no_args():
    result = retry.retry(get_dummy_func(), wait=0)
    assert result == (4, (), {})


def test_func_that_raises_too_many_time_raises():
    with raises(Exception) as e:
        retry.retry(get_dummy_func(50), wait=0)
    assert e.value.message == 'Test Error 5'


def test_func_with_positional_arg():
    assert retry.retry(lambda x: x, args=['bar']) == 'bar'


def test_retry_func_with_postional_arg():
    result = retry.retry(get_dummy_func(), args=['foo'], wait=0)
    assert result == (4, ('foo',), {})


def test_func_with_kwargs():
    result = retry.retry(get_dummy_func(0), kwargs={'foo': 'bar'})
    assert result == (1, (), {'foo': 'bar'})


def test_retry_func_with_kwarg():
    result = retry.retry(get_dummy_func(), kwargs={'foo': 'bar'}, wait=0)
    assert result == (4, (), {'foo': 'bar'})


def test_decorated_func_with_no_args():
    func = get_dummy_func(0)

    @retry.retry(wait=0)
    def foo():
        return func()

    assert foo() == (1, (), {})


def test_retry_decorated_func_with_no_args():
    func = get_dummy_func()

    @retry.retry(wait=0)
    def foo():
        return func()

    assert foo() == (4, (), {})


def test_decorated_func_with_positional_arg():
    func = get_dummy_func(0)

    @retry.retry(wait=0)
    def foo(arg):
        return func(arg)

    assert foo('arg') == (1, ('arg',), {})


def test_retry_decorated_func_with_positional_arg():
    func = get_dummy_func()

    @retry.retry(wait=0)
    def foo(arg):
        return func(arg)

    assert foo('arg') == (4, ('arg',), {})


def test_decorated_func_with_kwargs():
    func = get_dummy_func(0)

    @retry.retry(wait=0)
    def foo(**kwargs):
        return func(**kwargs)

    assert foo(foo='bar') == (1, (), {'foo': 'bar'})


def test_retry_decorated_func_with_kwargs():
    func = get_dummy_func()

    @retry.retry(wait=0)
    def foo(**kwargs):
        return func(**kwargs)

    assert foo(foo='bar') == (4, (), {'foo': 'bar'})


def test_decorated_func_that_raises_too_many_time_raises():
    func = get_dummy_func(50)

    @retry.retry(wait=0)
    def foo():
        return func()

    with raises(Exception) as e:
        retry.retry(get_dummy_func(50), wait=0)
    assert e.value.message == 'Test Error 5'
