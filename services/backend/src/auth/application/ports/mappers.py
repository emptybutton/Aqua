from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from auth.domain.framework.entity import Entity
from auth.domain.models.access.aggregates import account as _account


_EntityT_co = TypeVar("_EntityT_co", bound=Entity[Any, Any], covariant=True)
_RepoT = TypeVar("_RepoT")


class Mapper(Generic[_EntityT_co], ABC):
    @abstractmethod
    async def add_all(self, entities: frozenset[_EntityT_co]) -> None: ...

    @abstractmethod
    async def update_all(self, entities: frozenset[_EntityT_co]) -> None: ...


class MapperFactory(Generic[_RepoT, _EntityT_co], ABC):
    @abstractmethod
    def __call__(self, repo: _RepoT) -> Mapper[_EntityT_co]: ...


class AccountMapper(Mapper[_account.root.Account]): ...


class AccountNameMapper(
    Mapper[_account.internal.entities.account_name.AccountName]
): ...


class SessionMapper(Mapper[_account.internal.entities.session.Session]): ...
