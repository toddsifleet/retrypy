import re


def message_equals(check_string):
    return lambda e, n: check_string == e.message


def message_contains(check_string):
    return lambda e, n: check_string in e.message


def message_matches(regex):
    if not isinstance(input, re._pattern_type):
        regex = re.compile(regex)

    return lambda e, n: regex.search(e.message)
