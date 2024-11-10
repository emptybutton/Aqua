from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from entrypoint.infrastructure.facades.clients import aqua, auth
from entrypoint.infrastructure.facades.loggers import aqua_logger, auth_logger


@dataclass(kw_only=True, frozen=True)
class OutputData:
    authentication_output: auth.AuthenticateUserOutputData
    aqua_output: aqua.ReadUserOutputData | None
    auth_output: auth.ReadUserOutputData | None


type Output = OutputData | Literal["error"] | Literal["not_authenticated"]


async def read_user(session_id: UUID) -> Output:
    async with auth.authenticate_user(session_id) as authenticate_result:
        ...

    if isinstance(authenticate_result, auth.AuthError):
        await auth_logger.log_auth_is_not_working(auth)
        return "error"
    if not isinstance(authenticate_result, auth.AuthenticateUserOutput):
        return "not_authenticated"

    user_id = authenticate_result.user_id

    aqua_result = await aqua.read_user(user_id)
    if isinstance(aqua_result, aqua.AquaError):
        await aqua_logger.log_error(aqua_result)

    auth_result = await auth.read_user(user_id)
    if isinstance(auth_result, auth.AuthError):
        await auth_logger.log_error(auth_result)

    aqua_has_no_user = aqua_result == "no_user"
    auth_has_no_user = auth_result == "no_user"

    if not auth_has_no_user and aqua_has_no_user:
        await aqua_logger.log_no_user_from_other_parts(user_id)

    if auth_has_no_user and not aqua_has_no_user:
        await auth_logger.log_no_user_from_other_parts(user_id)

    output_auth_result: auth.ReadUserOutput | None = None
    output_aqua_result: aqua.ReadUserOutput | None = None

    if isinstance(auth_result, auth.ReadUserOutput):
        output_auth_result = auth_result

    if isinstance(aqua_result, aqua.ReadUserOutput):
        output_aqua_result = aqua_result

    return OutputData(
        authenticate_user_output=authenticate_result,
        read_auth_user_output=output_auth_result,
        read_aqua_user_output=output_aqua_result,
    )
