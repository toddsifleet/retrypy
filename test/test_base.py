from pytest import raises
from doubles import expect

from retry import retry


def get_dummy_func(raise_count=4):
    calls = []

    def func(*args, **kwargs):
        calls.append(True)
        if len(calls) <= raise_count:
            raise Exception('Test Error {count}'.format(count=len(calls)))
        return len(calls), args, kwargs
    return func


def test_func_with_no_args():
    assert retry.retry(get_dummy_func(0)) == (1, (), {})


def test_retry_func_with_no_args():
    result = retry.retry(get_dummy_func())
    assert result == (5, (), {})


def test_func_that_raises_too_many_time_raises():
    with raises(Exception) as e:
        retry.retry(get_dummy_func(50))
    assert e.value.message == 'Test Error 5'


def test_func_that_fails_check_for_retry_raises():
    with raises(Exception) as e:
        retry.retry(
            get_dummy_func(5),
            check_for_retry=lambda e, c: not e.message.endswith('3'),
        )
    assert e.value.message == 'Test Error 3'


def test_func_that_raises_wrong_exception_type_should_raise():
    with raises(Exception) as e:
        retry.retry(
            get_dummy_func(5),
            exceptions=[TypeError],
        )
    assert e.value.message == 'Test Error 1'


def test_func_with_positional_arg():
    assert retry.retry(lambda x: x, args=['bar']) == 'bar'


def test_retry_func_with_postional_arg():
    result = retry.retry(get_dummy_func(), args=['foo'])
    assert result == (5, ('foo',), {})


def test_func_with_kwargs():
    result = retry.retry(get_dummy_func(0), kwargs={'foo': 'bar'})
    assert result == (1, (), {'foo': 'bar'})


def test_retry_func_with_kwarg():
    result = retry.retry(get_dummy_func(), kwargs={'foo': 'bar'})
    assert result == (5, (), {'foo': 'bar'})


def test_decorated_func_with_no_args():
    func = get_dummy_func(0)

    @retry.retry()
    def foo():
        return func()

    assert foo() == (1, (), {})


def test_retry_decorated_func_with_no_args():
    func = get_dummy_func()

    @retry.retry()
    def foo():
        return func()

    assert foo() == (5, (), {})


def test_decorated_func_with_positional_arg():
    func = get_dummy_func(0)

    @retry.retry()
    def foo(arg):
        return func(arg)

    assert foo('arg') == (1, ('arg',), {})


def test_retry_decorated_func_with_positional_arg():
    func = get_dummy_func()

    @retry.retry()
    def foo(arg):
        return func(arg)

    assert foo('arg') == (5, ('arg',), {})


def test_decorated_func_with_kwargs():
    func = get_dummy_func(0)

    @retry.retry()
    def foo(**kwargs):
        return func(**kwargs)

    assert foo(foo='bar') == (1, (), {'foo': 'bar'})


def test_retry_decorated_func_with_kwargs():
    func = get_dummy_func()

    @retry.retry()
    def foo(**kwargs):
        return func(**kwargs)

    assert foo(foo='bar') == (5, (), {'foo': 'bar'})


def test_decorated_func_that_raises_too_many_time_raises():
    func = get_dummy_func(50)

    @retry.retry()
    def foo():
        return func()

    with raises(Exception) as e:
        foo()
    assert e.value.message == 'Test Error 5'


def test_decorated_func_that_raises_wrong_exception_type_should_raise():
    func = get_dummy_func(50)

    @retry.retry(TypeError)
    def foo():
        return func()

    with raises(Exception) as e:
        foo()
    assert e.value.message == 'Test Error 1'


def test_retry_with_custom_wait_function():
    expect(retry)._sleep.with_args(0)
    expect(retry)._sleep.with_args(1)
    expect(retry)._sleep.with_args(2)
    expect(retry)._sleep.with_args(3)

    retry.retry(get_dummy_func(), wait=lambda n: n)


def test_retry_with_fixed_wait():
    expect(retry)._sleep.with_args(1).exactly(4).times

    retry.retry(get_dummy_func(), wait=1)


def test_retry_with_doubling_delay():
    expect(retry)._sleep.with_args(1)
    expect(retry)._sleep.with_args(2)
    expect(retry)._sleep.with_args(4)
    expect(retry)._sleep.with_args(8)

    retry.retry(get_dummy_func(), wait=retry.doubling_delay(1))


def test_retry_with_linear_delay():
    expect(retry)._sleep.with_args(2)
    expect(retry)._sleep.with_args(3)
    expect(retry)._sleep.with_args(4)
    expect(retry)._sleep.with_args(5)

    retry.retry(get_dummy_func(), wait=retry.linear_delay(2, 1))
