from typing import TypeVar

from shared.application.ports.indexes import EmptyIndexFactory, Index
from shared.domain.framework.pure.entity import Entity
from shared.domain.framework.pure.ports.effect import Effect, Event


_EntityT = TypeVar("_EntityT", bound=Entity)


class IndexedEffect(Effect):
    def __init__(
        self,
        *,
        empty_index_factory: EmptyIndexFactory,
        index_by_entity_type: dict[type[Entity], Index[Entity]] | None = None,
    ) -> None:
        self.__create_empty_index = empty_index_factory
        self.__index_by_entity_type: dict[type[Entity], Index[Entity]]

        if index_by_entity_type is None:
            self.__index_by_entity_type = dict()
        else:
            self.__index_by_entity_type = index_by_entity_type

    def new_entities_with_type(
        self, entity_type: type[_EntityT]
    ) -> frozenset[_EntityT]:
        index = self.__index_by_entity_type.get(entity_type)

        if index is None:
            return frozenset()

        return index.new_entities

    def dirty_entities_with_type(
        self, entity_type: type[_EntityT]
    ) -> frozenset[_EntityT]:
        index = self.__index_by_entity_type.get(entity_type)

        if index is None:
            return frozenset()

        return index.dirty_entities

    def deleted_entities_with_type(
        self, entity_type: type[_EntityT]
    ) -> frozenset[_EntityT]:
        index = self.__index_by_entity_type.get(entity_type)

        if index is None:
            return frozenset()

        return index.deleted_entities

    def entities_with_event(
        self,
        *,
        event_type: type[Event],
        entity_type: _EntityT,
    ) -> frozenset[_EntityT]:
        index = self.__index_by_entity_type.get(entity_type)

        if index is None:
            return frozenset()

        return index.entities_with_event(event_type=event_type)

    def consider(self, *entities: Entity) -> None:
        for entity in entities:
            self.__consider_one(entity)

    def ignore(self, *entities: Entity) -> None:
        for entity in entities:
            self.__ignore_one(entity)

    def cancel(self) -> None:
        self.__index_by_entity_type = dict()

    def __consider_one(self, entity: Entity) -> None:
        index = self.__index_by_entity_type.get(type(entity))

        if index is None:
            index = self.__create_empty_index()
            self.__index_by_entity_type[type(entity)] = index

        index.add(entity)

    def __ignore_one(self, entity: Entity) -> None:
        index = self.__index_by_entity_type.get(type(entity))

        if index is None:
            return

        index.remove(entity)
