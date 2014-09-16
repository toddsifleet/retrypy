from random import random as _random


def random(min_seconds=0, max_seconds=5):
    def func(count):
        return _random(min_seconds, max_seconds)

    return func


def exponential(start_at):
    def func(count):
        return start_at * (2**count)

    return func


def incremental(start_at, step=1):
    def func(count):
        return start_at + count*step

    return func
