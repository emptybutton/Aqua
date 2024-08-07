from dataclasses import dataclass
from datetime import datetime

from auth.domain import value_objects as vos
from auth.application.ports import serializers


@dataclass(kw_only=True, frozen=True)
class Output:
    serialized_refreshed_access_token: str


class Error(Exception): ...


class NoAccessTokenError(Error): ...


async def perform(
    serialized_access_token: str,
    refresh_token_text: str,
    refresh_token_expiration_date: datetime,
    *,
    access_token_serializer: serializers.SecureSymmetricSerializer[
        vos.AccessToken,
        str,
    ],
) -> Output:
    access_token = access_token_serializer.deserialized(serialized_access_token)

    if access_token is None:
        raise NoAccessTokenError()

    refresh_token = vos.RefreshToken(
        text=refresh_token_text,
        expiration_date=refresh_token_expiration_date,
    )

    refreshed_access_token = access_token.refresh(refresh_token=refresh_token)
    serialized_refreshed_access_token = (
        access_token_serializer.serialized(refreshed_access_token)
    )

    return Output(
        serialized_refreshed_access_token=serialized_refreshed_access_token,
    )
