from contextlib import AbstractAsyncContextManager
from typing import Self


class Transaction(AbstractAsyncContextManager["Transaction"]):
    async def __aenter__(self) -> Self:
        return self
