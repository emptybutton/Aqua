from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from auth.application.cases import authenticate_user
from auth.domain import value_objects as vos
from auth.infrastructure.adapters import serializers
from auth.presentation.di.containers import sync_container


@dataclass(kw_only=True, frozen=True)
class Output:
    user_id: UUID


InvalidJWTError: TypeAlias = authenticate_user.NoAccessTokenError

ExpiredJWTError: TypeAlias = (
    vos.AccessToken.ExpiredForAuthenticationError
)

Error: TypeAlias = (
    authenticate_user.Error
    | InvalidJWTError
    | ExpiredJWTError
)


async def perform(jwt: str) -> Output:
    with sync_container() as container:
        serializer = container.get(serializers.AccessTokenSerializer)

        access_token = await authenticate_user.perform(
            jwt,
            access_token_serializer=serializer,
        )

    return Output(user_id=access_token.user_id)
