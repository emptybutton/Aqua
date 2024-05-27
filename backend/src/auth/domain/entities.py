from dataclasses import dataclass
from typing import Optional

from src.auth.domain.value_objects import Username


@dataclass
class User:
    id: Optional[int]
    name: Username
