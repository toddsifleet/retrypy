import re


def message_equals(check_string):
    """Error message equals

    :param str check_string: Value to check against
    :rtype func:
    """
    return lambda e, n: check_string == str(e)


def message_contains(check_string):
    """Error message contains

    :param str check_string: Value to check against
    :rtype func:
    """
    return lambda e, n: check_string in str(e)


def message_matches(regex):
    """Error message matches regex

    :param regex regex: Regex to test (str or compiled regex)
    :rtype func:
    """
    if not isinstance(input, re._pattern_type):
        regex = re.compile(regex)

    return lambda e, n: regex.search(str(e))
