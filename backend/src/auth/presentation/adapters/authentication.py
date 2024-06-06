from datetime import datetime
from typing import TypeAlias

from src.auth.application import authentication
from src.auth.infrastructure.adapters import serializers
from src.auth.presentation import secrets


BaseError: TypeAlias = authentication.BaseError

NoAccessTokenError: TypeAlias = authentication.NoAccessTokenError

ExpiredRefreshTokenError: TypeAlias = authentication.ExpiredRefreshTokenError


def authenticate_user(
    serialized_access_token: str,
    refresh_token_text: str,
    refresh_token_expiration_date: datetime,
) -> None:
    serializer = serializers.AccessTokenSerializer(secrets.jwt_secret)

    authentication.authenticate_user(
        serialized_access_token,
        refresh_token_text,
        refresh_token_expiration_date,
        access_token_serializer=serializer,
    )
