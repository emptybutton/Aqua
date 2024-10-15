from typing import Any, Generic, TypeVar

from shared.application.ports.indexes import EmptyIndexFactory, Index
from shared.domain.framework.entity import Entity, EntityEvent


_EntityT = TypeVar("_EntityT", bound=Entity[Any, Any])


class SortingIndex(Generic[_EntityT], Index[_EntityT]):
    def __init__(self) -> None:
        self.__entities: set[_EntityT] = set()

    @property
    def entities(self) -> frozenset[_EntityT]:
        return frozenset(self.__entities)

    @property
    def new_entities(self) -> frozenset[_EntityT]:
        return frozenset(entity for entity in self.__entities if entity.is_new)

    @property
    def dirty_entities(self) -> frozenset[_EntityT]:
        return frozenset(
            entity for entity in self.__entities if entity.is_dirty
        )

    def entities_with_event(
        self, *, event_type: type[EntityEvent[Any]]
    ) -> frozenset[_EntityT]:
        return frozenset(
            entity
            for entity in self.entities
            for event in entity.events
            if isinstance(event, event_type)
        )

    def add(self, entity: _EntityT) -> None:
        self.remove(entity)
        self.__entities.add(entity)

    def remove(self, entity: _EntityT) -> None:
        if entity in self.__entities:
            self.__entities.remove(entity)


class EmptySortingIndexFactory(EmptyIndexFactory):
    def __call__(self, entity_type: type[_EntityT]) -> SortingIndex[_EntityT]:
        return SortingIndex()
