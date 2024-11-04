from typing import Iterable


def one_from[V](values: Iterable[V]) -> V | None:
    try:
        return next(iter(values))
    except StopIteration:
        return None
