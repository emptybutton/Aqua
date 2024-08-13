from datetime import date
from typing import TypeVar, Literal, TypeAlias

from entrypoint.application.ports import clients, loggers
from shared.application.ports.transactions import Transaction


_TransactionT = TypeVar("_TransactionT", bound=Transaction)
_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth[_TransactionT])  # type: ignore[valid-type]
_AquaT = TypeVar("_AquaT", bound=clients.aqua.Aqua[_TransactionT])  # type: ignore[valid-type]


Output: TypeAlias = (
    clients.aqua.ReadDayOutput
    | Literal["not_working"]
    | Literal["invalid_jwt"]
    | Literal["expired_access_token"]
    | Literal["no_user"]
)


async def perform(
    jwt: str,
    date_: date,
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

    aqua_result = await aqua.read_day(
        auth_result.user_id,
        date_,
        transaction=transaction,
    )

    if aqua_result == "aqua_is_not_working":
        await aqua_logger.log_aqua_is_not_working(aqua)
        return "not_working"
    if not isinstance(aqua_result, clients.aqua.ReadDayOutput):
        return aqua_result

    return aqua_result
