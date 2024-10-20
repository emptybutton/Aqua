from dataclasses import dataclass
from typing import Iterable, Self

from shared.domain.framework.ports.effect import Effect


@dataclass(kw_only=True, frozen=True, slots=True)
class Event[EntityT]:
    entity: EntityT


@dataclass(kw_only=True, frozen=True, slots=True)
class MutationEvent[EntityT](Event[EntityT]): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class CommentingEvent[EntityT](Event[EntityT]): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Created[EntityT](CommentingEvent[EntityT]): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Translated[EntityT, OriginalT](CommentingEvent[EntityT]):
    from_: OriginalT


@dataclass(kw_only=True, eq=False)
class Entity[IDT, EventT]:
    id: IDT
    events: list[EventT]

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

    def events_with_type[OtherEventT](
        self, event_type: type[OtherEventT]
    ) -> tuple[OtherEventT, ...]:
        return tuple(
            event for event in self.events if isinstance(event, event_type)
        )

    def last_event_with_type[OtherEventT](
        self, event_type: type[OtherEventT]
    ) -> OtherEventT | None:
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
