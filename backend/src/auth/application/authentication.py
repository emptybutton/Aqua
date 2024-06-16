from dataclasses import dataclass
from uuid import UUID

from src.auth.domain import value_objects
from src.auth.application.ports import serializers


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    user_id: UUID
    username: str


class BaseError(Exception): ...


class NoAccessTokenError(BaseError): ...


class ExpiredAccessTokenError(BaseError): ...


def authenticate_user(
    serialized_access_token: str,
    *,
    access_token_serializer: serializers.SymmetricSerializer[
        value_objects.AccessToken,
        str,
    ],
) -> OutputDTO:
    access_token = access_token_serializer.deserialized(serialized_access_token)

    if access_token is None:
        raise NoAccessTokenError()

    if access_token.is_expired:
        raise ExpiredAccessTokenError()

    return OutputDTO(
        user_id=access_token.user_id,
        username=access_token.username.text,
    )
