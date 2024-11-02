from uuid import UUID

from aqua.domain.model.core.aggregates.user.root import User
from aqua.infrastructure.adapters.repos.mongo.users import MongoUsers


async def test_user1(
    full_mongo: None,  # noqa: ARG001
    user1: User,
    mongo_users: MongoUsers,
) -> None:
    result = await mongo_users.user_with_id(user1.id)

    assert result == user1


async def test_user2(
    full_mongo: None,  # noqa: ARG001
    user2: User,
    mongo_users: MongoUsers,
) -> None:
    result = await mongo_users.user_with_id(user2.id)

    assert result == user2


async def test_no_user(full_mongo: None, mongo_users: MongoUsers) -> None:  # noqa: ARG001
    result = await mongo_users.user_with_id(UUID(int=-1))

    assert result is None
