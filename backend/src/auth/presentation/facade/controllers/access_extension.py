from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias

from src.auth.application.cases import access_extension
from src.auth.infrastructure.adapters import serializers
from src.auth.presentation import secrets


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    jwt: str


BaseError: TypeAlias = access_extension.BaseError

InvalidJWTError: TypeAlias = access_extension.NoAccessTokenError

ExpiredRefreshTokenError: TypeAlias = access_extension.ExpiredRefreshTokenError


def extend_access(
    jwt: str,
    refresh_token: str,
    refresh_token_expiration_date: datetime,
) -> OutputDTO:
    serializer = serializers.AccessTokenSerializer(secrets.jwt_secret)

    result = access_extension.extend_access(
        jwt,
        refresh_token,
        refresh_token_expiration_date,
        access_token_serializer=serializer
    )

    return OutputDTO(jwt=result.serialized_new_access_token)
