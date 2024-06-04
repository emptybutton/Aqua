from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Optional

from src.auth.domain import value_objects
from src.auth.application.ports import serializers


@dataclass(frozen=True)
class ReauthorizationDTO:
    new_refresh_token: value_objects.RefreshToken
    serialized_new_access_token: str


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
    generate_refresh_token_text: Callable[[], str],
) -> Optional[ReauthorizationDTO]:
    access_token = access_token_serializer.deserialized(serialized_access_token)

    if access_token is None:
        raise NoAccessTokenError()

    if not access_token.is_expired:
        return None

    refresh_token = value_objects.RefreshToken(
        refresh_token_text, refresh_token_expiration_date
    )

    if refresh_token.is_expired:
        raise ExpiredRefreshTokenError()

    new_access_token = value_objects.AccessToken(
        access_token.user_id,
        access_token.username,
    )

    new_refresh_token_text = generate_refresh_token_text()
    new_refresh_token = value_objects.RefreshToken(new_refresh_token_text)

    return ReauthorizationDTO(
        new_refresh_token,
        access_token_serializer.serialized(new_access_token),
    )
