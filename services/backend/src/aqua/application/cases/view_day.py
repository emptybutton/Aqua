from datetime import date
from uuid import UUID

from aqua.application.ports import repos, views


async def view_day[UsersT: repos.Users, ViewT](
    user_id: UUID,
    date_: date,
    *,
    view_from: views.DayViewFrom[UsersT, ViewT],
    users: UsersT,
) -> ViewT:
    return await view_from(users, user_id=user_id, date_=date_)
