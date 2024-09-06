from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from auth.application import ports
from auth.application.cases import change_password
from auth.domain import value_objects as vos
from auth.infrastructure.adapters import repos, serializers
from auth.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransactionFactory


@dataclass(kw_only=True, frozen=True)
class Output:
    session_id: UUID
    user_id: UUID
    username: str


NoUserError: TypeAlias = change_password.NoUserError

WeekPasswordError: TypeAlias = vos.Password.WeekError

Error: TypeAlias = change_password.Error | WeekPasswordError


async def perform(
    session_id: UUID,
    user_id: UUID,
    new_password: str,
    *,
    session: AsyncSession,
) -> Output:
    async with async_container(context={AsyncSession: session}) as container:
        result = await change_password.perform(
            user_id,
            new_password,
            session_id,
            users=await container.get(repos.DBUsers, "repos"),
            sessions=await container.get(repos.DBSessions, "repos"),
            user_transaction_for=await container.get(
                DBTransactionFactory, "transactions"
            ),
            session_transaction_for=await container.get(
                DBTransactionFactory, "transactions"
            ),
            password_serializer=await container.get(
                serializers.SHA256PasswordHasher, "serializers"
            ),
            logger=await container.get(ports.loggers.Logger, "loggers"),
        )

    return Output(
        user_id=result.user.id,
        username=result.user.name.text,
        session_id=session_id,
    )
