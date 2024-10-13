from dataclasses import dataclass
from typing import Generic, Iterable, Self, TypeVar

from shared.domain.framework.ports.effect import Effect


_EntityT = TypeVar("_EntityT")
_IDT = TypeVar("_IDT")
_EventTypeT = TypeVar("_EventTypeT")


@dataclass(kw_only=True, frozen=True, slots=True)
class EntityEvent(Generic[_EntityT]):
    entity: _EntityT


@dataclass(kw_only=True, frozen=True, slots=True)
class MutationEvent(Generic[_EntityT], EntityEvent[_EntityT]): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class CommentingEvent(Generic[_EntityT], EntityEvent[_EntityT]): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Created(Generic[_EntityT], CommentingEvent[_EntityT]): ...


_AdditionalEventT = TypeVar("_AdditionalEventT")


@dataclass(kw_only=True, eq=False)
class Entity(Generic[_IDT, _AdditionalEventT]):
    id: _IDT
    events: list[Created[Self] | _AdditionalEventT]

    @property
    def mutation_events(self) -> Iterable[MutationEvent[Self]]:
        for event in self.events:
            if isinstance(event, MutationEvent):
                yield event

    @property
    def commenting_events(self) -> Iterable[MutationEvent[Self]]:
        for event in self.events:
            if isinstance(event, MutationEvent):
                yield event

    @property
    def is_new(self) -> bool:
        return any(isinstance(event, Created) for event in self.events)

    @property
    def is_dirty(self) -> bool:
        return bool(tuple(self.mutation_events))

    def events_with_type(
        self, event_type: type[_EventTypeT]
    ) -> tuple[_EventTypeT, ...]:
        return tuple(
            event for event in self.events if isinstance(event, event_type)
        )

    def last_event_with_type(
        self, event_type: type[_EventTypeT]
    ) -> _EventTypeT | None:
        for event in self.events:
            if isinstance(event, event_type):
                return event

        return None

    def reset_events(self, effect: Effect) -> None:
        self.events = list()
        effect.ignore(self)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.id == other.id
