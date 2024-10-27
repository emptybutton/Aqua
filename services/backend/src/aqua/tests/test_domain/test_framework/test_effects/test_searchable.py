from dataclasses import dataclass

from aqua.domain.framework.effects.searchable import SearchableEffect
from aqua.domain.framework.entity import Entity, FrozenEntities


@dataclass(kw_only=True, eq=False)
class X(Entity[int, int | str | float]):
    x: int = int()


@dataclass(kw_only=True, eq=False)
class Y(Entity[int, int | str | float]):
    y: str = str()


@dataclass(kw_only=True, eq=False)
class Z(Entity[int, int | str | float]):
    z: float = float()


def test_entities_that() -> None:
    x1 = X(id=0, events=list())
    x2 = X(id=1, events=list())
    y1 = Y(id=0, events=list())
    y2 = Y(id=1, events=list())
    z1 = Z(id=0, events=list())
    z2 = Z(id=1, events=list())

    effect = SearchableEffect([x1, x2, y1, y2, z1, z2])

    xs = effect.entities_that(X)

    assert xs == FrozenEntities([x1, x2])


def test_ignore() -> None:
    x1 = X(id=0, events=list())
    x2 = X(id=1, events=list())
    y1 = Y(id=0, events=list())
    y2 = Y(id=1, events=list())
    z1 = Z(id=0, events=list())
    z2 = Z(id=1, events=list())

    effect = SearchableEffect([x1, x2, y1, y2, z1, z2])

    effect.ignore(x1, x2, y1)

    assert not effect.entities_that(X)
    assert effect.entities_that(Y) == FrozenEntities([y2])
    assert effect.entities_that(Z) == FrozenEntities([z1, z2])


def test_cancel() -> None:
    x1 = X(id=0, events=list())
    x2 = X(id=1, events=list())
    y1 = Y(id=0, events=list())
    y2 = Y(id=1, events=list())
    z1 = Z(id=0, events=list())
    z2 = Z(id=1, events=list())

    effect = SearchableEffect([x1, x2, y1, y2, z1, z2])

    effect.cancel()

    assert not effect.entities_that(X)
    assert not effect.entities_that(Y)
    assert not effect.entities_that(Z)
