from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID


_ViewT = TypeVar("_ViewT")
_RepoT = TypeVar("_RepoT")


class AccountViewFrom(Generic[_RepoT, _ViewT], ABC):
    @abstractmethod
    async def __call__(self, repo: _RepoT, *, account_id: UUID) -> _ViewT: ...
