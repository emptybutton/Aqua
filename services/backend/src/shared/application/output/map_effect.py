from functools import cached_property
from typing import Any, TypeAlias, TypeVar, cast

from shared.application.adapters.effects import IndexedEffect
from shared.application.ports.mappers import Mapper
from shared.domain.framework.entity import Entity


_EntityT = TypeVar("_EntityT", bound=Entity[Any, Any])


class Mappers:
    _Pair: TypeAlias = tuple[type[_EntityT], Mapper[_EntityT]]

    def __init__(self, *pairs: _Pair[Entity[Any, Any]]) -> None:
        self.__pairs = pairs

    def mapper_for(
        self, entity_type: type[_EntityT]
    ) -> Mapper[_EntityT] | None:
        for pair in self.__pairs:
            if pair[0] is entity_type:
                return cast(Mapper[_EntityT], pair[1])

        return None

    @cached_property
    def entity_types(self) -> tuple[type[Entity[Any, Any]], ...]:
        return tuple(pair[0] for pair in self.__pairs)


class Error(Exception): ...


class NoMapperError(Exception): ...


async def map_effect(effect: IndexedEffect, mappers: Mappers) -> None:
    for entity_type in mappers.entity_types:
        mapper = mappers.mapper_for(entity_type)

        if mapper is None:
            raise NoMapperError

        new_entities = effect.new_entities_with_type(entity_type)
        dirty_entities = effect.dirty_entities_with_type(entity_type)
        deleted_entities = effect.deleted_entities_with_type(entity_type)

        await mapper.add_all(new_entities)
        await mapper.update_all(dirty_entities)
        await mapper.delete_all(deleted_entities)
