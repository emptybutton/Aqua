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
