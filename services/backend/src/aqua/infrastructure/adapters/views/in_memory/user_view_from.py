from datetime import date
from uuid import UUID

from aqua.application.ports.views import UserViewFrom
from aqua.infrastructure.adapters.repos.in_memory.users import InMemoryUsers
from aqua.infrastructure.periphery.views.in_memory.user_view import (
    InMemoryUserView,
)


class InMemoryUserViewFrom(UserViewFrom[InMemoryUsers, InMemoryUserView]):
    async def __call__(
        self, users: InMemoryUsers, *, user_id: UUID, date_: date
    ) -> InMemoryUserView:
        user = await users.user_with_id(user_id)
        day = users.day_with_user_id_and_date(user_id=user_id, date_=date_)

        return InMemoryUserView(user=user, day=day)
