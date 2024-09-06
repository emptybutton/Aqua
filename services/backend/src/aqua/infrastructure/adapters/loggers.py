from copy import copy
from dataclasses import dataclass
from functools import singledispatchmethod
from typing import Any

from aqua.application.ports import loggers
from aqua.domain import entities
from aqua.infrastructure.periphery import logs
from shared.infrastructure.periphery.structlog import dev_logger, prod_logger


class _Mapper:
    @singledispatchmethod
    def to_dict(self, value: object) -> dict[str, Any]:
        raise NotImplementedError

    @to_dict.register
    def _(self, user: entities.User) -> dict[str, Any]:
        suitable_milliliters = user.suitable_water_balance.water.milliliters
        kilograms = None if user.weight is None else user.weight.kilograms

        return dict(
            user_id=user.id,
            user_weight_kilograms=kilograms,
            user_glass_water_milliliters=user.glass.capacity.milliliters,
            user_target_water_balance_milliliters=user.target.water.milliliters,
            user_suitable_target_water_balance_milliliters=suitable_milliliters,
        )

    @to_dict.register
    def _(self, record: entities.Record) -> dict[str, Any]:
        return dict(
            record_id=record.id,
            record_user_id=record.user_id,
            record_drunk_water_milliliters=record.drunk_water.milliliters,
            recording_time=record.recording_time,
            is_record_accidental=record.is_accidental,
        )

    @to_dict.register
    def _(self, day: entities.Day) -> dict[str, Any]:
        return dict(
            day_id=day.id,
            day_user_id=day.user_id,
            day_date=day.date_,
            day_target_water_balance_milliliters=day.target.water.milliliters,
            day_water_balance_milliliters=day.water_balance.water.milliliters,
            day_result_code=day.result.value,
            day_correct_result_code=day.correct_result.value,
            is_day_result_pinned=day.is_result_pinned,
        )


class StructlogDevLogger(loggers.Logger):
    async def log_registered_user_registration(
        self, user: entities.User
    ) -> None:
        log = logs.registered_user_registration_log
        await dev_logger.awarning(log, user=user)

    async def log_record_without_day(self, record: entities.Record) -> None:
        await dev_logger.awarning(logs.record_without_day_log, record=record)

    async def log_day_without_records(self, day: entities.Day) -> None:
        await dev_logger.awarning(logs.day_without_records_log, day=day)

    async def log_new_day(self, day: entities.Day) -> None:
        await dev_logger.ainfo(logs.new_day_log, day=day)

    async def log_new_day_state(self, day: entities.Day) -> None:
        await dev_logger.ainfo(logs.new_day_state_log, day=day)

    async def log_new_record(self, record: entities.Record) -> None:
        await dev_logger.ainfo(logs.new_record_log, record=record)

    async def log_registered_user(self, user: entities.User) -> None:
        await dev_logger.ainfo(logs.registered_user_log, user=user)

    async def log_record_cancellation(
        self,
        *,
        record: entities.Record,
        day: entities.Day,
    ) -> None:
        await dev_logger.ainfo(
            logs.record_cancellation_log,
            record=record,
            day=day,
        )


class StructlogProdLogger(loggers.Logger):
    __mapper = _Mapper()

    async def log_registered_user_registration(
        self, user: entities.User
    ) -> None:
        await prod_logger.awarning(
            logs.registered_user_registration_log, **self.__mapper.to_dict(user)
        )

    async def log_record_without_day(self, record: entities.Record) -> None:
        await prod_logger.awarning(
            logs.record_without_day_log, **self.__mapper.to_dict(record)
        )

    async def log_day_without_records(self, day: entities.Day) -> None:
        await prod_logger.awarning(
            logs.day_without_records_log, **self.__mapper.to_dict(day)
        )

    async def log_new_day(self, day: entities.Day) -> None:
        await prod_logger.ainfo(logs.new_day_log, **self.__mapper.to_dict(day))

    async def log_new_day_state(self, day: entities.Day) -> None:
        await prod_logger.ainfo(
            logs.new_day_state_log, **self.__mapper.to_dict(day)
        )

    async def log_new_record(self, record: entities.Record) -> None:
        await prod_logger.ainfo(
            logs.new_record_log, **self.__mapper.to_dict(record)
        )

    async def log_registered_user(self, user: entities.User) -> None:
        await prod_logger.ainfo(
            logs.registered_user_log, **self.__mapper.to_dict(user)
        )

    async def log_record_cancellation(
        self,
        *,
        record: entities.Record,
        day: entities.Day,
    ) -> None:
        await prod_logger.ainfo(
            logs.record_cancellation_log,
            **self.__mapper.to_dict(record),
            **self.__mapper.to_dict(day),
        )


class InMemoryStorageLogger(loggers.Logger):
    @dataclass(kw_only=True, frozen=True)
    class RecordCancellationLog:
        record: entities.Record
        day: entities.Day

    __record_cancellation_logs: list[RecordCancellationLog]

    def __init__(self) -> None:
        self.__registered_users: list[entities.User] = list()
        self.__before_registered_users: list[entities.User] = list()
        self.__records_without_day: list[entities.Record] = list()
        self.__days_without_records: list[entities.Day] = list()
        self.__new_days: list[entities.Day] = list()
        self.__days_with_new_state: list[entities.Day] = list()
        self.__new_records: list[entities.Record] = list()
        self.__record_cancellation_logs = list()

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
            and len(self.__record_cancellation_logs) == 0
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

    @property
    def record_cancellation_logs(self) -> tuple[RecordCancellationLog, ...]:
        return tuple(map(copy, self.__record_cancellation_logs))

    async def log_registered_user(self, user: entities.User) -> None:
        self.__registered_users.append(user)

    async def log_registered_user_registration(
        self, user: entities.User
    ) -> None:
        self.__before_registered_users.append(user)

    async def log_record_without_day(self, record: entities.Record) -> None:
        self.__records_without_day.append(record)

    async def log_day_without_records(self, day: entities.Day) -> None:
        self.__days_without_records.append(day)

    async def log_new_day(self, day: entities.Day) -> None:
        self.__new_days.append(day)

    async def log_new_day_state(self, day: entities.Day) -> None:
        self.__days_with_new_state.append(day)

    async def log_new_record(self, record: entities.Record) -> None:
        self.__new_records.append(record)

    async def log_record_cancellation(
        self,
        *,
        record: entities.Record,
        day: entities.Day,
    ) -> None:
        log = InMemoryStorageLogger.RecordCancellationLog(
            record=record, day=day
        )
        self.__record_cancellation_logs.append(log)
