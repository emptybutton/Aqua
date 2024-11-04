from aqua.application.ports import loggers
from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import User
from aqua.infrastructure.periphery.logs import text_logs as logs
from aqua.infrastructure.periphery.serializing.from_model.to_prod_log_data import (  # noqa: E501
    prod_log_day_of,
    prod_log_record_of,
    prod_log_user_of,
)
from aqua.infrastructure.periphery.structlog.prod_logger import (
    prod_logger,
)


class StructlogProdLogger(loggers.Logger):
    async def log_registered_user_registration(self, user: User) -> None:
        await prod_logger.awarning(
            logs.registered_user_registration_log, **prod_log_user_of(user)
        )

    async def log_record_without_day(self, record: Record) -> None:
        await prod_logger.awarning(
            logs.record_without_day_log, **prod_log_record_of(record)
        )

    async def log_new_day(self, day: Day) -> None:
        await prod_logger.ainfo(logs.new_day_log, **prod_log_day_of(day))

    async def log_new_day_state(self, day: Day) -> None:
        await prod_logger.ainfo(logs.new_day_state_log, **prod_log_day_of(day))

    async def log_new_record(self, record: Record) -> None:
        await prod_logger.ainfo(
            logs.new_record_log, **prod_log_record_of(record)
        )

    async def log_registered_user(self, user: User) -> None:
        await prod_logger.ainfo(
            logs.registered_user_log, **prod_log_user_of(user)
        )

    async def log_record_cancellation(self, *, record: Record) -> None:
        await prod_logger.ainfo(
            logs.record_cancellation_log, **prod_log_record_of(record)
        )
