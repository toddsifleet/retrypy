from retry import retry
import re
import unittest


def dummy_func(*args, **kwargs):
    return


class Test__parse_search(unittest.TestCase):
    def test_regex(self):
        regex = re.compile("house")
        result = retry._parse_search(regex)
        self.assertTrue(result("house"))
        self.assertFalse(result("houddse"))

    def test_string(self):
        result = retry._parse_search("house")
        self.assertTrue(result("house"))
        self.assertFalse(result("houddse"))

    def test_function(self):
        result = retry._parse_search(lambda x: "house" in x)
        self.assertTrue(result("house"))
        self.assertFalse(result("houddse"))

    def test_invalid(self):
        self.assertRaises(TypeError, retry._parse_search, 11)


class Test__parse_exceptions(unittest.TestCase):
    def test_empty_list(self):
        result = retry._parse_exceptions([])
        assert ((), []) == result

    def test_no_match_functions(self):
        input = [Exception, TypeError]
        exceptions, matches = retry._parse_exceptions(input)
        for test_e, (result_e, f) in zip(input, matches):
            self.assertTrue(f(''))
            assert test_e == result_e
        assert exceptions == tuple(input)

    def test_match_functions(self):
        f = lambda x: "house" in x
        input = [
            [Exception, f],
            (TypeError, f)
        ]
        exceptions, matches = retry._parse_exceptions(input)
        for (test_e, _), (result_e, f) in zip(input, matches):
            self.assertFalse(f(''))
            self.assertTrue(f('test_house'))
            assert test_e == result_e
        assert exceptions == tuple(map(lambda x: x[0], input))


class Test__retryable(unittest.TestCase):
    def test_empty_matches(self):
        result = retry._retryable(Exception(''), [])
        self.assertFalse(result)

    def test_passing_case(self):
        result = retry._retryable(Exception(''), [(Exception, lambda x: True)])
        self.assertTrue(result)

    def test_subclass_exception(self):
        result = retry._retryable(TypeError(''), [(Exception, lambda x: True)])
        self.assertTrue(result)

    def test_failing_case(self):
        result = retry._retryable(Exception(''), [(TypeError, lambda x: True)])
        self.assertFalse(result)

    def test_pass_exception_type_fail_match(self):
        result = retry._retryable(
            Exception(''),
            [(Exception, lambda x: False)]
        )
        self.assertFalse(result)


class Test_retry(unittest.TestCase):
    def setUp(self):
        def dummy_retry(*args):
            return args

        def dummy_partial(*args, **kwargs):
            return args, kwargs

        self.old_retry = retry._retry
        retry._retry = dummy_retry
        self.old_partial = retry.partial
        retry.partial = dummy_partial

    def tearDown(self):
        retry._retry = self.old_retry
        retry.partial = self.old_partial

    def test_just_func_supplied(self):
        result = retry.retry(dummy_func)
        ((func,), _), exceptions, times, wait = result
        assert dummy_func == func
        assert exceptions == [Exception]
        assert times == 5
        assert wait == 1

    def test_args_kwargs(self):
        test_args = (1, 2, 3)
        test_kwargs = {'foo': 'bar'}
        result = retry.retry(
            dummy_func,
            args=test_args,
            kwargs=test_kwargs
        )
        results, exceptions, times, wait = result

        assert results[0][0] == dummy_func
        assert results[0][1::] == test_args
        assert results[1] == test_kwargs

    def test_different_times(self):
        self.assertRaises(TypeError, retry.retry, dummy_func, times=-1)
        result = retry.retry(dummy_func, times=1)
        assert result is None
        _, _, times, _ = retry.retry(dummy_func, times=10)
        assert times == 10


class Test__retry(unittest.TestCase):
    def test_no_error(self):
        result = retry._retry(
            lambda count, previous_exception, **_: 100,
            [],
            10,
            1,
        )
        assert result == 100
        result = retry._retry(lambda **_: 100, [], 10, 1)
        assert result == 100

    def test_error_out(self):
        self.call_count = 0

        def dummy_func(**kwargs):
            self.call_count += 1
            raise TypeError("FOOBAR")

        self.assertRaises(TypeError, retry._retry, dummy_func, [], 5, 1)
        assert self.call_count == 1

    def test_catch_errors_and_retry(self):
        self.call_count = 0

        def dummy_func(**kwargs):
            self.call_count += 1
            raise TypeError("FOOBAR")

        self.assertRaises(
            TypeError,
            retry._retry,
            dummy_func,
            [Exception],
            5,
            0,
        )
        assert self.call_count == 5

    def test_catch_error_and_succeed(self):
        self.call_count = 0

        def dummy_func(**kwargs):
            self.call_count += 1
            if self.call_count < 4:
                raise TypeError("FOOBAR")
            return "victory"

        result = retry._retry(dummy_func, [Exception], 5, 0)
        assert self.call_count == 4
        assert result == "victory"


class Test_decorator(unittest.TestCase):
    def test_failure(self):
        self.call_count = 0

        @retry.retry_me(wait=0)
        def dummy_func(**kwargs):
            self.call_count += 1
            raise Exception("house")

        self.assertRaises(Exception, dummy_func)
        assert self.call_count == 5

    def test_success(self):
        @retry.retry_me(wait=0)
        def dummy_func(**kwargs):
            return 10

        assert dummy_func() == 10

    def test_function_args(self):
        @retry.retry_me(wait=0)
        def dummy_func(arg_1, kwarg_1=False, **kwargs):
            return arg_1, kwarg_1

        assert dummy_func(1, kwarg_1=2) == (1, 2,)
