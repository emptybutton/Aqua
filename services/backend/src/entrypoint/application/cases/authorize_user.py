from typing import Literal, TypeAlias, TypeVar
from uuid import UUID

from entrypoint.application.ports import clients, loggers


_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth)


Output: TypeAlias = (
    clients.auth.AuthorizeUserOutput
    | Literal["not_working"]
    | Literal["no_user"]
    | Literal["incorrect_password"]
)


async def perform(
    session_id: UUID | None,
    name: str,
    password: str,
    *,
    auth: _AuthT,
    auth_logger: loggers.AuthLogger[_AuthT],
) -> Output:
    auth_result = await auth.authorize_user(session_id, name, password)

    if auth_result == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)
        return "not_working"

    return auth_result
