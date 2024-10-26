from dataclasses import dataclass

from aqua.domain.framework.entity import Entity


@dataclass(kw_only=True, eq=False)
class X(Entity[int, int | str | float]):
    x: int


def test_events_with_type() -> None:
    x = X(id=0, x=4, events=[0, 1, 2.0, "3", 4, 5.0, "6"])

    events = x.events_with_type(str)

    assert events == ("3", "6")


def test_true_eq() -> None:
    a = X(id=0, x=4, events=[])
    b = X(id=0, x=5, events=[])

    assert a == b


def test_false_eq_with_x() -> None:
    a = X(id=0, x=4, events=[])
    b = X(id=1, x=4, events=[])

    assert a != b


def test_false_eq_without_x() -> None:
    a = X(id=0, x=4, events=[])
    b = 5

    assert a != b
