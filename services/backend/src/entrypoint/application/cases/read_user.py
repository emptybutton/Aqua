from dataclasses import dataclass
from datetime import date, datetime
from typing import TypeVar, TypeAlias, Literal
from uuid import UUID

from entrypoint.application.ports import clients, loggers
from shared.application.ports.transactions import Transaction



@dataclass(kw_only=True, frozen=True)
class OutputData:
    @dataclass(kw_only=True, frozen=True)
    class AuthPart:
        username: str

    @dataclass(kw_only=True, frozen=True)
    class AquaPart:
        glass_milliliters: int
        weight_kilograms: int | None
        target_water_balance_milliliters: int
        date_: date
        water_balance_milliliters: int
        result_code: int
        real_result_code: int
        is_result_pinned: bool

        @dataclass(kw_only=True, frozen=True)
        class RecordData:
            record_id: UUID
            drunk_water_milliliters: int
            recording_time: datetime

        records: tuple[RecordData, ...]

    user_id: UUID
    auth_part: AuthPart | None = None
    aqua_part: AquaPart | None = None


Output: TypeAlias = (
    OutputData
    | None
    | Literal["not_working"]
    | Literal["invalid_jwt"]
    | Literal["expired_jwt"]
)


_TransactionT = TypeVar("_TransactionT", bound=Transaction)
_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth[_TransactionT])  # type: ignore[valid-type]
_AquaT = TypeVar("_AquaT", bound=clients.aqua.Aqua[_TransactionT])  # type: ignore[valid-type]


async def perform(
    jwt: str,
    *,
    transaction: _TransactionT,
    auth: _AuthT,
    aqua: _AquaT,
    auth_logger: loggers.AuthLogger[_AuthT],
    aqua_logger: loggers.AquaLogger[_AquaT],
) -> Output:
    first_auth_result = await auth.authenticate_user(jwt)

    if first_auth_result == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)
        return "not_working"
    if not isinstance(first_auth_result, clients.auth.AuthenticateUserOutput):
        return first_auth_result

    user_id = first_auth_result.user_id

    async with transaction as nested_transaction:
        aqua_result = await aqua.read_user(
            user_id,
            transaction=nested_transaction,
        )
        if aqua_result == "aqua_is_not_working":
            await aqua_logger.log_aqua_is_not_working(aqua)


        auth_result = await auth.read_user(
            user_id,
            transaction=nested_transaction,
        )
        if auth_result == "auth_is_not_working":
            await auth_logger.log_auth_is_not_working(auth)


        if auth_result != "no_user" and aqua_result == "no_user":
            await auth_logger.log_has_extra_user(auth, user_id)

        if auth_result == "no_user" and aqua_result != "no_user":
            await aqua_logger.log_has_extra_user(aqua, user_id)


        aqua_part: OutputData.AquaPart | None = None
        auth_part: OutputData.AuthPart | None = None

        if not isinstance(aqua_result, str):
            records = tuple(
                OutputData.AquaPart.RecordData(
                    record_id=record.record_id,
                    drunk_water_milliliters=record.drunk_water_milliliters,
                    recording_time=record.recording_time,
                )
                for record in aqua_result.records
            )
            target = aqua_result.target_water_balance_milliliters
            aqua_part = OutputData.AquaPart(
                records=records,
                glass_milliliters=aqua_result.glass_milliliters,
                weight_kilograms=aqua_result.weight_kilograms,
                target_water_balance_milliliters=target,
                date_=aqua_result.date_,
                water_balance_milliliters=aqua_result.water_balance_milliliters,
                result_code=aqua_result.result_code,
                real_result_code=aqua_result.real_result_code,
                is_result_pinned=aqua_result.is_result_pinned,
            )

        if not isinstance(auth_result, str):
            auth_part = OutputData.AuthPart(username=auth_result.username)

        return OutputData(
            user_id=user_id,
            aqua_part=aqua_part,
            auth_part=auth_part,
        )
