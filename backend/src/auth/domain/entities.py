from dataclasses import dataclass, field
from uuid import uuid4

from src.auth.domain.value_objects import Username, PasswordHash


@dataclass
class User:
    name: Username
    password_hash: PasswordHash
    id: int = field(default_factory=lambda: uuid4().int)
