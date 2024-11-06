from dataclasses import dataclass
from typing import Literal, TypeAlias, TypeVar
from uuid import UUID

from entrypoint.application.ports import clients, loggers


_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth)
_AquaT = TypeVar("_AquaT", bound=clients.aqua.Aqua)


AquaOutput: TypeAlias = (
    clients.aqua.CancelRecordOutput | Literal["error"] | Literal["no_record"]
)


@dataclass(kw_only=True, frozen=True)
class OutputData:
    auth_output: clients.auth.AuthenticateUserOutput
    aqua_output: AquaOutput


Output: TypeAlias = OutputData | Literal["error"] | Literal["not_authenticated"]


async def perform(
    session_id: UUID,
    record_id: UUID,
    *,
    auth: _AuthT,
    aqua: _AquaT,
    auth_logger: loggers.AuthLogger[_AuthT],
    aqua_logger: loggers.AquaLogger[_AquaT],
) -> Output:
    auth_output = await auth.authenticate_user(session_id)

    if auth_output == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)
        return "error"
    if not isinstance(auth_output, clients.auth.AuthenticateUserOutput):
        return "not_authenticated"

    aqua_result = await aqua.cancel_record(auth_output.user_id, record_id)

    aqua_output: AquaOutput

    if aqua_result == "aqua_is_not_working":
        await aqua_logger.log_aqua_is_not_working(aqua)
        aqua_output = "error"
    else:
        aqua_output = aqua_result

    return OutputData(auth_output=auth_output, aqua_output=aqua_output)
