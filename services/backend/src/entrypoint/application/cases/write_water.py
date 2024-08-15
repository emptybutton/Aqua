from dataclasses import dataclass
from datetime import datetime
from typing import TypeVar, TypeAlias, Literal
from uuid import UUID

from entrypoint.application.ports import clients, loggers
from shared.application.ports.transactions import Transaction


@dataclass(kw_only=True, frozen=True)
class OutputData:
    user_id: UUID
    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime
    target_water_balance_milliliters: int
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool


Output: TypeAlias = (
    OutputData
    | Literal["not_working"]
    | Literal["invalid_jwt"]
    | Literal["expired_jwt"]
    | Literal["no_user"]
    | Literal["incorrect_water_amount"]
)


_TransactionT = TypeVar("_TransactionT", bound=Transaction)
_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth[_TransactionT])  # type: ignore[valid-type]
_AquaT = TypeVar("_AquaT", bound=clients.aqua.Aqua[_TransactionT])  # type: ignore[valid-type]


async def perform(
    jwt: str,
    milliliters: int | None,
    *,
    transaction: _TransactionT,
    auth: _AuthT,
    aqua: _AquaT,
    auth_logger: loggers.AuthLogger[_AuthT],
    aqua_logger: loggers.AquaLogger[_AquaT],
) -> Output:
    auth_result = await auth.authenticate_user(jwt)

    if auth_result == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)
        return "not_working"
    if not isinstance(auth_result, clients.auth.AuthenticateUserOutput):
        return auth_result

    aqua_result = await aqua.write_water(
        auth_result.user_id,
        milliliters,
        transaction=transaction,
    )

    if aqua_result == "aqua_is_not_working":
        await aqua_logger.log_aqua_is_not_working(aqua)
        return "not_working"
    if not isinstance(aqua_result, clients.aqua.WriteWaterOutput):
        return aqua_result

    target = aqua_result.target_water_balance_milliliters
    return OutputData(
        user_id=aqua_result.user_id,
        record_id=aqua_result.record_id,
        drunk_water_milliliters=aqua_result.drunk_water_milliliters,
        recording_time=aqua_result.recording_time,
        target_water_balance_milliliters=target,
        water_balance_milliliters=aqua_result.water_balance_milliliters,
        result_code=aqua_result.result_code,
        real_result_code=aqua_result.real_result_code,
        is_result_pinned=aqua_result.is_result_pinned,
    )
