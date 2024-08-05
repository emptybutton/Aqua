from typing import TypeAlias

from auth.application.cases import authentication
from auth.infrastructure.adapters import serializers
from auth.presentation import secrets


OutputDTO: TypeAlias = authentication.OutputDTO

BaseError: TypeAlias = authentication.BaseError

InvalidJWTError: TypeAlias = authentication.NoAccessTokenError

ExpiredAccessTokenError: TypeAlias = authentication.ExpiredAccessTokenError


def authenticate_user(jwt: str) -> OutputDTO:
    serializer = serializers.AccessTokenSerializer(secrets.jwt_secret)

    return authentication.authenticate_user(
        jwt,
        access_token_serializer=serializer,
    )
