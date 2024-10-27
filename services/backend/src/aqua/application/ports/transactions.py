from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Self

from aqua.domain.framework.fp.act import Act


class Transaction(AbstractAsyncContextManager["Transaction"]):
    async def __aenter__(self) -> Self:
        return self

    @abstractmethod
    async def rollback(self) -> None: ...


class TransactionFor[RepoT](Act[RepoT, Transaction]): ...
