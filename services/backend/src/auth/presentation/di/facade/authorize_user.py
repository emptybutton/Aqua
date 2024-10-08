from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from auth.application import ports
from auth.application.cases import authorize_user
from auth.infrastructure.adapters import repos, serializers
from auth.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransactionFactory


@dataclass(kw_only=True, frozen=True)
class Output:
    user_id: UUID
    username: str
    session_id: UUID


Error: TypeAlias = authorize_user.Error

NoUserError: TypeAlias = authorize_user.NoUserError

IncorrectPasswordError: TypeAlias = authorize_user.IncorrectPasswordError


async def perform(
    session_id: UUID | None,
    name: str,
    password: str,
    *,
    session: AsyncSession,
) -> Output:
    async with async_container(context={AsyncSession: session}) as container:
        result = await authorize_user.perform(
            session_id,
            name,
            password,
            password_serializer=await container.get(
                serializers.SHA256PasswordHasher, "serializers"
            ),
            users=await container.get(repos.DBUsers, "repos"),
            sessions=await container.get(repos.DBSessions, "repos"),
            user_transaction_for=await container.get(
                DBTransactionFactory, "transactions"
            ),
            session_transaction_for=await container.get(
                DBTransactionFactory, "transactions"
            ),
            logger=await container.get(ports.loggers.Logger, "loggers"),
        )

    return Output(
        user_id=result.user.id,
        username=result.user.name.text,
        session_id=result.session.id,
    )
