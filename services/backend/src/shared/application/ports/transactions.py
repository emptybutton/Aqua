from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Self, TypeVar, Generic


class Transaction(AbstractAsyncContextManager["Transaction"]):
    async def __aenter__(self) -> Self:
        return self


_RepoT = TypeVar("_RepoT")
_TransactionT_co = TypeVar(
    "_TransactionT_co",
    bound=Transaction,
    default=Transaction,
    covariant=True,
)


class TransactionFactory(ABC, Generic[_RepoT, _TransactionT_co]):
    @abstractmethod
    def __call__(self, repo: _RepoT) -> _TransactionT_co: ...
