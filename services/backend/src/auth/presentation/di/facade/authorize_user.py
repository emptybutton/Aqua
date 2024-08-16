from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.cases import authorize_user
from auth.infrastructure.adapters import serializers, repos, generators
from auth.presentation.di.containers import async_container


@dataclass(kw_only=True, frozen=True)
class Output:
    user_id: UUID
    username: str
    refresh_token: str
    refresh_token_expiration_date: datetime
    jwt: str


Error: TypeAlias = authorize_user.Error

NoUserError: TypeAlias = authorize_user.NoUserError

IncorrectPasswordError: TypeAlias = authorize_user.IncorrectPasswordError


async def perform(
    name: str,
    password: str,
    *,
    session: AsyncSession,
) -> Output:
    async with async_container(context={AsyncSession: session}) as container:
        result = await authorize_user.perform(
            name,
            password,
            users=await container.get(repos.DBUsers, "repos"),
            password_serializer=await container.get(
                serializers.PasswordSerializer, "serializers"
            ),
            access_token_serializer=await container.get(
                serializers.AccessTokenSerializer, "serializers"
            ),
            generate_refresh_token_text=await container.get(
                generators.GenerateByTokenHex, "generators"
            ),
        )

    return Output(
        user_id=result.user.id,
        username=result.user.name.text,
        refresh_token=result.refresh_token.text,
        refresh_token_expiration_date=result.refresh_token.expiration_date,
        jwt=result.serialized_access_token,
    )
