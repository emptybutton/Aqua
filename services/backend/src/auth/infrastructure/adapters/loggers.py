from auth.application.ports import loggers
from auth.domain import entities
from shared.infrastructure.periphery.structlog import dev_logger


class StructlogDevLogger(loggers.Logger):
    async def log_registration(
        self,
        *,
        user: entities.User,
        session: entities.Session,
    ) -> None:
        await dev_logger.ainfo("user registration", user=user, session=session)

    async def log_login(
        self,
        *,
        user: entities.User,
        session: entities.Session,
    ) -> None:
        message = "new session created"
        await dev_logger.ainfo(message, user=user, session=session)

    async def log_session_extension(
        self,
        session: entities.Session,
    ) -> None:
        message = "session extended"
        await dev_logger.ainfo(message, session=session)
