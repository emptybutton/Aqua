from abc import ABC, abstractmethod
from typing import TypeVar

from shared.domain.framework.pure.entity import Entity


_EntityT = TypeVar("_EntityT", bound=Entity)


class HighLevelSpec(ABC):
    @abstractmethod
    async def __call__(self, entity: _EntityT) -> bool: ...
