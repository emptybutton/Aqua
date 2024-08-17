from typing import TypeVar
from uuid import UUID

from auth.domain import entities
from auth.application import ports
from shared.application.ports.transactions import TransactionFactory


class Error(Exception): ...


class NoSessionError(Error): ...


_SessionsT = TypeVar("_SessionsT", bound=ports.repos.Sessions)


async def perform(
    session_id: UUID,
    *,
    sessions: _SessionsT,
    transaction_for: TransactionFactory[_SessionsT],
) -> entities.Session:
    async with transaction_for(sessions):
        session = await sessions.find_with_id(session_id)

        if session is None:
            raise NoSessionError

        session.authenticate()
        await sessions.update(session)

        return session
