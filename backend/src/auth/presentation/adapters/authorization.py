from dataclasses import dataclass
from datetime import datetime
from secrets import token_hex
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncConnection

from src.auth.application import authorization
from src.auth.infrastructure.adapters import serializers, repos
from src.auth.presentation import secrets


BaseError: TypeAlias = authorization.BaseError

NoUserError: TypeAlias = authorization.NoUserError

IncorrectPasswordError: TypeAlias = authorization.IncorrectPasswordError


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    user_id: UUID
    username: str
    refresh_token: str
    refresh_token_expiration_date: datetime
    jwt: str


async def authorize_user(
    name: str,
    password: str,
    *,
    connection: AsyncConnection,
) -> OutputDTO:
    serializer = serializers.AccessTokenSerializer(secrets.jwt_secret)

    result = await authorization.authorize_user(
        name,
        password,
        users=repos.Users(connection),
        password_serializer=serializers.PasswordSerializer(),
        access_token_serializer=serializer,
        generate_refresh_token_text=token_hex,
    )

    return OutputDTO(
        user_id=result.user.id,
        username=result.user.name.text,
        refresh_token=result.refresh_token.text,
        refresh_token_expiration_date=result.refresh_token.expiration_date,
        jwt=result.serialized_access_token,
    )
