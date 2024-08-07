from abc import ABC, abstractmethod
from uuid import UUID

from auth.domain import entities
from auth.domain import value_objects as vos


class Users(ABC):
    @abstractmethod
    async def add(self, user: entities.User) -> None: ...

    @abstractmethod
    async def find_with_id(
        self, user_id: UUID
    ) -> entities.User | None: ...

    @abstractmethod
    async def find_with_name(
        self, username: vos.Username
    ) -> entities.User | None: ...

    @abstractmethod
    async def contains_with_name(
        self,
        username: vos.Username,
    ) -> bool: ...
