from dataclasses import dataclass
from datetime import datetime
from typing import TypeVar, TypeAlias, Literal
from uuid import UUID

from entrypoint.application.ports import clients, loggers
from shared.application.ports.transactions import Transaction


@dataclass(kw_only=True, frozen=True)
class OutputData:
    user_id: UUID
    username: str
    access_token: str
    refresh_token: str
    refresh_token_expiration_date: datetime
    water_balance_milliliters: int
    glass_milliliters: int


Output: TypeAlias = (
    OutputData
    | Literal["not_working"]
    | Literal["incorrect_water_amount"]
    | Literal["incorrect_weight_amount"]
    | Literal["no_weight_for_water_balance"]
    | Literal["extreme_weight_for_water_balance"]
    | Literal["user_is_already_registered"]
    | Literal["empty_username"]
    | Literal["week_password"]
)


_TransactionT = TypeVar("_TransactionT", bound=Transaction)
_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth[_TransactionT])  # type: ignore[valid-type]
_AquaT = TypeVar("_AquaT", bound=clients.aqua.Aqua[_TransactionT])  # type: ignore[valid-type]


async def perform(
    name: str,
    password: str,
    water_balance_milliliters: int | None,
    glass_milliliters: int | None,
    weight_kilograms: int | None,
    *,
    transaction: _TransactionT,
    auth: _AuthT,
    aqua: _AquaT,
    auth_logger: loggers.AuthLogger[_AuthT],
    aqua_logger: loggers.AquaLogger[_AquaT],
) -> Output:
    async with transaction:
        auth_result = await auth.register_user(
            name,
            password,
            transaction=transaction,
        )

        if not isinstance(auth_result, clients.auth.RegisterUserOutput):
            await transaction.rollback()
            if auth_result == "auth_is_not_working":
                await auth_logger.log_auth_is_not_working(auth)
                return "not_working"
            return auth_result

        aqua_result = await aqua.register_user(
            auth_result.user_id,
            water_balance_milliliters,
            glass_milliliters,
            weight_kilograms,
            transaction=transaction,
        )

        if not isinstance(aqua_result, clients.aqua.RegisterUserOutput):
            await transaction.rollback()
            if aqua_result == "aqua_is_not_working":
                await aqua_logger.log_aqua_is_not_working(aqua)
                return "not_working"
            return aqua_result

        refresh_token_expiration = auth_result.refresh_token_expiration_date
        return OutputData(
            user_id=auth_result.user_id,
            username=auth_result.username,
            access_token=auth_result.access_token,
            refresh_token=auth_result.refresh_token,
            refresh_token_expiration_date=refresh_token_expiration,
            water_balance_milliliters=aqua_result.water_balance_milliliters,
            glass_milliliters=aqua_result.glass_milliliters,
        )
