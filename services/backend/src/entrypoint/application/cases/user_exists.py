from typing import Literal, TypeAlias, TypeVar

from entrypoint.application.ports import clients, loggers


_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth)


Output: TypeAlias = bool | Literal["error"]


async def perform(
    username: str,
    *,
    auth: _AuthT,
    auth_logger: loggers.AuthLogger[_AuthT],
) -> Output:
    result = await auth.user_exists(username)

    if result == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)
        return "error"

    return result
