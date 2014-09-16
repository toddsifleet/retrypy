import mock

import retry.delay


@mock.patch('retry.delay._random')
def test_random_calls_stdlib_random(mock_random):
    mock_random.return_value = 'bob'
    func = retry.delay.random(0, 1)

    assert func(1) == 'bob'
    mock_random.assert_called_with(0, 1)


def test_exponential_grows_exponentialy():
    func = retry.delay.exponential(2)

    assert func(0) == 2
    assert func(1) == 4
    assert func(2) == 8
    assert func(3) == 16


def test_incremental_grows_by_step():
    func = retry.delay.incremental(2, 3)

    assert func(0) == 2
    assert func(1) == 5
    assert func(2) == 8
