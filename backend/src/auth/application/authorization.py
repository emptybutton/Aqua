from dataclasses import dataclass
from typing import Callable, Optional

from src.auth.domain import entities, value_objects
from src.auth.application.ports import repos, serializers
from src.auth.application.ports.places import Place


@dataclass(frozen=True)
class OutputDTO:
    user: entities.User
    refresh_token: value_objects.RefreshToken
    serialized_access_token: str


async def authorize_user(  # noqa: PLR0913
    name_text: str,
    password_text: str,
    refresh_token_place: Place[value_objects.RefreshToken],
    *,
    users: repos.Users,
    password_serializer: serializers.AsymmetricSerializer[
        value_objects.Password,
        value_objects.PasswordHash,
    ],
    access_token_serializer: serializers.SymmetricSerializer[
        value_objects.AccessToken,
        str,
    ],
    generate_refresh_token_text: Callable[[], str],
) -> Optional[OutputDTO]:
    user = await users.get_by_name(value_objects.Username(name_text))

    if user is None:
        return None

    password = value_objects.Password(password_text)
    password_hash = password_serializer.serialized(password)

    if user.password_hash != password_hash:
        return None

    refresh_token = value_objects.RefreshToken(generate_refresh_token_text())
    refresh_token_place.set(refresh_token)

    access_token = value_objects.AccessToken(user.id, user.name)
    serialized_access_token = access_token_serializer.serialized(access_token)

    return OutputDTO(user, refresh_token, serialized_access_token)
