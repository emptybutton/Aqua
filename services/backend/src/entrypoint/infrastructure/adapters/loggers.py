from uuid import UUID

from entrypoint.application.ports import loggers
from entrypoint.infrastructure.adapters import clients
from shared.infrastructure.periphery.structlog import dev_logger


class AquaFacadeDevLogger(loggers.AquaLogger[clients.AquaFacade]):
    async def log_aqua_is_not_working(self, aqua: clients.AquaFacade) -> None:
        message = "aqua facade caused an unexpected error"

        for error in aqua.errors:
            await dev_logger.aerror(message, exc_info=error)

    async def log_no_user_from_other_parts(
        self,
        aqua: clients.AquaFacade,
        user_id: UUID,
    ) -> None:
        message = "aqua does not have a user that is in other modules"
        await dev_logger.awarning(message, user_id=user_id)


class AuthFacadeDevLogger(loggers.AuthLogger[clients.AuthFacade]):
    async def log_auth_is_not_working(self, auth: clients.AuthFacade) -> None:
        message = "auth facade caused an unexpected error"

        for error in auth.errors:
            await dev_logger.aerror(message, exc_info=error)

    async def log_no_user_from_other_parts(
        self,
        auth: clients.AuthFacade,
        user_id: UUID,
    ) -> None:
        message = "auth does not have a user that is in other modules"
        await dev_logger.awarning(message, user_id=user_id)
