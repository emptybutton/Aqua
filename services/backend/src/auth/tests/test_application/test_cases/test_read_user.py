from uuid import uuid4

from pytest import mark

from auth.domain import entities
from auth.application.cases import read_user
from auth.infrastructure import adapters


@mark.asyncio
async def test_with_invalid_id_and_empty_storage() -> None:
    users = adapters.repos.InMemoryUsers()

    result = await read_user.perform(uuid4(), users=users)

    assert result is None


@mark.asyncio
async def test_with_invalid_id_and_full_storage(
    user1: entities.User,
    user2: entities.User,
) -> None:
    users = adapters.repos.InMemoryUsers([user1, user2])

    result = await read_user.perform(uuid4(), users=users)

    assert result is None


@mark.asyncio
async def test_with_valid_id_and_full_storage(
    user1: entities.User,
    user2: entities.User,
) -> None:
    users = adapters.repos.InMemoryUsers([user1, user2])

    user = await read_user.perform(user2.id, users=users)

    assert user == user2
