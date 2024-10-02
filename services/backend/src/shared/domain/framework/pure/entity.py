from dataclasses import dataclass
from typing import Generic, Iterable, TypeVar

from shared.domain.framework.pure.ports.effect import Effect


_IDT = TypeVar("_IDT")


@dataclass(kw_only=True, frozen=True)
class EntityEvent(Generic[_IDT]):
    entity_id: _IDT


@dataclass(kw_only=True, frozen=True)
class MutationEvent(Generic[_IDT], EntityEvent[_IDT]): ...


@dataclass(kw_only=True, frozen=True)
class CommentingEvent(Generic[_IDT], EntityEvent[_IDT]): ...


@dataclass(kw_only=True, frozen=True)
class Created(Generic[_IDT], CommentingEvent[_IDT]):
    entity_id: _IDT


@dataclass(kw_only=True, frozen=True)
class Deleted(Generic[_IDT], CommentingEvent[_IDT]):
    entity_id: _IDT


_AdditionalEventT = TypeVar("_AdditionalEventT", bound=EntityEvent)


@dataclass(kw_only=True, eq=False)
class Entity(Generic[_IDT, _AdditionalEventT]):
    id: _IDT
    events: list[EntityEvent | _AdditionalEventT]

    @property
    def mutation_events(self) -> Iterable[MutationEvent]:
        for event in self.events:
            if isinstance(event, MutationEvent):
                yield event

    @property
    def commenting_events(self) -> Iterable[MutationEvent]:
        for event in self.events:
            if isinstance(event, MutationEvent):
                yield event

    @property
    def is_deleted(self) -> bool:
        return any(isinstance(event, Deleted) for event in self.events)

    @property
    def is_new(self) -> bool:
        return (
            not self.is_deleted
            and any(isinstance(event, Created) for event in self.events)
        )

    @property
    def is_dirty(self) -> bool:
        return tuple(self.mutation_events)

    def reset_events(self, effect: Effect) -> None:
        self.events = list()
        effect.ignore(self)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.id == other.id
