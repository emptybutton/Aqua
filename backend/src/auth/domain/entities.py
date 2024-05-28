from dataclasses import dataclass
from typing import Optional

from src.auth.domain.value_objects import Username, PasswordHash


@dataclass
class User:
    id: Optional[int]
    name: Username
    password_hash: PasswordHash
