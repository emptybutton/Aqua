from typing import Literal, TypeAlias, TypeVar

from entrypoint.application.ports import clients, loggers
from shared.application.ports.transactions import Transaction


_TransactionT = TypeVar("_TransactionT", bound=Transaction)
_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth[_TransactionT])  # type: ignore[valid-type]


Output: TypeAlias = bool | Literal["error"]


async def perform(
    username: str,
    *,
    transaction: _TransactionT,
    auth: _AuthT,
    auth_logger: loggers.AuthLogger[_AuthT],
) -> Output:
    result = await auth.user_exists(username, transaction=transaction)

    if result == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)
        return "error"

    return result
