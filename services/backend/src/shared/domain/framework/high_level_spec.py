from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from shared.domain.framework.entity import Entity


_EntityT = TypeVar("_EntityT", bound=Entity[Any, Any])


class HighLevelSpec(Generic[_EntityT], ABC):
    @abstractmethod
    async def __call__(self, entity: _EntityT) -> bool: ...
