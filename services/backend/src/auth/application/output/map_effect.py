from functools import cached_property
from typing import cast

from auth.application.ports.mappers import Mapper
from auth.domain.framework.effects.searchable import SearchableEffect
from auth.domain.framework.entity import AnyEntity, Created, Mutated


class Mappers:
    type _Pair[EntityT: AnyEntity] = tuple[type[EntityT], Mapper[EntityT]]

    def __init__(self, *pairs: _Pair[AnyEntity]) -> None:
        self.__pairs = pairs

    def mapper_for[EntityT: AnyEntity](
        self, entity_type: type[EntityT]
    ) -> Mapper[EntityT] | None:
        for pair in self.__pairs:
            if pair[0] is entity_type:
                return cast(Mapper[EntityT], pair[1])

        return None

    @cached_property
    def entity_types(self) -> frozenset[type[AnyEntity]]:
        return frozenset(pair[0] for pair in self.__pairs)


class Error(Exception): ...


class NoMapperError(Exception): ...


async def map_effect(effect: SearchableEffect, mappers: Mappers) -> None:
    for entity_type in mappers.entity_types:
        mapper = mappers.mapper_for(entity_type)

        if mapper is None:
            raise NoMapperError

        entities = effect.entities_that(entity_type)

        created_entities = entities.with_event(Created)
        mutated_entities = entities.with_event(Mutated)

        await mapper.add_all(frozenset(created_entities))
        await mapper.update_all(frozenset(mutated_entities))
