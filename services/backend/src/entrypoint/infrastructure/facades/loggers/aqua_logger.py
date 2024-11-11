from uuid import UUID

from entrypoint.infrastructure.facades.clients.aqua import Error as AquaError
from entrypoint.infrastructure.periphery import logs
from entrypoint.infrastructure.periphery.structlog import get_logger


async def log_error(error: AquaError) -> None:
    await get_logger().aerror(
        logs.aqua_is_not_working_log, exc_info=error.unexpected_error
    )


async def log_no_user_from_other_parts(user_id: UUID) -> None:
    await get_logger().awarning(
        logs.no_user_in_aqua_from_other_parts_log, user_id=user_id
    )
