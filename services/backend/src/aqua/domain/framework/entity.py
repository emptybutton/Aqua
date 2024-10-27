from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Iterable, Iterator, Self

from aqua.domain.framework.effects.base import Effect


@dataclass(kw_only=True, frozen=True, slots=True)
class Event[EntityT]:
    entity: EntityT = field(compare=False)


@dataclass(kw_only=True, frozen=True, slots=True)
class Mutated[EntityT](Event[EntityT]): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Created[EntityT](Event[EntityT]): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Translated[EntityT, OriginalT](Event[EntityT]):
    from_: OriginalT


@dataclass(kw_only=True)
class Entity[IDT, EventT]:
    id: IDT
    events: list[EventT]

    def events_with_type[OtherEventT](
        self, event_type: type[OtherEventT]
    ) -> tuple[OtherEventT, ...]:
        return tuple(
            event for event in self.events if isinstance(event, event_type)
        )

    def reset_events(self, *, effect: Effect) -> None:
        self.events = list()
        effect.ignore(self)

    def is_(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.id == other.id

    def without_aggregation(self) -> Self:
        entity = deepcopy(self)

        for attribute_name, attribute in entity.__dict__.items():
            if isinstance(attribute, Entities):
                entity.__dict__[attribute_name] = Entities()

        return entity


type AnyEntity = Entity[Any, Any]


class _BaseEntities[EntityT: AnyEntity]:
    def __init__(self, entities: Iterable[EntityT] = tuple()) -> None:
        self._map: _Map[EntityT] = _map_of(entities)

    def __iter__(self) -> Iterator[EntityT]:
        return iter(self._map.values())

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self._map == other._map

    def __len__(self) -> int:
        return len(self._map)

    def __hash__(self) -> int:
        return hash(self._map)

    def __bool__(self) -> bool:
        return bool(self._map)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({list(self)})"

    def with_event[EventT](
        self, event_type: type[EventT]
    ) -> "FrozenEntities[EntityT]":
        return FrozenEntities(
            entity for entity in self if entity.events_with_type(event_type)
        )

    def without_event[EventT](
        self, event_type: type[EventT]
    ) -> "FrozenEntities[EntityT]":
        return FrozenEntities(
            entity for entity in self if not entity.events_with_type(event_type)
        )

    def without_aggregation(self) -> "FrozenEntities[EntityT]":
        return FrozenEntities(entity.without_aggregation() for entity in self)


class Entities[EntityT: AnyEntity](_BaseEntities[EntityT]):
    def with_event[EventT](
        self, event_type: type[EventT]
    ) -> "FrozenEntities[EntityT]":
        return FrozenEntities(
            entity for entity in self if entity.events_with_type(event_type)
        )

    def add(self, entity: EntityT) -> None:
        self._map[entity.id] = entity

    def remove(self, entity: EntityT) -> None:
        if entity.id in self._map:
            del self._map[entity.id]


class FrozenEntities[EntityT: AnyEntity](_BaseEntities[EntityT]): ...


def is_in[EntityT: AnyEntity](
    entities: Iterable[EntityT], entity: EntityT
) -> bool:
    return any(entity.is_(stored_entity) for stored_entity in entities)


type SearchableEntities[EntityT: AnyEntity] = (
    Entities[EntityT] | FrozenEntities[EntityT]
)


type _Map[EntityT: AnyEntity] = dict[Any, EntityT]


def _map_of[EntityT: AnyEntity](entities: Iterable[EntityT]) -> _Map[EntityT]:
    return {entity.id: entity for entity in entities}
