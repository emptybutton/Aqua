from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from entrypoint.infrastructure.facades.clients import aqua, auth
from entrypoint.infrastructure.facades.loggers import aqua_logger, auth_logger


type AquaOutput = (
    aqua.WriteWaterOutputData
    | Literal["error"]
    | Literal["incorrect_water_amount"]
)


@dataclass(kw_only=True, frozen=True)
class OutputData:
    auth_output: auth.AuthenticateUserOutputData
    aqua_output: AquaOutput


type Output = OutputData | Literal["error"] | Literal["not_authenticated"]


async def write_water(session_id: UUID, milliliters: int | None) -> Output:
    async with auth.authenticate_user(session_id) as auth_result:
        ...

    if isinstance(auth_result, auth.Error):
        await auth_logger.log_error(auth_result)
        return "error"
    if not isinstance(auth_result, auth.AuthenticateUserOutputData):
        return "not_authenticated"

    user_id = auth_result.user_id

    async with aqua.write_water(user_id, milliliters) as aqua_result:
        if isinstance(aqua_result, aqua.Error):
            await aqua_logger.log_error(aqua_result)
        if aqua_result == "no_user":
            await aqua_logger.log_no_user_from_other_parts(user_id)

        aqua_output: AquaOutput

        if (
            isinstance(aqua_result, aqua.WriteWaterOutputData)
            or aqua_result == "incorrect_water_amount"
        ):
            aqua_output = aqua_result
        else:
            aqua_output = "error"

        return OutputData(auth_output=auth_result, aqua_output=aqua_output)
