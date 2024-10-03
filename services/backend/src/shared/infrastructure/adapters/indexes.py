from typing import Generic, TypeVar

from shared.application.ports.indexes import EmptyIndexFactory, Index
from shared.domain.framework.pure.entity import Entity, Event


_EntityT = TypeVar("_EntityT", bound=Entity)


class SortingIndex(Generic[_EntityT], Index[_EntityT]):
    def __init__(self) -> None:
        self.__new_entities: set[_EntityT] = set()
        self.__dirty_entities: set[_EntityT] = set()
        self.__deleted_entities: set[_EntityT] = set()

    @property
    def entities(self) -> frozenset[_EntityT]:
        return frozenset(
            *self.__new_entities,
            *self.__dirty_entities,
            *self.__deleted_entities,
        )

    @property
    def new_entities(self) -> frozenset[_EntityT]:
        return frozenset(self.__new_entities)

    @property
    def dirty_entities(self) -> frozenset[_EntityT]:
        return frozenset(self.__dirty_entities)

    @property
    def deleted_entities(self) -> frozenset[_EntityT]:
        return frozenset(self.__deleted_entities)

    def entities_with_event(
        self, *, event_type: type[Event]
    ) -> frozenset[_EntityT]:
        return frozenset(
            entity
            for entity in self.entities
            if tuple(map(type, entity.events))
        )

    def add(self, entity: _EntityT) -> None:
        self.remove(entity)

        if entity.is_new:
            self.__new_entities.add(entity)
        elif entity.is_dirty:
            self.__dirty_entities.add(entity)
        elif entity.is_deleted:
            self.__deleted_entities.add(entity)

    def remove(self, entity: _EntityT) -> None:
        if entity in self.__new_entities:
            self.__new_entities.remove(entity)
        elif entity in self.__dirty_entities:
            self.__dirty_entities.remove(entity)
        elif entity in self.__deleted_entities:
            self.__deleted_entities.remove(entity)

    def __entity_has_event(
        self, entity: _EntityT, event_type: type[Event]
    ) -> bool:
        entity_event_types = tuple(map(type, entity.events))

        return any(
            issubclass(entity_event_type, event_type)
            for entity_event_type in entity_event_types
        )


class EmptySortingIndexFactory(Generic[_EntityT], EmptyIndexFactory[_EntityT]):
    def __call__(self) -> SortingIndex[_EntityT]:
        return SortingIndex()
