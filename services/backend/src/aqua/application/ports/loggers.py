from abc import ABC, abstractmethod

from aqua.domain import entities


class Logger(ABC):
    @abstractmethod
    async def log_registered_user_registration(
        self,
        user: entities.User,
    ) -> None: ...

    @abstractmethod
    async def log_records_without_day(
        self,
        records: tuple[entities.Record, ...],
    ) -> None: ...

    @abstractmethod
    async def log_day_without_records(self, day: entities.Day) -> None: ...

    @abstractmethod
    async def log_new_day_record(
        self,
        record: entities.Record,
        *,
        day: entities.Day,
    ) -> None: ...
