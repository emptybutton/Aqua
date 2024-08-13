from uuid import UUID

from entrypoint.application.ports import loggers
from entrypoint.infrastructure.adapters import clients
from shared.infrastructure.periphery.loguru import logger


class AquaFacadeLogger(loggers.AquaLogger[clients.AquaFacade]):
    async def log_aqua_is_not_working(self, aqua: clients.AquaFacade) -> None:
        message = "aqua facade caused an unexpected error"

        for error in aqua.errors:
            logger.opt(exception=error).error(message)

    async def log_has_extra_user(
        self,
        aqua: clients.AquaFacade,
        user_id: UUID,
    ) -> None:
        message = (
            f"aqua has a user with id = {user_id}, which is not"
            " present in other parts of the system"
        )
        logger.warning(message)


class AuthFacadeLogger(loggers.AuthLogger[clients.AuthFacade]):
    async def log_auth_is_not_working(self, auth: clients.AuthFacade) -> None:
        message = "auth facade caused an unexpected error"

        for error in auth.errors:
            logger.opt(exception=error).error(message)

    async def log_has_extra_user(
        self,
        auth: clients.AuthFacade,
        user_id: UUID,
    ) -> None:
        message = (
            f"auth has a user with id = {user_id}, which is not"
            " present in other parts of the system"
        )
        logger.warning(message)
