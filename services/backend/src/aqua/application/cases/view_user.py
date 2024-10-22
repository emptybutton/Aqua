from uuid import UUID

from aqua.application.ports import repos, views


async def view_user[UsersT: repos.Users, ViewT](
    user_id: UUID,
    *,
    view_from: views.UserViewFrom[UsersT, ViewT],
    users: UsersT,
) -> ViewT:
    return await view_from(users, user_id=user_id)
