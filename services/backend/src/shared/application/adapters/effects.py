from typing import Any, TypeAlias, TypeVar, cast

from shared.application.ports.indexes import EmptyIndexFactory, Index
from shared.domain.framework.entity import Entity, EntityEvent
from shared.domain.framework.ports.effect import Effect


_EntityT = TypeVar("_EntityT", bound=Entity[Any, Any])


class IndexedEffect(Effect):
    _IndexByEntityType: TypeAlias = (
        dict[type[Entity[Any, Any]], Index[Entity[Any, Any]]]
    )

    def __init__(
        self,
        *,
        empty_index_factory: EmptyIndexFactory,
        index_by_entity_type: _IndexByEntityType | None = None,
    ) -> None:
        self.__create_empty_index = empty_index_factory
        self.__index_by_entity_type: IndexedEffect._IndexByEntityType

        if index_by_entity_type is None:
            self.__index_by_entity_type = dict()
        else:
            self.__index_by_entity_type = index_by_entity_type

    def new_entities_with_type(
        self, entity_type: type[_EntityT]
    ) -> frozenset[_EntityT]:
        index = self.__index_for(entity_type)

        if index is None:
            return frozenset()

        return index.new_entities

    def dirty_entities_with_type(
        self, entity_type: type[_EntityT]
    ) -> frozenset[_EntityT]:
        index = self.__index_for(entity_type)

        if index is None:
            return frozenset()

        return index.dirty_entities

    def deleted_entities_with_type(
        self, entity_type: type[_EntityT]
    ) -> frozenset[_EntityT]:
        index = self.__index_for(entity_type)

        if index is None:
            return frozenset()

        return index.deleted_entities

    def entities_with_event(
        self,
        *,
        event_type: type[EntityEvent[Any]],
        entity_type: type[_EntityT],
    ) -> frozenset[_EntityT]:
        index = self.__index_for(entity_type)

        if index is None:
            return frozenset()

        return index.entities_with_event(event_type=event_type)

    def consider(self, *entities: Entity[Any, Any]) -> None:
        for entity in entities:
            self.__consider_one(entity)

    def ignore(self, *entities: Entity[Any, Any]) -> None:
        for entity in entities:
            self.__ignore_one(entity)

    def cancel(self) -> None:
        self.__index_by_entity_type = dict()

    def __consider_one(self, entity: Entity[Any, Any]) -> None:
        index = self.__index_for(type(entity))

        if index is None:
            index = self.__create_empty_index(type(entity))
            self.__index_by_entity_type[type(entity)] = index

        index.add(entity)

    def __ignore_one(self, entity: Entity[Any, Any]) -> None:
        index = self.__index_for(type(entity))

        if index is None:
            return

        index.remove(entity)

    def __index_for(
        self, entity_type: type[_EntityT]
    ) -> Index[_EntityT] | None:
        index = self.__index_by_entity_type.get(entity_type)

        return None if index is None else cast(Index[_EntityT], index)
