from typing import Iterable

from aqua.application.ports.mappers import UserMapper, UserMapperTo
from aqua.domain.model.core.aggregates.user.root import User
from aqua.infrastructure.adapters.repos.in_memory.user import InMemoryUsers


class InMemoryUserMapper(UserMapper):
    def __init__(self, in_memory_users: InMemoryUsers) -> None:
        self.__in_memory_users = in_memory_users

    async def add_all(self, users: Iterable[User]) -> None:
        for user in users:
            self.__in_memory_users.add_user(user)


class InMemoryUserMapperTo(UserMapperTo[InMemoryUsers]):
    def __call__(self, in_memory_users: InMemoryUsers) -> InMemoryUserMapper:
        return InMemoryUserMapper(in_memory_users)
