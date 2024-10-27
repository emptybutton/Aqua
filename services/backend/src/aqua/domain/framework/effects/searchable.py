from typing import Iterable, cast

from aqua.domain.framework.effects.base import Effect
from aqua.domain.framework.entity import AnyEntity, Entities, FrozenEntities


type _EntityMap = dict[type[AnyEntity], Entities[AnyEntity]]


class SearchableEffect(Effect):
    def __init__(self, entities: Iterable[AnyEntity] = tuple()) -> None:
        self.__entity_map: _EntityMap = dict()
        self.consider(*entities)

    def entities_that[EntityT: AnyEntity](
        self, entity_type: type[EntityT]
    ) -> FrozenEntities[EntityT]:
        entities = self.__entities_of(entity_type)

        if entities is None:
            return FrozenEntities()

        return FrozenEntities(entities)

    def consider(self, *entities: AnyEntity) -> None:
        for entity in entities:
            self.__consider_one(entity)

    def ignore(self, *entities: AnyEntity) -> None:
        for entity in entities:
            self.__ignore_one(entity)

    def cancel(self) -> None:
        self.__entity_map = dict()

    def __consider_one(self, entity: AnyEntity) -> None:
        entities = self.__entities_of(type(entity))

        if entities is None:
            entities = self.__casted(Entities(), entity=entity)
            self.__entity_map[type(entity)] = entities

        entities.add(entity)

    def __ignore_one(self, entity: AnyEntity) -> None:
        entities = self.__entities_of(type(entity))

        if entities is None:
            return

        entities.remove(entity)

    def __entities_of[EntityT: AnyEntity](
        self, entity_type: type[EntityT]
    ) -> Entities[EntityT] | None:
        entities = self.__entity_map.get(entity_type)

        return None if entities is None else cast(Entities[EntityT], entities)

    def __casted[EntityT: AnyEntity](
        self,
        entities: Entities[AnyEntity],
        *,
        entity: EntityT,  # noqa: ARG002
    ) -> Entities[EntityT]:
        return cast(Entities[EntityT], entities)
