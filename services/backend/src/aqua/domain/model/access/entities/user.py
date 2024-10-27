from dataclasses import dataclass
from typing import Never
from uuid import UUID

from aqua.domain.framework.entity import Entity


@dataclass(kw_only=True)
class User(Entity[UUID, Never]): ...
