from abc import ABC, abstractmethod
from uuid import UUID

from auth.domain import entities
from auth.domain import value_objects as vos


class Users(ABC):
    @abstractmethod
    async def add(self, user: entities.User) -> None: ...

    @abstractmethod
    async def find_with_id(self, user_id: UUID) -> entities.User | None: ...

    @abstractmethod
    async def find_with_name(
        self, username: vos.Username
    ) -> entities.User | None: ...

    @abstractmethod
    async def contains_with_name(self, username: vos.Username) -> bool: ...

    @abstractmethod
    async def update(self, user: entities.User) -> None: ...


class Sessions(ABC):
    @abstractmethod
    async def add(self, session: entities.Session) -> None: ...

    @abstractmethod
    async def find_with_id(
        self, session_id: UUID
    ) -> entities.Session | None: ...

    @abstractmethod
    async def update(self, session: entities.Session) -> None: ...


class PreviousUsernames(ABC):
    @abstractmethod
    async def add(
        self, previous_username: entities.PreviousUsername
    ) -> None: ...

    @abstractmethod
    async def find_with_username(
        self, username: vos.Username
    ) -> entities.PreviousUsername | None: ...

    @abstractmethod
    async def contains_with_username(self, username: vos.Username) -> bool: ...
