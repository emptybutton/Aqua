from datetime import date
from uuid import UUID

from aqua.application.ports.views import DayViewFrom
from aqua.infrastructure.adapters.repos.in_memory.user import InMemoryUsers
from aqua.infrastructure.periphery.views.in_memory.day_view import (
    InMemoryDayView,
)


class InMemoryDayViewFrom(DayViewFrom[InMemoryUsers, InMemoryDayView]):
    async def __call__(
        self, users: InMemoryUsers, *, user_id: UUID, date_: date
    ) -> InMemoryDayView:
        user = await users.user_with_id(user_id)
        day = users.day_with_user_id_and_date(user_id=user_id, date_=date_)

        return InMemoryDayView(user=user, day=day)
