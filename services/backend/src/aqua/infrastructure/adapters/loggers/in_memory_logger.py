from copy import deepcopy

from aqua.application.ports import loggers
from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import User
from aqua.infrastructure.periphery.logs.in_memory_logs import (
    NewDayLog,
    NewDayStateLog,
    NewRecordLog,
    RecordCancellationLog,
    RecordWithoutDayLog,
    RegisteredUserRegistrationLog,
    RegistredUserLog,
)


class InMemoryLogger(loggers.Logger):
    def __init__(self) -> None:
        self.__registred_user_logs = list[RegistredUserLog]()
        self.__registered_user_registration_logs = list[
            RegisteredUserRegistrationLog
        ]()
        self.__record_without_day_logs = list[RecordWithoutDayLog]()
        self.__new_day_logs = list[NewDayLog]()
        self.__new_day_state_logs = list[NewDayStateLog]()
        self.__new_record_logs = list[NewRecordLog]()
        self.__record_cancellation_logs = list[RecordCancellationLog]()

    @property
    def is_empty(self) -> bool:
        return (
            not self.__registred_user_logs
            or not self.__registered_user_registration_logs
            or not self.__record_without_day_logs
            or not self.__new_day_logs
            or not self.__new_day_state_logs
            or not self.__new_record_logs
            or not self.__record_cancellation_logs
        )

    @property
    def registred_user_logs(self) -> tuple[RegistredUserLog, ...]:
        return tuple(self.__registred_user_logs)

    @property
    def registered_user_registration_logs(
        self,
    ) -> tuple[RegisteredUserRegistrationLog, ...]:
        return tuple(self.__registered_user_registration_logs)

    @property
    def record_without_day_logs(self) -> tuple[RecordWithoutDayLog, ...]:
        return tuple(self.__record_without_day_logs)

    @property
    def new_day_logs(self) -> tuple[NewDayLog, ...]:
        return tuple(self.__new_day_logs)

    @property
    def new_day_state_logs(self) -> tuple[NewDayStateLog, ...]:
        return tuple(self.__new_day_state_logs)

    @property
    def new_record_logs(self) -> tuple[NewRecordLog, ...]:
        return tuple(self.__new_record_logs)

    @property
    def record_cancellation_logs(self) -> tuple[RecordCancellationLog, ...]:
        return tuple(self.__record_cancellation_logs)

    async def log_registered_user(self, user: User) -> None:
        log = RegistredUserLog(user=deepcopy(user))
        self.__registred_user_logs.append(log)

    async def log_registered_user_registration(self, user: User) -> None:
        log = RegisteredUserRegistrationLog(user=deepcopy(user))
        self.__registered_user_registration_logs.append(log)

    async def log_record_without_day(self, record: Record) -> None:
        log = RecordWithoutDayLog(record=deepcopy(record))
        self.__record_without_day_logs.append(log)

    async def log_new_day(self, day: Day) -> None:
        log = NewDayLog(day=deepcopy(day))
        self.__new_day_logs.append(log)

    async def log_new_day_state(self, day: Day) -> None:
        log = NewDayStateLog(day=deepcopy(day))
        self.__new_day_state_logs.append(log)

    async def log_new_record(self, record: Record) -> None:
        log = NewRecordLog(record=deepcopy(record))
        self.__new_record_logs.append(log)

    async def log_record_cancellation(self, *, record: Record) -> None:
        log = RecordCancellationLog(record=deepcopy(record))
        self.__record_cancellation_logs.append(log)
