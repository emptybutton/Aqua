from dataclasses import dataclass

from src.auth.domain import entities, value_objects


@dataclass(frozen=True)
class Registration:
    user: entities.User
    refresh_token: value_objects.RefreshToken
    serialized_access_token: str


@dataclass(frozen=True)
class Authorization:
    user: entities.User
    refresh_token: value_objects.RefreshToken
    serialized_access_token: str


@dataclass(frozen=True)
class Authentication:
    new_refresh_token: value_objects.RefreshToken
    serialized_new_access_token: str
