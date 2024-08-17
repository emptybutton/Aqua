from dataclasses import dataclass
from typing import TypeVar, TypeAlias, Literal
from uuid import UUID

from entrypoint.application.ports import clients, loggers
from shared.application.ports.transactions import Transaction


@dataclass(kw_only=True, frozen=True)
class OutputData:
    authenticate_user_result: clients.auth.AuthenticateUserOutput
    read_aqua_user_result: clients.aqua.ReadUserOutput | None
    read_auth_user_result: clients.auth.ReadUserOutput | None


Output: TypeAlias = (
    OutputData
    | Literal["not_working"]
    | Literal["not_authenticated"]
)


_TransactionT = TypeVar("_TransactionT", bound=Transaction)
_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth[_TransactionT])  # type: ignore[valid-type]
_AquaT = TypeVar("_AquaT", bound=clients.aqua.Aqua[_TransactionT])  # type: ignore[valid-type]


async def perform(
    session_id: UUID,
    *,
    transaction: _TransactionT,
    auth: _AuthT,
    aqua: _AquaT,
    auth_logger: loggers.AuthLogger[_AuthT],
    aqua_logger: loggers.AquaLogger[_AquaT],
) -> Output:
    authenticate_result = await auth.authenticate_user(
        session_id,
        transaction=transaction,
    )

    if authenticate_result == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)
        return "not_working"
    if not isinstance(authenticate_result, clients.auth.AuthenticateUserOutput):
        return "not_authenticated"

    user_id = authenticate_result.user_id

    aqua_result = await aqua.read_user(
        user_id,
        transaction=transaction,
    )
    if aqua_result == "aqua_is_not_working":
        await aqua_logger.log_aqua_is_not_working(aqua)


    auth_result = await auth.read_user(
        user_id,
        transaction=transaction,
    )
    if auth_result == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)


    if auth_result != "no_user" and aqua_result == "no_user":
        await auth_logger.log_has_extra_user(auth, user_id)

    if auth_result == "no_user" and aqua_result != "no_user":
        await aqua_logger.log_has_extra_user(aqua, user_id)

    output_auth_result: clients.auth.ReadUserOutput | None = None
    output_aqua_result: clients.aqua.ReadUserOutput | None = None

    if isinstance(auth_result, clients.auth.ReadUserOutput):
        output_auth_result = auth_result

    if isinstance(aqua_result, clients.aqua.ReadUserOutput):
        output_aqua_result = aqua_result

    return OutputData(
        authenticate_user_result=authenticate_result,
        read_auth_user_result=output_auth_result,
        read_aqua_user_result=output_aqua_result,
    )
