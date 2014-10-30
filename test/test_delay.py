import mock

import retrypy.delay


@mock.patch('retrypy.delay._random')
def test_random_calls_stdlib_random(mock_random):
    mock_random.return_value = 'bob'
    func = retrypy.delay.random(0, 1)

    assert func(1) == 'bob'
    mock_random.assert_called_with(0, 1)


def test_exponential_grows_exponentialy():
    func = retrypy.delay.exponential(2)

    assert func(1) == 2
    assert func(2) == 4
    assert func(3) == 8
    assert func(4) == 16


def test_incremental_grows_by_step():
    func = retrypy.delay.incremental(2, 3)

    assert func(1) == 2
    assert func(2) == 5
    assert func(3) == 8
