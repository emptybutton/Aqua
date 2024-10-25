from aqua.application.ports import loggers
from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import User
from aqua.infrastructure.periphery.loggers.structlog.dev_logger import (
    dev_logger,
)
from aqua.infrastructure.periphery.logs import text_logs as logs


class StructlogDevLogger(loggers.Logger):
    async def log_registered_user_registration(self, user: User) -> None:
        log = logs.registered_user_registration_log
        await dev_logger.awarning(log, user=user)

    async def log_record_without_day(self, record: Record) -> None:
        await dev_logger.awarning(logs.record_without_day_log, record=record)

    async def log_new_day(self, day: Day) -> None:
        await dev_logger.ainfo(logs.new_day_log, day=day)

    async def log_new_day_state(self, day: Day) -> None:
        await dev_logger.ainfo(logs.new_day_state_log, day=day)

    async def log_new_record(self, record: Record) -> None:
        await dev_logger.ainfo(logs.new_record_log, record=record)

    async def log_registered_user(self, user: User) -> None:
        await dev_logger.ainfo(logs.registered_user_log, user=user)

    async def log_record_cancellation(self, *, record: Record) -> None:
        await dev_logger.ainfo(logs.record_cancellation_log, record=record)
