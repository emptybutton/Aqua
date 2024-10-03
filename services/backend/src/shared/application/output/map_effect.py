from typing import TypeVar, cast

from shared.application.adapters.effects import IndexedEffect
from shared.application.ports.mappers import Mapper
from shared.domain.framework.entity import Entity


_EntityT = TypeVar("_EntityT", bound=Entity)


async def map_effect(
    effect: IndexedEffect,
    mapper_by_entity_type: dict[type[Entity], Mapper[Entity]],
) -> None:
    for entity_type in mapper_by_entity_type:
        mapper = _mapper_in(mapper_by_entity_type, for_=entity_type)

        new_entities = effect.new_entities_with_type(entity_type)
        dirty_entities = effect.dirty_entities_with_type(entity_type)
        deleted_entities = effect.deleted_entities_with_type(entity_type)

        await mapper.add_all(new_entities)
        await mapper.update_all(dirty_entities)
        await mapper.delete_all(deleted_entities)


def _mapper_in(
    mapper_by_entity_type: dict[type[Entity], Mapper[Entity]],
    *,
    for_: type[_EntityT],
) -> Mapper[_EntityT]:
    entity_type = for_

    return cast(Mapper[_EntityT], mapper_by_entity_type[entity_type])
