from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from auth.application import ports
from auth.application.cases import authenticate_user
from auth.domain import entities
from auth.infrastructure.adapters import repos
from auth.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransactionFactory


@dataclass(kw_only=True, frozen=True)
class Output:
    user_id: UUID
    session_id: UUID


NoSessionError: TypeAlias = authenticate_user.NoSessionError

ExpiredSessionError: TypeAlias = (
    entities.Session.ExpiredLifetimeForAuthenticationError
)

Error: TypeAlias = (
    authenticate_user.Error | NoSessionError | ExpiredSessionError
)


async def perform(session_id: UUID, *, session: AsyncSession) -> Output:
    async with async_container(context={AsyncSession: session}) as container:
        result = await authenticate_user.perform(
            session_id,
            sessions=await container.get(repos.DBSessions, "repos"),
            transaction_for=await container.get(
                DBTransactionFactory, "transactions"
            ),
            logger=await container.get(ports.loggers.Logger, "loggers"),
        )

    return Output(user_id=result.user_id, session_id=result.id)
