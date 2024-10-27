from abc import ABC, abstractmethod
from uuid import UUID

from aqua.domain.model.core.aggregates.user.root import User


class Users(ABC):
    @abstractmethod
    async def user_with_id(self, user_id: UUID) -> User | None: ...
