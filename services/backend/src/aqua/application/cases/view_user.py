from datetime import UTC, datetime
from uuid import UUID

from aqua.application.ports import repos, views
from aqua.domain.model.primitives.vos.time import Time


async def view_user[UsersT: repos.Users, ViewT](
    user_id: UUID,
    *,
    view_from: views.UserViewFrom[UsersT, ViewT],
    users: UsersT,
) -> ViewT:
    current_time = Time.with_(datetime_=datetime.now(UTC)).unwrap()
    current_date = current_time.datetime_.date()

    return await view_from(users, user_id=user_id, date_=current_date)
