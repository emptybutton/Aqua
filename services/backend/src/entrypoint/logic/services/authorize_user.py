from typing import Literal
from uuid import UUID

from entrypoint.application.facades.clients import auth
from entrypoint.application.facades.loggers import auth_logger


type Output = (
    auth.AuthorizeUserOutputData
    | Literal["error"]
    | Literal["no_user"]
    | Literal["incorrect_password"]
)


async def authorize_user(
    session_id: UUID | None, name: str, password: str
) -> Output:
    async with auth.authorize_user(session_id, name, password) as auth_result:
        ...

    if isinstance(auth_result, auth.Error):
        await auth_logger.log_error(auth_result)
        return "error"

    return auth_result
