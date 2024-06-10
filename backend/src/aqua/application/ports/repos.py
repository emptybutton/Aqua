from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from src.aqua.domain import entities


class Users(ABC):
    @abstractmethod
    async def add(self, user: entities.User) -> None: ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[entities.User]: ...


class Records(ABC):
    @abstractmethod
    async def add(self, record: entities.Record) -> None: ...


class Days(ABC):
    @abstractmethod
    async def add(self, day: entities.Day) -> None: ...

    @abstractmethod
    async def get_on(self, date_: date) -> Optional[entities.Day]: ...
