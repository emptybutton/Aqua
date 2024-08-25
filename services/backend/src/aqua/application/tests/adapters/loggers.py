from copy import copy

from aqua.application.ports import loggers
from aqua.domain import entities


class SavingLogger(loggers.Logger):
    def __init__(self) -> None:
        self.__registered_users: list[entities.User] = list()
        self.__before_registered_users: list[entities.User] = list()
        self.__records_without_day: list[entities.Record] = list()
        self.__days_without_records: list[entities.Day] = list()
        self.__new_days: list[entities.Day] = list()
        self.__days_with_new_state: list[entities.Day] = list()
        self.__new_records: list[entities.Record] = list()

    @property
    def is_empty(self) -> bool:
        return (
            len(self.__registered_users) == 0
            and len(self.__before_registered_users) == 0
            and len(self.__records_without_day) == 0
            and len(self.__days_without_records) == 0
            and len(self.__new_days) == 0
            and len(self.__days_with_new_state) == 0
            and len(self.__new_records) == 0
        )

    @property
    def registered_users(self) -> tuple[entities.User, ...]:
        return tuple(map(copy, self.__registered_users))

    @property
    def before_registered_users(self) -> tuple[entities.User, ...]:
        return tuple(map(copy, self.__before_registered_users))

    @property
    def records_without_day(self) -> tuple[entities.Record, ...]:
        return tuple(map(copy, self.__records_without_day))

    @property
    def days_without_records(self) -> tuple[entities.Day, ...]:
        return tuple(map(copy, self.__days_without_records))

    @property
    def new_days(self) -> tuple[entities.Day, ...]:
        return tuple(map(copy, self.__new_days))

    @property
    def days_with_new_state(self) -> tuple[entities.Day, ...]:
        return tuple(map(copy, self.__days_with_new_state))

    @property
    def new_records(self) -> tuple[entities.Record, ...]:
        return tuple(map(copy, self.__new_records))

    async def log_registered_user(self, user: entities.User) -> None:
        self.__registered_users.append(user)

    async def log_registered_user_registration(
        self,
        user: entities.User,
    ) -> None:
        self.__before_registered_users.append(user)

    async def log_record_without_day(
        self,
        record: entities.Record,
    ) -> None:
        self.__records_without_day.append(record)

    async def log_day_without_records(self, day: entities.Day) -> None:
        self.__days_without_records.append(day)

    async def log_new_day(self, day: entities.Day) -> None:
        self.__new_days.append(day)

    async def log_new_day_state(self, day: entities.Day) -> None:
        self.__days_with_new_state.append(day)

    async def log_new_record(self, record: entities.Record) -> None:
        self.__new_records.append(record)
