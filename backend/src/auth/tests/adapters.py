from typing import Optional, TypeVar, Iterable
from uuid import UUID

from src.auth.application.ports import repos
from src.auth.domain import entities, value_objects


class Users(repos.Users):
    def __init__(self, users: Iterable[entities.User] = tuple()) -> None:
        self.storage = list(users)

    async def add(self, user: entities.User) -> None:
        self.storage.append(user)

    async def get_by_id(
        self, user_id: UUID
    ) -> Optional[entities.User]:
        for user in self.storage:
            if user.id == user_id:
                return user

        return None

    async def get_by_name(
        self, username: value_objects.Username
    ) -> Optional[entities.User]:
        for user in self.storage:
            if user.name == username:
                return user

        return None

    async def has_with_name(self, username: value_objects.Username) -> bool:
        return any(user.name == username for user in self.storage)
