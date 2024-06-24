from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.auth.domain import entities
from src.auth.domain import value_objects


class Users(ABC):
    @abstractmethod
    async def add(self, user: entities.User) -> None: ...

    @abstractmethod
    async def get_by_id(
        self, user_id: UUID
    ) -> Optional[entities.User]: ...

    @abstractmethod
    async def get_by_name(
        self, username: value_objects.Username
    ) -> Optional[entities.User]: ...

    @abstractmethod
    async def has_with_name(self, username: value_objects.Username) -> bool: ...
