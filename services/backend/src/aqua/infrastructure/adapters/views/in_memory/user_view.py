from uuid import UUID

from aqua.application.ports.views import UserViewFrom
from aqua.infrastructure.adapters.repos.in_memory.user import InMemoryUsers
from aqua.infrastructure.periphery.views.in_memory.user_view import (
    InMemoryUserView,
)


class InMemoryUserViewFrom(UserViewFrom[InMemoryUsers, InMemoryUserView]):
    async def __call__(
        self, users: InMemoryUsers, *, user_id: UUID
    ) -> InMemoryUserView:
        return await users.user_with_id(user_id)
