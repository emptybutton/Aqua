from abc import ABC, abstractmethod
from typing import Iterable

from aqua.application.ports.repos import Users
from aqua.domain.framework.fp.act import Act
from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import User


class DayMapper(ABC):
    @abstractmethod
    async def add_all(self, days: Iterable[Day]) -> None: ...

    @abstractmethod
    async def update_all(self, days: Iterable[Day]) -> None: ...


class RecordMapper(ABC):
    @abstractmethod
    async def add_all(self, records: Iterable[Record]) -> None: ...

    @abstractmethod
    async def update_all(self, records: Iterable[Record]) -> None: ...


class UserMapper(ABC):
    @abstractmethod
    async def add_all(self, users: Iterable[User]) -> None: ...


class UserMapperTo[UsersT: Users](Act[UsersT, UserMapper]): ...


class RecordMapperTo[UsersT: Users](Act[UsersT, RecordMapper]): ...


class DayMapperTo[UsersT: Users](Act[UsersT, DayMapper]): ...
