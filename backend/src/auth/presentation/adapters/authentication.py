from typing import TypeAlias

from src.auth.application import authentication
from src.auth.infrastructure.adapters import serializers
from src.auth.presentation import secrets


BaseError: TypeAlias = authentication.BaseError

InvalidJWTError: TypeAlias = authentication.NoAccessTokenError

ExpiredAccessTokenError: TypeAlias = authentication.ExpiredAccessTokenError


def authenticate_user(jwt: str) -> None:
    serializer = serializers.AccessTokenSerializer(secrets.jwt_secret)

    authentication.authenticate_user(
        jwt,
        access_token_serializer=serializer,
    )
