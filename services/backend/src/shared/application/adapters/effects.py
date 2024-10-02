from dataclasses import dataclass, field
from typing import Generic, TypeVar, Iterator

from shared.domain.framework.pure.entity import Entity
from shared.domain.framework.pure.ports.effect import Effect


_EntityT = TypeVar("_EntityT", bound=Entity)


class IndexedEffect(Effect):
    @dataclass(kw_only=True, frozen=True, slots=True)
    class Index(Generic[_EntityT]):
        new_enitties: set[_EntityT] = field(default_factory=set)
        dirty_enitties: set[_EntityT] = field(default_factory=set)

    def __init__(self) -> None:
        self.__index_by_entity_type: dict[
            type[Entity], IndexedEffect.Index[Entity]
        ]
        self.__index_by_entity_type = dict()

    @property
    def entity_types(self) -> frozenset[type[Entity]]:
        return frozenset(self.__index_by_entity_type.keys())

    def __iter__(self) -> Iterator[Entity]:
        for index in self.__index_by_type.values():
            yield from index.new_enitties
            yield from index.dirty_enitties

    def consider(self, *entities: Entity) -> None:
        for entity in entities:
            self.__index_by_type.setdefault() [type(entity)].add(entity)

    def ignore(self, *entities: Entity) -> None:
        for entity in entities:
            if type(entity) in self.__entities_by_type.keys():
                self.__entities_by_type[type(entity)].remove(entity)

    def cancel(self) -> None:
        self.__entities_by_type = defaultdict(set)

    def __index_for(
        self, entity_type: type[_EntityT]
    ) -> Index[_EntityT] | None:
        return self.__index_by_entity_type.get(entity_type)


# @abstractmethod
# def __iter__(self) -> Iterator["Entity"]: ...

# @abstractmethod
# def consider(self, *entities: "Entity") -> None: ...

# @abstractmethod
# def ignore(self, *entities: "Entity") -> None: ...

# @abstractmethod
# def cancel(self) -> None: ...

# @abstractmethod
# def clone(self) -> "Effect[Entity]": ...
