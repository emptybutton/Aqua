from datetime import datetime
from typing import TypeVar, Literal, TypeAlias

from entrypoint.application.ports import clients, loggers
from shared.application.ports.transactions import Transaction


_TransactionT = TypeVar("_TransactionT", bound=Transaction)
_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth[_TransactionT])  # type: ignore[valid-type]


Output: TypeAlias = (
    clients.auth.RefreshTokenOutput
    | Literal["not_working"]
    | Literal["invalid_jwt"]
    | Literal["not_utc_refresh_token_expiration_date"]
    | Literal["expired_refresh_token"]
)


async def perform(
    jwt: str,
    refresh_token: str,
    refresh_token_expiration_date: datetime,
    *,
    transaction: _TransactionT,
    auth: _AuthT,
    auth_logger: loggers.AuthLogger[_AuthT],
) -> Output:
    auth_result = await auth.refresh_token(
        jwt,
        refresh_token,
        refresh_token_expiration_date,
        transaction=transaction,
    )

    if auth_result == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)
        return "not_working"

    return auth_result
