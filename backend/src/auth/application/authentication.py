from datetime import datetime

from src.auth.domain import value_objects
from src.auth.application.ports import serializers


class BaseError(Exception): ...


class NoAccessTokenError(BaseError): ...


class ExpiredRefreshTokenError(BaseError): ...


def authenticate_user(
    serialized_access_token: str,
    refresh_token_text: str,
    refresh_token_expiration_date: datetime,
    *,
    access_token_serializer: serializers.SymmetricSerializer[
        value_objects.AccessToken,
        str,
    ],
) -> None:
    access_token = access_token_serializer.deserialized(serialized_access_token)

    if access_token is None:
        raise NoAccessTokenError()

    if not access_token.is_expired:
        return

    refresh_token = value_objects.RefreshToken(
        refresh_token_text, refresh_token_expiration_date
    )

    if refresh_token.is_expired:
        raise ExpiredRefreshTokenError()
