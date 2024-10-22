from abc import ABC, abstractmethod

from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import User


class Logger(ABC):
    @abstractmethod
    async def log_registered_user(self, user: User) -> None: ...

    @abstractmethod
    async def log_registered_user_registration(self, user: User) -> None: ...

    @abstractmethod
    async def log_record_without_day(self, record: Record) -> None: ...

    @abstractmethod
    async def log_new_day(self, day: Day) -> None: ...

    @abstractmethod
    async def log_new_day_state(self, day: Day) -> None:
        ...

    @abstractmethod
    async def log_new_record(self, record: Record) -> None: ...

    @abstractmethod
    async def log_record_cancellation(self, *, record: Record) -> None: ...
