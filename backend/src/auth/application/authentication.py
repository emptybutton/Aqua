from dataclasses import dataclass
from typing import Callable, TypeVar, Optional

from src.auth.domain import value_objects
from src.auth.application import errors
from src.auth.application.ports import serializers
from src.auth.application.ports.places import Place


_RefreshTokenContainerT = TypeVar(
    "_RefreshTokenContainerT",
    bound=Place[value_objects.RefreshToken],
)


@dataclass(frozen=True)
class OutputDTO:
    new_refresh_token: value_objects.RefreshToken
    serialized_new_access_token: str


def authenticate_user(
    serialized_access_token: str,
    refresh_token_place: _RefreshTokenContainerT,
    *,
    access_token_serializer: serializers.SymmetricSerializer[
        value_objects.AccessToken,
        str,
    ],
    generate_refresh_token_text: Callable[[], str],
) -> Optional[OutputDTO]:
    access_token = access_token_serializer.deserialized(serialized_access_token)

    if access_token is None:
        raise errors.UserIsNotAuthenticated()

    if not access_token.is_expired:
        return None

    refresh_token = refresh_token_place.get()

    if refresh_token is None or refresh_token.is_expired:
        raise errors.UserIsNotAuthenticated()

    new_access_token = value_objects.AccessToken(
        access_token.user_id,
        access_token.username,
    )

    new_refresh_token_text = generate_refresh_token_text()
    new_refresh_token = value_objects.RefreshToken(new_refresh_token_text)

    refresh_token_place.set(new_refresh_token)

    return OutputDTO(
        new_refresh_token,
        access_token_serializer.serialized(new_access_token),
    )
