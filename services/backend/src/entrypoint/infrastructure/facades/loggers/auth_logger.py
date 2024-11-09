from uuid import UUID

from entrypoint.infrastructure.facades.clients.auth import Error as AuthError
from entrypoint.infrastructure.periphery import logs
from entrypoint.infrastructure.periphery.structlog import get_logger


async def log_error(error: AuthError) -> None:
    await get_logger().aerror(
        logs.auth_is_not_working_log, exc_info=error.unexpected_error
    )


async def log_no_user_from_other_parts(user_id: UUID) -> None:
    await get_logger().awarning(
        logs.no_user_in_auth_from_other_parts_log, user_id=user_id
    )


async def log_user_without_session(
    user_id: UUID, session_id: UUID
) -> None:
    await get_logger().awarning(
        logs.user_without_session_log,
        user_id=user_id,
        session_id=session_id,
    )
