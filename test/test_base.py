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


class Test_retry(unittest.TestCase):

    def test_just_func_supplied(self):
        assert retry.retry(lambda: 'bar') == 'bar'

    def test_args_kwargs(self):
        test_args = (1, 2, 3)
        test_kwargs = {'foo': 'bar'}
        result = retry.retry(
            lambda *args, **kwargs: (args, kwargs),
            args=test_args,
            kwargs=test_kwargs
        )
        assert result == (test_args, test_kwargs)

    def test_no_error(self):
        result = retry.retry(
            lambda: 100,
            [],
            {},
            [Exception],
            10,
            1,
        )
        assert result == 100

    def test_error_out(self):
        self.call_count = 0

        def dummy_func():
            self.call_count += 1
            raise TypeError("FOOBAR")

        self.assertRaises(
            TypeError,
            retry.retry,
            dummy_func,
            [],
            {},
            [ValueError],
            5,
            1,
        )
        assert self.call_count == 1

    def test_catch_errors_and_retry(self):
        self.call_count = 0

        def dummy_func(**kwargs):
            self.call_count += 1
            raise TypeError("FOOBAR")

        self.assertRaises(
            TypeError,
            retry.retry,
            dummy_func,
            [],
            {},
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

        result = retry.retry(
            dummy_func,
            [],
            {},
            [Exception],
            5,
            0
        )
        assert self.call_count == 4
        assert result == "victory"


class Test_decorator(unittest.TestCase):
    def test_failure(self):
        self.call_count = 0

        @retry.retry(wait=0)
        def dummy_func():
            self.call_count += 1
            raise Exception("house")

        self.assertRaises(Exception, dummy_func)
        assert self.call_count == 5

    def test_success(self):
        @retry.retry(wait=0)
        def dummy_func(**kwargs):
            return 10

        assert dummy_func() == 10

    def test_function_args(self):
        @retry.retry(wait=0)
        def dummy_func(arg_1, kwarg_1=False, **kwargs):
            return arg_1, kwarg_1

        assert dummy_func(1, kwarg_1=2) == (1, 2,)
