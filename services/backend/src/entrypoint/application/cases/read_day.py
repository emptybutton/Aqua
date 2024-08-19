from dataclasses import dataclass
from datetime import date
from typing import TypeVar, Literal, TypeAlias
from uuid import UUID

from entrypoint.application.ports import clients, loggers
from shared.application.ports.transactions import Transaction


_TransactionT = TypeVar("_TransactionT", bound=Transaction)
_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth[_TransactionT])  # type: ignore[valid-type]
_AquaT = TypeVar("_AquaT", bound=clients.aqua.Aqua[_TransactionT])  # type: ignore[valid-type]


@dataclass(kw_only=True, frozen=True)
class OutputData:
    auth_result: clients.auth.AuthenticateUserOutput
    aqua_result: clients.aqua.ReadDayOutput | None


Output: TypeAlias = (
    OutputData
    | Literal["not_working"]
    | Literal["not_authenticated"]
)


async def perform(
    session_id: UUID,
    date_: date,
    *,
    transaction: _TransactionT,
    auth: _AuthT,
    aqua: _AquaT,
    auth_logger: loggers.AuthLogger[_AuthT],
    aqua_logger: loggers.AquaLogger[_AquaT],
) -> Output:
    auth_result = await auth.authenticate_user(
        session_id,
        transaction=transaction,
    )

    if auth_result == "auth_is_not_working":
        await auth_logger.log_auth_is_not_working(auth)
        return "not_working"
    if not isinstance(auth_result, clients.auth.AuthenticateUserOutput):
        return "not_authenticated"

    aqua_result = await aqua.read_day(
        auth_result.user_id,
        date_,
        transaction=transaction,
    )

    if aqua_result == "aqua_is_not_working":
        await aqua_logger.log_aqua_is_not_working(aqua)

    if aqua_result == "no_user":
        await aqua_logger.log_no_user_from_other_parts(
            aqua,
            auth_result.user_id,
        )

    output_aqua_result: clients.aqua.ReadDayOutput | None = None

    if isinstance(aqua_result, clients.aqua.ReadDayOutput):
        output_aqua_result = aqua_result

    return OutputData(
        auth_result=auth_result,
        aqua_result=output_aqua_result,
    )
