from datetime import UTC, datetime
from typing import TypeVar
from uuid import UUID

from auth.application import ports
from auth.domain import entities
from auth.domain import value_objects as vos
from shared.application.ports.transactions import TransactionFactory


class Error(Exception): ...


class NoSessionError(Error): ...


_SessionsT = TypeVar("_SessionsT", bound=ports.repos.Sessions)


async def perform(
    session_id: UUID,
    *,
    sessions: _SessionsT,
    transaction_for: TransactionFactory[_SessionsT],
    logger: ports.loggers.Logger,
) -> entities.Session:
    current_time = vos.Time(datetime_=datetime.now(UTC))

    async with transaction_for(sessions):
        session = await sessions.find_with_id(session_id)

        if session is None:
            raise NoSessionError

        extended_session = session.authenticate(current_time=current_time)
        await sessions.update(extended_session)
        await logger.log_session_extension(extended_session)

        return session
