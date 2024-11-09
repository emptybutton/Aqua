from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from entrypoint.infrastructure.facades.clients import aqua, auth
from entrypoint.infrastructure.facades.loggers import aqua_logger, auth_logger


type AquaOutput = (
   aqua.CancelRecordOutputData | Literal["error"] | Literal["no_record"]
)


@dataclass(kw_only=True, frozen=True)
class OutputData:
    auth_output: auth.AuthenticateUserOutputData
    aqua_output: AquaOutput


type Output = OutputData | Literal["error"] | Literal["not_authenticated"]


async def cancel_record(session_id: UUID, record_id: UUID) -> Output:
    async with auth.authenticate_user(session_id) as auth_result:
        ...

    if isinstance(auth_result, auth.Error):
        await auth_logger.log_error(auth_result)
        return "error"
    if not isinstance(auth_result, auth.AuthenticateUserOutputData):
        return "not_authenticated"

    user_id = auth_result.user_id

    async with aqua.cancel_record(user_id, record_id) as aqua_result:
        aqua_output: AquaOutput

        if isinstance(aqua_result, aqua.Error):
            await aqua_logger.log_error(aqua_result)
            aqua_output = "error"
        else:
            aqua_output = aqua_result

        return OutputData(auth_output=auth_result, aqua_output=aqua_output)
