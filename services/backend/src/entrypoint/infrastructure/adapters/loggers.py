from uuid import UUID

from entrypoint.application.ports import loggers
from entrypoint.infrastructure.adapters import clients
from entrypoint.infrastructure.periphery import logs
from shared.infrastructure.periphery.structlog import dev_logger, prod_logger


class AquaFacadeDevLogger(loggers.AquaLogger[clients.AquaFacade]):
    async def log_aqua_is_not_working(self, aqua: clients.AquaFacade) -> None:
        for error in aqua.errors:
            await dev_logger.aerror(
                logs.aqua_is_not_working_log,
                exc_info=error,
            )

    async def log_no_user_from_other_parts(
        self,
        aqua: clients.AquaFacade,
        user_id: UUID,
    ) -> None:
        await dev_logger.awarning(
            logs.no_user_in_aqua_from_other_parts_log,
            user_id=user_id,
        )


class AuthFacadeDevLogger(loggers.AuthLogger[clients.AuthFacade]):
    async def log_auth_is_not_working(self, auth: clients.AuthFacade) -> None:
        for error in auth.errors:
            await dev_logger.aerror(
                logs.auth_is_not_working_log,
                exc_info=error,
            )

    async def log_no_user_from_other_parts(
        self,
        auth: clients.AuthFacade,
        user_id: UUID,
    ) -> None:
        await dev_logger.awarning(
            logs.no_user_in_auth_from_other_parts_log,
            user_id=user_id,
        )


class AquaFacadeProdLogger(loggers.AquaLogger[clients.AquaFacade]):
    async def log_aqua_is_not_working(self, aqua: clients.AquaFacade) -> None:
        for error in aqua.errors:
            await dev_logger.aerror(
                logs.aqua_is_not_working_log,
                exc_info=error,
            )

    async def log_no_user_from_other_parts(
        self,
        aqua: clients.AquaFacade,
        user_id: UUID,
    ) -> None:
        await dev_logger.awarning(
            logs.no_user_in_aqua_from_other_parts_log,
            user_id=user_id,
        )


class AuthFacadeProdLogger(loggers.AuthLogger[clients.AuthFacade]):
    async def log_auth_is_not_working(self, auth: clients.AuthFacade) -> None:
        for error in auth.errors:
            await prod_logger.aerror(
                logs.auth_is_not_working_log,
                exc_info=error,
            )

    async def log_no_user_from_other_parts(
        self,
        auth: clients.AuthFacade,
        user_id: UUID,
    ) -> None:
        await prod_logger.awarning(
            logs.no_user_in_auth_from_other_parts_log,
            user_id=user_id,
        )
