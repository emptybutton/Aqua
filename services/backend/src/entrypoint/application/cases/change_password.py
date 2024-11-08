from dataclasses import dataclass
from typing import Literal, TypeAlias, TypeVar
from uuid import UUID

from entrypoint.application.ports import clients, loggers


_ChangingOutput: TypeAlias = (
    clients.auth.ChangePasswordOutput
    | Literal["error"]
    | Literal["week_password"]
)


@dataclass(kw_only=True, frozen=True)
class OutputData:
    authentication_output: clients.auth.AuthenticateUserOutput
    changing_output: _ChangingOutput


Output: TypeAlias = OutputData | Literal["error"] | Literal["not_authenticated"]


_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth)


async def perform(
    session_id: UUID,
    new_password: str,
    *,
    auth: _AuthT,
    auth_logger: loggers.AuthLogger[_AuthT],
) -> Output:
    async with auth.authenticate_user(session_id) as authentication_result:
        ...

    if authentication_result == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)
        return "error"
    if not isinstance(
        authentication_result, clients.auth.AuthenticateUserOutput
    ):
        return "not_authenticated"

    change_password = auth.change_password(
        session_id, authentication_result.user_id, new_password
    )
    async with change_password as changing_result:
        changing_output: _ChangingOutput = "error"

        if changing_result == "auth_is_not_working":
            await auth_logger.log_auth_is_not_working(auth)
        elif changing_result == "no_user":
            await auth_logger.log_user_without_session(
                auth, authentication_result.user_id, session_id
            )
        else:
            changing_output = changing_result

        return OutputData(
            authentication_output=authentication_result,
            changing_output=changing_output,
        )
