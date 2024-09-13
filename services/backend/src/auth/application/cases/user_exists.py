from auth.application.ports import repos
from auth.domain import value_objects as vos


async def perform(
    username_text: str,
    *,
    users: repos.Users,
    previous_usernames: repos.PreviousUsernames,
) -> bool:
    try:
        username = vos.Username(text=username_text)
    except vos.Username.Error:
        return False

    exists_with_name = users.contains_with_name(username)
    existed_with_name = previous_usernames.contains_with_username(username)

    return await exists_with_name or await existed_with_name
