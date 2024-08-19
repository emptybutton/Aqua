from aqua.application.ports import loggers
from aqua.domain import entities
from shared.infrastructure.periphery.loguru import logger


class LoguruLogger(loggers.Logger):
    async def log_registered_user_registration(
        self,
        user: entities.User,
    ) -> None:
        message = f"attempt to register a registered user with id = {user.id}"
        logger.warning(message)

    async def log_records_without_day(
        self,
        records: tuple[entities.Record, ...],
    ) -> None:
        for record in records:
            message = f"record with id = {record.id} exists without day"
            logger.warning(message)

    async def log_day_without_records(self, day: entities.Day) -> None:
        message = f"day with id = {day.id} exists without records"
        logger.warning(message)

    async def log_new_day_record(
        self,
        record: entities.Record,
        *,
        day: entities.Day,
    ) -> None:
        logger.info(
            f"New record with id = {record.id}, for day with id = {day.id}"
        )
