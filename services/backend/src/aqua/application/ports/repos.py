from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from aqua.domain import entities


class Users(ABC):
    @abstractmethod
    async def add(self, user: entities.User) -> None: ...

    @abstractmethod
    async def find_with_id(self, user_id: UUID) -> entities.User | None: ...

    @abstractmethod
    async def contains_with_id(self, user_id: UUID) -> bool: ...


class Records(ABC):
    @abstractmethod
    async def add(self, record: entities.Record) -> None: ...

    @abstractmethod
    async def find_from(
        self, date_: date, *, user_id: UUID
    ) -> tuple[entities.Record, ...]: ...


class Days(ABC):
    @abstractmethod
    async def add(self, day: entities.Day) -> None: ...

    @abstractmethod
    async def find_from(
        self, date_: date, *, user_id: UUID
    ) -> entities.Day | None: ...

    @abstractmethod
    async def update(self, day: entities.Day) -> None: ...
