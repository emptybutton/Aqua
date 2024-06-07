from dataclasses import dataclass
from datetime import datetime

from src.auth.domain import value_objects
from src.auth.application.ports import serializers


@dataclass(frozen=True)
class OutputDTO:
    serialized_new_access_token: str


class BaseError(Exception): ...


class NoAccessTokenError(BaseError): ...


class ExpiredRefreshTokenError(BaseError): ...


def extend_access(
    serialized_access_token: str,
    refresh_token_text: str,
    refresh_token_expiration_date: datetime,
    *,
    access_token_serializer: serializers.SymmetricSerializer[
        value_objects.AccessToken,
        str,
    ],
) -> OutputDTO:
    access_token = access_token_serializer.deserialized(serialized_access_token)

    if access_token is None:
        raise NoAccessTokenError()

    refresh_token = value_objects.RefreshToken(
        refresh_token_text,
        refresh_token_expiration_date,
    )

    if refresh_token.is_expired:
        raise ExpiredRefreshTokenError()

    new_access_token = value_objects.refreshed(access_token)
    serialized_new_access_token = (
        access_token_serializer.serialized(new_access_token)
    )

    return OutputDTO(serialized_new_access_token)
