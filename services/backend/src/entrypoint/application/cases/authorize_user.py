from typing import TypeVar, Literal, TypeAlias

from entrypoint.application.ports import clients, loggers
from shared.application.ports.transactions import Transaction


_TransactionT = TypeVar("_TransactionT", bound=Transaction)
_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth[_TransactionT])  # type: ignore[valid-type]


Output: TypeAlias = (
    clients.auth.AuthorizeUserOutput
    | Literal["not_working"]
    | Literal["no_user"]
    | Literal["incorrect_password"]
)


async def perform(
    name: str,
    password: str,
    *,
    transaction: _TransactionT,
    auth: _AuthT,
    auth_logger: loggers.AuthLogger[_AuthT],
) -> Output:
    auth_result = await auth.authorize_user(
        name,
        password,
        transaction=transaction,
    )

    if auth_result == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)
        return "not_working"

    return auth_result
