from dataclasses import dataclass
from datetime import datetime
from secrets import token_hex
from typing import TypeAlias

from sqlalchemy.ext.asyncio import AsyncConnection

from src.auth.application import registration
from src.auth.infrastructure.adapters import serializers, repos
from src.auth.presentation import secrets
from src.shared.infrastructure.adapters import uows


@dataclass(frozen=True)
class OutputDTO:
    user_id: int
    username: str
    refresh_token_text: str
    refresh_token_expiration_date: datetime
    serialized_access_token: str


BaseError: TypeAlias = registration.BaseError

UserIsAlreadyRegisteredError: TypeAlias = (
    registration.UserIsAlreadyRegisteredError
)


async def register_user(
    username: str,
    password: str,
    *,
    connection: AsyncConnection,
) -> OutputDTO:
    serializer = serializers.AccessTokenSerializer(secrets.jwt_secret)

    result = await registration.register_user(
        username,
        password,
        users=repos.Users(connection),
        uow_for=lambda _: uows.FakeUoW(),  # type: ignore[arg-type, return-value]
        access_token_serializer=serializer,
        password_serializer=serializers.PasswordSerializer(),
        generate_refresh_token_text=token_hex,
    )

    return OutputDTO(
        user_id=result.user.id,
        username=result.user.name.text,
        refresh_token_text=result.refresh_token.text,
        refresh_token_expiration_date=result.refresh_token.expiration_date,
        serialized_access_token=result.serialized_access_token,
    )