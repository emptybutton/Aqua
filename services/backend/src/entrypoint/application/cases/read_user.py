from dataclasses import dataclass
from typing import TypeVar, TypeAlias, Literal
from uuid import UUID

from entrypoint.application.ports import clients, loggers
from shared.application.ports.transactions import Transaction


@dataclass(kw_only=True, frozen=True)
class OutputData:
    user_id: UUID
    username: str
    glass_milliliters: int
    target_water_balance_milliliters: int
    weight_kilograms: int | None


Output: TypeAlias = (
    OutputData
    | None
    | Literal["not_working"]
    | Literal["invalid_jwt"]
    | Literal["expired_access_token"]
)


_TransactionT = TypeVar("_TransactionT", bound=Transaction)
_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth[_TransactionT])  # type: ignore[valid-type]
_AquaT = TypeVar("_AquaT", bound=clients.aqua.Aqua[_TransactionT])  # type: ignore[valid-type]


async def perform(  # noqa: PLR0911, PLR0913
    jwt: str,
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

    async with transaction as nested_transaction:
        aqua_reading_result = await aqua.read_user(
            auth_result.user_id,
            transaction=nested_transaction,
        )

        if not isinstance(aqua_reading_result, clients.aqua.ReadUserOutput):
            await nested_transaction.rollback()
            if aqua_reading_result == "aqua_is_not_working":
                await aqua_logger.log_aqua_is_not_working(aqua)
                return "not_working"
            return aqua_reading_result

        auth_reading_result = await auth.read_user(
            auth_result.user_id,
            transaction=nested_transaction,
        )

        if not isinstance(auth_reading_result, clients.auth.ReadUserOutput):
            await nested_transaction.rollback()
            if auth_reading_result == "auth_is_not_working":
                await auth_logger.log_auth_is_not_working(auth)
                return "not_working"
            return auth_reading_result

        if auth_reading_result is None or aqua_reading_result is None:
            if auth_reading_result is None and aqua_reading_result is not None:
                await aqua_logger.log_has_extra_user(aqua, auth_result.user_id)
            if auth_reading_result is not None and aqua_reading_result is None:
                await auth_logger.log_has_extra_user(auth, auth_result.user_id)

            return None

        water_balance = aqua_reading_result.target_water_balance_milliliters

        return OutputData(
            user_id=auth_result.user_id,
            username=auth_reading_result.username,
            glass_milliliters=aqua_reading_result.glass_milliliters,
            target_water_balance_milliliters=water_balance,
            weight_kilograms=aqua_reading_result.weight_kilograms,
        )
