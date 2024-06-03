from abc import ABC, abstractmethod
from typing import Optional

from src.auth.domain import entities
from src.auth.domain import value_objects


class Users(ABC):
    @abstractmethod
    def add(self, user: entities.User) -> None: ...

    @abstractmethod
    def get_by_name(
        self, username: value_objects.Username
    ) -> Optional[entities.User]: ...

    @abstractmethod
    def has_with_name(self, username: value_objects.Username) -> bool: ...
