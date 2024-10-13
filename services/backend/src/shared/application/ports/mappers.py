from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from shared.domain.framework.entity import Entity


_EntityT_co = TypeVar("_EntityT_co", bound=Entity[Any, Any], covariant=True)
_RepoT = TypeVar("_RepoT")


class Mapper(Generic[_EntityT_co], ABC):
    @abstractmethod
    async def add_all(self, entities: frozenset[_EntityT_co]) -> None: ...

    @abstractmethod
    async def update_all(self, entities: frozenset[_EntityT_co]) -> None: ...


class MapperFactory(ABC, Generic[_RepoT, _EntityT_co]):
    @abstractmethod
    def __call__(self, repo: _RepoT) -> Mapper[_EntityT_co]: ...
