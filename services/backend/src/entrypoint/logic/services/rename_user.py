from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from entrypoint.infrastructure.facades.clients import auth
from entrypoint.infrastructure.facades.loggers import auth_logger


type AuthOutput = (
    auth.RenameUserOutputData
    | Literal["error"]
    | Literal["new_username_taken"]
    | Literal["empty_new_username"]
)


@dataclass(kw_only=True, frozen=True)
class OutputData:
    authentication_output: auth.AuthenticateUserOutputData
    auth_output: AuthOutput


type Output = OutputData | Literal["error"] | Literal["not_authenticated"]


async def rename_user(session_id: UUID, new_username: str) -> Output:
    async with auth.authenticate_user(session_id) as authentication_result:
        ...

    if isinstance(authentication_result, auth.Error):
        await auth_logger.log_error(authentication_result)
        return "error"
    if not isinstance(authentication_result, auth.AuthenticateUserOutputData):
        return "not_authenticated"

    user_id = authentication_result.user_id

    async with auth.rename_user(user_id, new_username) as auth_result:
        auth_output: AuthOutput = "error"

        if isinstance(auth_result, auth.Error):
            await auth_logger.log_error(auth_result)
        elif auth_result == "no_user":
            await auth_logger.log_user_without_session(user_id, session_id)
        else:
            auth_output = auth_result

        return OutputData(
            authentication_output=authentication_result,
            auth_output=auth_output,
        )
