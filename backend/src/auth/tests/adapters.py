from typing import Optional, TypeVar, Generic, Iterable

from src.auth.application.ports import places, repos
from src.auth.domain import entities, value_objects


_Value = TypeVar("_Value")


class Place(Generic[_Value], places.Place[_Value]):
    def __init__(self, value: Optional[_Value] = None) -> None:
        self.__value = value

    def get(self) -> Optional[_Value]:
        return self.__value

    def set(self, value: Optional[_Value]) -> None:
        self.__value = value


class Users(repos.Users):
    def __init__(self, users: Iterable[entities.User] = tuple()) -> None:
        self.storage = list(users)

    async def add(self, user: entities.User) -> None:
        self.storage.append(user)

    async def get_by_name(
        self, username: value_objects.Username
    ) -> Optional[entities.User]:
        for user in self.storage:
            if user.name == username:
                return user

        return None

    async def has_with_name(self, username: value_objects.Username) -> bool:
        return any(user.name == username for user in self.storage)
