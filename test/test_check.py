import re

from retrypy import check


def test_message_equals_returns_true():
    func = check.message_equals('foo')
    assert func(Exception('foo'), 1)


def test_message_equals_returns_false():
    func = check.message_equals('foo')
    assert not func(Exception('bar'), 1)


def test_message_contains_returns_true():
    func = check.message_contains('foo')
    assert func(Exception('bob foo'), 1)


def test_message_contains_returns_false():
    func = check.message_contains('foo')
    assert not func(Exception('bob barker'), 1)


def test_message_matches_returns_true_with_regex():
    func = check.message_matches(re.compile('bar'))
    assert func(Exception('bob barker'), 1)


def test_message_matches_returns_false_with_regex():
    func = check.message_matches(re.compile('foo'))
    assert not func(Exception('bob barker'), 1)


def test_message_matches_returns_true_with_string():
    func = check.message_matches('bar')
    assert func(Exception('bob barker'), 1)


def test_message_matches_returns_false_with_string():
    func = check.message_matches('foo')
    assert not func(Exception('bob barker'), 1)
