from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Generic, Self, TypeVar


class Transaction(AbstractAsyncContextManager["Transaction"]):
    async def __aenter__(self) -> Self:
        return self

    @abstractmethod
    async def rollback(self) -> None: ...


_RepoT = TypeVar("_RepoT")
_TransactionT_co = TypeVar(
    "_TransactionT_co", bound=Transaction, covariant=True
)


class TransactionFactory(Generic[_RepoT], ABC):
    @abstractmethod
    def __call__(self, repo: _RepoT) -> Transaction: ...
