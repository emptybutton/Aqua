from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.cases import register_user
from auth.domain import value_objects as vos
from auth.infrastructure.adapters import serializers, repos, generators
from auth.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransactionFactory


@dataclass(kw_only=True, frozen=True)
class Output:
    user_id: UUID
    username: str
    refresh_token_text: str
    refresh_token_expiration_date: datetime
    jwt: str


UserIsAlreadyRegisteredError: TypeAlias = (
    register_user.UserIsAlreadyRegisteredError
)

EmptyUsernameError: TypeAlias = vos.Username.EmptyError

WeekPasswordError: TypeAlias = vos.Password.WeekError

Error: TypeAlias = (
    register_user.Error
    | EmptyUsernameError
    | WeekPasswordError
)


async def perform(
    username: str,
    password: str,
    *,
    session: AsyncSession,
) -> Output:
    async with async_container(context={AsyncSession: session}) as container:
        result = await register_user.perform(
            username,
            password,
            users=await container.get(repos.DBUsers),
            password_serializer=(
                await container.get(serializers.PasswordSerializer)
            ),
            access_token_serializer=(
                await container.get(serializers.AccessTokenSerializer)
            ),
            generate_high_entropy_text=(
                await container.get(generators.GenerateByTokenHex)
            ),
            transaction_for=await container.get(DBTransactionFactory),
        )

    return Output(
        user_id=result.user.id,
        username=result.user.name.text,
        refresh_token_text=result.refresh_token.text,
        refresh_token_expiration_date=result.refresh_token.expiration_date,
        jwt=result.serialized_access_token,
    )
