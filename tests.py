from retry import retry
import re
import unittest
import functools

def dummy_func():
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
        self.assertEqual(((), []), result)

    def test_no_match_functions(self):
        input = [Exception, TypeError]
        exceptions, matches = retry._parse_exceptions(input)
        for test_e, (result_e, f) in zip(input, matches):
            self.assertTrue(f(''))
            self.assertEqual(test_e, result_e)
        self.assertEqual(exceptions, tuple(input))

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
            self.assertEqual(test_e, result_e)
        self.assertEqual(exceptions, tuple(map(lambda x: x[0], input)))

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
        result = retry._retryable(Exception(''), [(Exception, lambda x: False)])
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
        ((func,), _), exceptions, times, wait, include_error_and_count = retry.retry(dummy_func)
        self.assertEqual(dummy_func, func)
        self.assertEqual(exceptions, [Exception])
        self.assertEqual(times, 5)
        self.assertEqual(wait, 1)

    def test_args_kwargs(self):
        test_args = (1, 2, 3)
        test_kwargs = {'foo': 'bar'}
        results, exceptions, times, wait, include_error_and_count = retry.retry(dummy_func, 
            args = test_args,
            kwargs = test_kwargs
        )

        self.assertEqual(results[0][0], dummy_func)
        self.assertEqual(results[0][1::], test_args)
        self.assertEqual(results[1], test_kwargs)

    def test_different_times(self):
        self.assertRaises(TypeError, retry.retry, dummy_func, times = -1)
        result = retry.retry(dummy_func, times = 1)
        self.assertEqual(result, None)
        _, _, times, _, _ = retry.retry(dummy_func, times = 10)
        self.assertEqual(times, 10)

class Test__retry(unittest.TestCase):
    def test_no_error(self):
        result = retry._retry(lambda count, previous_exception: 100, [], 10, 1, True)
        self.assertEqual(result, 100)
        result = retry._retry(lambda: 100, [], 10, 1, False)
        self.assertEqual(result, 100)

    def test_error_out(self):
        self.call_count = 0
        def dummy_func():
            self.call_count += 1
            raise TypeError("FOOBAR")
        self.assertRaises(TypeError, retry._retry, dummy_func, [], 5, 1, False)
        self.assertEqual(self.call_count, 1)

    def test_catch_errors_and_retry(self):
        self.call_count = 0
        def dummy_func():
            self.call_count += 1
            raise TypeError("FOOBAR")
        self.assertRaises(TypeError, retry._retry, dummy_func, [Exception], 5, 0, False)
        self.assertEqual(self.call_count, 5)

    def test_catch_error_and_succeed(self):
        self.call_count = 0
        def dummy_func():
            self.call_count += 1
            if self.call_count < 4:
                raise TypeError("FOOBAR")
            return "victory"

        result = retry._retry(dummy_func, [Exception], 5, 0, False)
        self.assertEqual(self.call_count, 4)
        self.assertEqual(result, "victory")


if __name__ == '__main__':
    unittest.main()

