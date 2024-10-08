from dataclasses import dataclass
from typing import Literal, TypeAlias, TypeVar
from uuid import UUID

from entrypoint.application.ports import clients, loggers
from shared.application.ports.transactions import Transaction


AquaResult: TypeAlias = (
    clients.aqua.WriteWaterOutput
    | Literal["error"]
    | Literal["incorrect_water_amount"]
)


@dataclass(kw_only=True, frozen=True)
class OutputData:
    auth_result: clients.auth.AuthenticateUserOutput
    aqua_result: AquaResult


Output: TypeAlias = (
    OutputData | Literal["not_working"] | Literal["not_authenticated"]
)


_TransactionT = TypeVar("_TransactionT", bound=Transaction)
_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth[_TransactionT])  # type: ignore[valid-type]
_AquaT = TypeVar("_AquaT", bound=clients.aqua.Aqua[_TransactionT])  # type: ignore[valid-type]


async def perform(
    session_id: UUID,
    milliliters: int | None,
    *,
    transaction: _TransactionT,
    auth: _AuthT,
    aqua: _AquaT,
    auth_logger: loggers.AuthLogger[_AuthT],
    aqua_logger: loggers.AquaLogger[_AquaT],
) -> Output:
    auth_result = await auth.authenticate_user(
        session_id, transaction=transaction
    )

    if auth_result == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)
        return "not_working"
    if not isinstance(auth_result, clients.auth.AuthenticateUserOutput):
        return "not_authenticated"

    aqua_result = await aqua.write_water(
        auth_result.user_id, milliliters, transaction=transaction
    )

    if aqua_result == "aqua_is_not_working":
        await aqua_logger.log_aqua_is_not_working(aqua)
    if aqua_result == "no_user":
        await aqua_logger.log_no_user_from_other_parts(
            aqua, auth_result.user_id
        )

    output_aqua_result: AquaResult

    if (
        isinstance(aqua_result, clients.aqua.WriteWaterOutput)
        or aqua_result == "incorrect_water_amount"
    ):
        output_aqua_result = aqua_result
    else:
        output_aqua_result = "error"

    return OutputData(auth_result=auth_result, aqua_result=output_aqua_result)
