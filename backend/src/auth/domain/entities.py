from dataclasses import dataclass, field
from uuid import uuid4, UUID

from auth.domain.value_objects import Username, PasswordHash


@dataclass
class User:
    name: Username
    password_hash: PasswordHash
    id: UUID = field(default_factory=uuid4)
