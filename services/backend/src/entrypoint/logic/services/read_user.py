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
    async with auth.authenticate_user(session_id) as authentication_result:
        ...

    if isinstance(authentication_result, auth.Error):
        await auth_logger.log_error(authentication_result)
        return "error"
    if not isinstance(authentication_result, auth.AuthenticateUserOutputData):
        return "not_authenticated"

    user_id = authentication_result.user_id

    aqua_result = await aqua.read_user(user_id)
    if isinstance(aqua_result, aqua.Error):
        await aqua_logger.log_error(aqua_result)

    auth_result = await auth.read_user(user_id)
    if isinstance(auth_result, auth.Error):
        await auth_logger.log_error(auth_result)

    aqua_has_no_user = aqua_result == "no_user"
    auth_has_no_user = auth_result == "no_user"

    if not auth_has_no_user and aqua_has_no_user:
        await aqua_logger.log_no_user_from_other_parts(user_id)

    if auth_has_no_user and not aqua_has_no_user:
        await auth_logger.log_no_user_from_other_parts(user_id)

    auth_output: auth.ReadUserOutputData | None = None
    aqua_output: aqua.ReadUserOutputData | None = None

    if isinstance(auth_result, auth.ReadUserOutputData):
        auth_output = auth_result

    if isinstance(aqua_result, aqua.ReadUserOutputData):
        aqua_output = aqua_result

    return OutputData(
        authentication_output=authentication_result,
        auth_output=auth_output,
        aqua_output=aqua_output,
    )
