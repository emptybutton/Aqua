from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from auth.application import ports
from auth.application.cases import register_user
from auth.domain import value_objects as vos
from auth.infrastructure.adapters import repos, serializers
from auth.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransactionFactory


@dataclass(kw_only=True, frozen=True)
class Output:
    user_id: UUID
    username: str
    session_id: UUID


UserIsAlreadyRegisteredError: TypeAlias = (
    register_user.UserIsAlreadyRegisteredError
)

EmptyUsernameError: TypeAlias = vos.Username.EmptyError

WeekPasswordError: TypeAlias = vos.Password.WeekError

Error: TypeAlias = register_user.Error | EmptyUsernameError | WeekPasswordError


async def perform(
    username: str, password: str, *, session: AsyncSession
) -> Output:
    async with async_container(context={AsyncSession: session}) as container:
        result = await register_user.perform(
            username,
            password,
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
        session_id=result.session.id,
    )
