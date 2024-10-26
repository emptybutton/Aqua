from dataclasses import dataclass

from aqua.domain.framework.entity import Entities, Entity


@dataclass(kw_only=True, eq=False)
class X(Entity[int, int | str | float]): ...


def test_add() -> None:
    a = X(id=0, events=list())
    b = X(id=1, events=list())
    c = X(id=2, events=list())

    entities = Entities[X]([a])

    entities.add(b)
    entities.add(c)

    assert frozenset(entities) == frozenset({a, b, c})


def test_add_with_conflict() -> None:
    a = X(id=0, events=list())
    b = X(id=1, events=[1, 2])
    c = X(id=1, events=[2, 3])

    entities = Entities[X]([a])

    entities.add(b)
    entities.add(c)

    stored_entities = tuple(entities)

    for stored_entity in stored_entities:
        if stored_entity == c:
            assert stored_entity.events == [2, 3]


def test_remove() -> None:
    a = X(id=0, events=list())
    b = X(id=1, events=list())
    c = X(id=2, events=list())

    entities = Entities[X]([a, b, c])

    entities.remove(b)
    entities.remove(c)

    assert frozenset(entities) == frozenset({a})


def test_remove_from_empty_entities() -> None:
    x = X(id=0, events=list())

    entities = Entities[X]()
    entities.remove(x)

    assert frozenset(entities) == frozenset()


def test_with_event() -> None:
    a = X(id=0, events=[1])
    b = X(id=1, events=[1.])
    c = X(id=2, events=["1"])
    d = X(id=3, events=[4])

    entities = Entities[X]((a, b, c, d))

    entities_with_event = entities.with_event(int)

    assert frozenset(entities_with_event) == frozenset({a, d})
