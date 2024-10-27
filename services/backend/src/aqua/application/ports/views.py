from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from aqua.application.ports.repos import Users
from aqua.domain.model.core.aggregates.user.root import (
    CancellationOutput,
    User,
    WritingOutput,
)


class UserViewFrom[UsersT: Users, ViewT](ABC):
    @abstractmethod
    async def __call__(
        self, users: UsersT, *, user_id: UUID, date_: date
    ) -> ViewT: ...


class DayViewFrom[UsersT: Users, ViewT](ABC):
    @abstractmethod
    async def __call__(
        self, users: UsersT, *, user_id: UUID, date_: date
    ) -> ViewT: ...


class WritingViewOf[ViewT](ABC):
    @abstractmethod
    def __call__(self, *, user: User, output: WritingOutput) -> ViewT: ...


class CancellationViewOf[ViewT](ABC):
    @abstractmethod
    def __call__(self, *, user: User, output: CancellationOutput) -> ViewT: ...


class RegistrationViewOf[ViewT](ABC):
    @abstractmethod
    def __call__(self, user: User) -> ViewT: ...
