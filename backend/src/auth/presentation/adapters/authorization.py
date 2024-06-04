from dataclasses import dataclass
from datetime import datetime
from secrets import token_hex

from sqlalchemy.ext.asyncio import AsyncConnection

from src.auth.application import authorization
from src.auth.infrastructure.adapters import serializers, repos
from src.auth.presentation import secrets


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    user_id: int
    username: str
    refresh_token_text: str
    refresh_token_expiration_date: datetime
    serialized_access_token: str


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
        refresh_token_text=result.refresh_token.text,
        refresh_token_expiration_date=result.refresh_token.expiration_date,
        serialized_access_token=result.serialized_access_token,
    )
