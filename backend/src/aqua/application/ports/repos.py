from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID
from typing import Optional

from src.aqua.domain import entities


class Users(ABC):
    @abstractmethod
    async def add(self, user: entities.User) -> None: ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[entities.User]: ...

    @abstractmethod
    async def has_with_id(self, user_id: UUID) -> bool: ...


class Records(ABC):
    @abstractmethod
    async def add(self, record: entities.Record) -> None: ...

    @abstractmethod
    async def get_on(
        self,
        date_: date,
        *,
        user_id: UUID,
    ) -> tuple[entities.Record, ...]: ...


class Days(ABC):
    @abstractmethod
    async def add(self, day: entities.Day) -> None: ...

    @abstractmethod
    async def get_on(
        self,
        date_: date,
        *,
        user_id: UUID,
    ) -> Optional[entities.Day]: ...
