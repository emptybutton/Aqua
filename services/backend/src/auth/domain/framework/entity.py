from dataclasses import dataclass
from typing import Any, Iterable, Iterator

from auth.domain.framework.effects.base import Effect


@dataclass(kw_only=True, frozen=True, slots=True)
class Event[EntityT]:
    entity: EntityT


@dataclass(kw_only=True, frozen=True, slots=True)
class Mutated[EntityT](Event[EntityT]): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Created[EntityT](Event[EntityT]): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Translated[EntityT, OriginalT](Event[EntityT]):
    from_: OriginalT


@dataclass(kw_only=True, eq=False)
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

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.id == other.id


type AnyEntity = Entity[Any, Any]


class Entities[EntityT: AnyEntity]:
    def __init__(self, entities: Iterable[EntityT] = tuple()) -> None:
        self.__entities: set[EntityT] = set(entities)

    def __iter__(self) -> Iterator[EntityT]:
        return iter(self.__entities)

    def with_event[EventT](
        self, event_type: type[EventT]
    ) -> "Entities[EntityT]":
        return Entities(
            entity
            for entity in self.__entities
            if len(entity.events_with_type(event_type)) > 0
        )

    def add(self, entity: EntityT) -> None:
        self.remove(entity)
        self.__entities.add(entity)

    def remove(self, entity: EntityT) -> None:
        if entity in self.__entities:
            self.__entities.remove(entity)
