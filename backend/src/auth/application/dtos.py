from dataclasses import dataclass
from typing import Optional

from src.auth.domain import entities


@dataclass(frozen=True)
class Registration:
    user: entities.User
    serialized_access_token: str
    refresh_token_text: str


@dataclass(frozen=True)
class Authentication:
    serialized_new_access_token: Optional[str] = None
