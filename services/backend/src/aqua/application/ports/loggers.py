from abc import ABC, abstractmethod

from aqua.domain import entities


class Logger(ABC):
    @abstractmethod
    async def log_registered_user(self, user: entities.User) -> None: ...

    @abstractmethod
    async def log_registered_user_registration(
        self, user: entities.User
    ) -> None: ...

    @abstractmethod
    async def log_record_without_day(self, record: entities.Record) -> None: ...

    @abstractmethod
    async def log_day_without_records(self, day: entities.Day) -> None: ...

    @abstractmethod
    async def log_new_day(self, day: entities.Day) -> None: ...

    @abstractmethod
    async def log_new_day_state(self, day: entities.Day) -> None: ...

    @abstractmethod
    async def log_new_record(self, record: entities.Record) -> None: ...
