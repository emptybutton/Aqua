from typing import Iterable


def last_among[ValueT](values: Iterable[ValueT]) -> ValueT | None:
    last_value = None

    for value in values:
        last_value = value

    return last_value
