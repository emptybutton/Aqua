from dataclasses import dataclass
from typing import Literal, TypeAlias, TypeVar
from uuid import UUID

from entrypoint.application.ports import clients, loggers


_RenamingOutput: TypeAlias = (
    clients.auth.RenameUserOutput
    | Literal["error"]
    | Literal["new_username_taken"]
    | Literal["empty_new_username"]
)


@dataclass(kw_only=True, frozen=True)
class OutputData:
    authentication_output: clients.auth.AuthenticateUserOutput
    renaming_output: _RenamingOutput


Output: TypeAlias = OutputData | Literal["error"] | Literal["not_authenticated"]


_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth)


async def perform(
    session_id: UUID,
    new_username: str,
    *,
    auth: _AuthT,
    auth_logger: loggers.AuthLogger[_AuthT],
) -> Output:
    authentication_result = await auth.authenticate_user(session_id)

    if authentication_result == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)
        return "error"
    if not isinstance(
        authentication_result, clients.auth.AuthenticateUserOutput
    ):
        return "not_authenticated"

    renaming_result = await auth.rename_user(
        authentication_result.user_id, new_username
    )

    renaming_output: _RenamingOutput = "error"

    if renaming_result == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)
    elif renaming_result == "no_user":
        await auth_logger.log_user_without_session(
            auth, authentication_result.user_id, session_id
        )
    else:
        renaming_output = renaming_result

    return OutputData(
        authentication_output=authentication_result,
        renaming_output=renaming_output,
    )
