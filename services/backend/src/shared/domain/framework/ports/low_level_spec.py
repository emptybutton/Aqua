from abc import ABC, abstractmethod
from typing import Generic, TypeVar


_ValueT = TypeVar("_ValueT")


class LowLevelSpec(ABC, Generic[_ValueT]):
    @abstractmethod
    async def __call__(self, value: _ValueT) -> bool: ...
