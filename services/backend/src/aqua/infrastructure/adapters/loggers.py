from aqua.application.ports import loggers
from aqua.domain import entities
from shared.infrastructure.periphery.structlog import dev_logger


class StructlogDevLogger(loggers.Logger):
    async def log_registered_user_registration(
        self,
        user: entities.User,
    ) -> None:
        message = "attempt to register a registered user"
        await dev_logger.awarning(message, user=user)

    async def log_record_without_day(
        self,
        record: entities.Record,
    ) -> None:
        message = "record exists without day"
        await dev_logger.awarning(message, record=record)

    async def log_day_without_records(self, day: entities.Day) -> None:
        await dev_logger.awarning("day exists without records", day=day)

    async def log_new_day(self, day: entities.Day) -> None:
        await dev_logger.ainfo("new day", day=day)

    async def log_new_day_state(self, day: entities.Day) -> None:
        await dev_logger.ainfo("new day state", day=day)

    async def log_new_record(
        self,
        record: entities.Record,
    ) -> None:
        await dev_logger.ainfo("new record", record=record)

    async def log_registered_user(self, user: entities.User) -> None:
        await dev_logger.ainfo("new user in aqua module", user=user)
