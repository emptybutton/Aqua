from typing import Literal

from entrypoint.infrastructure.facades.clients import auth
from entrypoint.infrastructure.facades.loggers import auth_logger


type Output = bool | Literal["error"]


async def user_exists(username: str) -> Output:
    result = await auth.user_exists(username)

    if isinstance(result, auth.AuthError):
        await auth_logger.log_error(result)
        return "error"

    return result
