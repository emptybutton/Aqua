from dataclasses import dataclass
from datetime import date
from typing import Literal
from uuid import UUID

from entrypoint.infrastructure.facades.clients import aqua, auth
from entrypoint.infrastructure.facades.loggers import aqua_logger, auth_logger


type AquaOutput = aqua.ReadDayOutputData | None


@dataclass(kw_only=True, frozen=True)
class OutputData:
    auth_output: auth.AuthenticateUserOutputData
    aqua_output: AquaOutput


type Output = OutputData | Literal["error"] | Literal["not_authenticated"]


async def read_day(session_id: UUID, date_: date) -> Output:
    async with auth.authenticate_user(session_id) as auth_result:
        ...

    if isinstance(auth_result, auth.Error):
        await auth_logger.log_error(auth_result)
        return "error"
    if not isinstance(auth_result, auth.AuthenticateUserOutputData):
        return "not_authenticated"

    aqua_result = await aqua.read_day(auth_result.user_id, date_)

    if isinstance(aqua_result, aqua.Error):
        await aqua_logger.log_error(aqua_result)

    if aqua_result == "no_user":
        await aqua_logger.log_no_user_from_other_parts(auth_result.user_id)

    aqua_output: AquaOutput = None

    if isinstance(aqua_result, aqua.ReadDayOutputData):
        aqua_output = aqua_result

    return OutputData(auth_output=auth_result, aqua_output=aqua_output)
