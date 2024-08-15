from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias

from auth.application.cases import refresh_token as case
from auth.domain import value_objects as vos
from auth.infrastructure.adapters import serializers
from auth.presentation.di.containers import sync_container


@dataclass(kw_only=True, frozen=True)
class Output:
    jwt: str
    refresh_token: str
    refresh_token_expiration_date: datetime


InvalidJWTError: TypeAlias = case.NoAccessTokenError

NotUTCRefreshTokenExpirationDateError: TypeAlias = (
    vos.RefreshToken.NotUTCExpirationDateError
)

ExpiredRefreshTokenError: TypeAlias = (
    vos.AccessToken.ExpiredRefreshTokenForRefreshingError
)

Error: TypeAlias = (
    case.Error
    | NotUTCRefreshTokenExpirationDateError
    | ExpiredRefreshTokenError
)


async def perform(
    jwt: str,
    refresh_token: str,
    refresh_token_expiration_date: datetime,
) -> Output:
    with sync_container() as container:
        result = await case.perform(
            jwt,
            refresh_token,
            refresh_token_expiration_date,
            access_token_serializer=(
                container.get(serializers.AccessTokenSerializer)
            ),
        )

    return Output(
        jwt=result.serialized_refreshed_access_token,
        refresh_token=result.refresh_token.text,
        refresh_token_expiration_date=result.refresh_token.expiration_date,
    )
