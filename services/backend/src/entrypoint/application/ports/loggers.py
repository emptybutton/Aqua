from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID


_ClientT = TypeVar("_ClientT")


class AquaLogger(ABC, Generic[_ClientT]):
    @abstractmethod
    async def log_aqua_is_not_working(self, aqua: _ClientT) -> None: ...

    @abstractmethod
    async def log_no_user_from_other_parts(
        self, aqua: _ClientT, user_id: UUID
    ) -> None: ...


class AuthLogger(ABC, Generic[_ClientT]):
    @abstractmethod
    async def log_auth_is_not_working(self, auth: _ClientT) -> None: ...

    @abstractmethod
    async def log_no_user_from_other_parts(
        self, aqua: _ClientT, user_id: UUID
    ) -> None: ...
