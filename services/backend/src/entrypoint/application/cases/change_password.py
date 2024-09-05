from dataclasses import dataclass
from typing import Literal, TypeAlias, TypeVar
from uuid import UUID

from entrypoint.application.ports import clients, loggers
from shared.application.ports.transactions import Transaction


_ChangingOutput: TypeAlias = (
    clients.auth.ChangePasswordOutput
    | Literal["error"]
    | Literal["week_password"]
)


@dataclass(kw_only=True, frozen=True)
class OutputData:
    authentication_output: clients.auth.AuthenticateUserOutput
    changing_output: _ChangingOutput


Output: TypeAlias = OutputData | Literal["error"] | Literal["not_authenticated"]


_TransactionT = TypeVar("_TransactionT", bound=Transaction)
_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth[_TransactionT])  # type: ignore[valid-type]


async def perform(
    session_id: UUID,
    new_password: str,
    *,
    transaction: _TransactionT,
    auth: _AuthT,
    auth_logger: loggers.AuthLogger[_AuthT],
) -> Output:
    authentication_result = await auth.authenticate_user(
        session_id, transaction=transaction
    )

    if authentication_result == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)
        return "error"
    if not isinstance(
        authentication_result, clients.auth.AuthenticateUserOutput
    ):
        return "not_authenticated"

    changing_result = await auth.change_password(
        session_id,
        authentication_result.user_id,
        new_password,
        transaction=transaction,
    )

    changing_output: _ChangingOutput = "error"

    if changing_result == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)
    elif changing_result == "no_user":
        await auth_logger.log_user_without_session(
            auth, authentication_result.user_id, session_id
        )
    else:
        changing_output = changing_result

    return OutputData(
        authentication_output=authentication_result,
        changing_output=changing_output,
    )
