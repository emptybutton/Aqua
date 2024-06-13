from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from src.aqua.domain import entities


class Users(ABC):
    @abstractmethod
    async def add(self, user: entities.User) -> None: ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[entities.User]: ...

    @abstractmethod
    async def has_with_id(self, user_id: int) -> bool: ...


class UsersWithTodayRecords(ABC):
    @abstractmethod
    async def add(self, user: entities.User) -> None: ...

    @abstractmethod
    async def get_all(self) -> tuple[entities.User]: ...

    @abstractmethod
    async def remove_all(self) -> None: ...


class TodayRecords(ABC):
    @abstractmethod
    async def add(self, record: entities.Record) -> None: ...

    @abstractmethod
    async def remove_all(self) -> None: ...

    @abstractmethod
    async def get_all_with_user_id(
        self,
        user_id: int,
    ) -> tuple[entities.Record, ...]: ...


class PastRecords(ABC):
    @abstractmethod
    async def add(self, record: entities.Record) -> None: ...

    @abstractmethod
    async def get_on(
        self,
        date_: date,
        *,
        user_id: int,
    ) -> tuple[entities.Record, ...]: ...


class PastDays(ABC):
    @abstractmethod
    async def add(self, day: entities.Day) -> None: ...

    @abstractmethod
    async def get_on(
        self,
        date_: date,
        *,
        user_id: int,
    ) -> Optional[entities.Day]: ...
