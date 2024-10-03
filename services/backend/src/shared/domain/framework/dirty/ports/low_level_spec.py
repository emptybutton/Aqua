from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from shared.domain.framework.pure.entity import Entity


_ValueT = TypeVar("_ValueT", bound=Entity)


class LowLevelSpec(ABC, Generic[_ValueT]):
    @abstractmethod
    async def __call__(self, value: _ValueT) -> bool: ...
