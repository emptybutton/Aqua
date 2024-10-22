from abc import ABC, abstractmethod
from typing import Iterable

from aqua.application.ports.repos import Users
from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import User
from shared.application.ports import mappers


class DayMapper(mappers.Mapper[Day]): ...


class RecordMapper(mappers.Mapper[Record]): ...


class UserMapeper(ABC):
    @abstractmethod
    async def add_all(self, users: Iterable[User]) -> None: ...


class UserMapeperFactory[UsersT: Users](ABC):
    @abstractmethod
    async def __call__(self, users: UsersT) -> UserMapeper: ...
