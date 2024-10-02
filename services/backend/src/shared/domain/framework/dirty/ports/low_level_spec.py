from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from shared.domain.framework.pure.entity import Entity


_EntityT = TypeVar("_EntityT", bound=Entity)


class LowLevelSpec(ABC, Generic[_EntityT]):
    @abstractmethod
    async def __call__(self, entity: _EntityT) -> bool: ...
