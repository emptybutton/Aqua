from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from shared.domain.framework.pure.entity import Entity


_EntityT = TypeVar("_EntityT", bound=Entity)
_RepoT = TypeVar("_RepoT")


class Mapper(ABC, Generic[_EntityT]):
    @abstractmethod
    async def add_all(self, entities: frozenset[_EntityT]) -> None: ...

    @abstractmethod
    async def update_all(self, entities: frozenset[_EntityT]) -> None: ...

    @abstractmethod
    async def delete_all(self, entities: frozenset[_EntityT]) -> None: ...


class MapperFactory(ABC, Generic[_RepoT, _EntityT]):
    @abstractmethod
    def __call__(self, repo: _RepoT) -> Mapper[_EntityT]: ...
