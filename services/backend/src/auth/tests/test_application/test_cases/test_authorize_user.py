from datetime import UTC, datetime, timedelta
from typing import Awaitable, Callable, TypeAlias

from dirty_equals import IsDatetime, IsNow
from pytest import fixture, mark, raises

from auth.application.cases import authorize_user
from auth.domain import entities
from auth.infrastructure import adapters
from shared.infrastructure.adapters.transactions import (
    InMemoryUoWTransactionFactory,
)

Case: TypeAlias = Callable[[str, str], Awaitable[authorize_user.Output]]


@fixture
def users(
    user1: entities.User,
    user2: entities.User,
) -> adapters.repos.InMemoryUsers:
    return adapters.repos.InMemoryUsers([user1, user2])


@fixture
def sessions() -> adapters.repos.InMemorySessions:
    return adapters.repos.InMemorySessions()


@fixture
def logger() -> adapters.loggers.InMemoryStorageLogger:
    return adapters.loggers.InMemoryStorageLogger()


@fixture
def case(
    users: adapters.repos.InMemoryUsers,
    sessions: adapters.repos.InMemorySessions,
    logger: adapters.loggers.InMemoryStorageLogger,
) -> Case:
    transaction_factory = InMemoryUoWTransactionFactory()
    password_serializer = adapters.serializers.ConcatenatingPasswordHasher()

    async def case_(name: str, password: str) -> authorize_user.Output:
        return await authorize_user.perform(
            name,
            password,
            users=users,
            sessions=sessions,
            password_serializer=password_serializer,
            user_transaction_for=transaction_factory,
            session_transaction_for=transaction_factory,
            logger=logger,
        )

    return case_


@mark.asyncio
async def test_user_storage_with_invalid_username(
    case: Case,
    users: adapters.repos.InMemoryUsers,
    user1: entities.User,
    user2: entities.User,
) -> None:
    with raises(authorize_user.NoUserError):
        await case("", "Ab345678")

    assert tuple(users) == (user1, user2)


@mark.asyncio
async def test_session_storage_with_invalid_username(
    case: Case,
    sessions: adapters.repos.InMemorySessions,
) -> None:
    with raises(authorize_user.NoUserError):
        await case("", "Ab345678")

    assert len(sessions) == 0


@mark.asyncio
async def test_logger_with_invalid_username(
    case: Case,
    logger: adapters.loggers.InMemoryStorageLogger,
) -> None:
    with raises(authorize_user.NoUserError):
        await case("", "Ab345678")

    assert logger.is_empty


@mark.asyncio
async def test_user_storage_with_invalid_password(
    case: Case,
    users: adapters.repos.InMemoryUsers,
    user1: entities.User,
    user2: entities.User,
) -> None:
    with raises(authorize_user.IncorrectPasswordError):
        await case("usernameX", "ab345678")

    assert tuple(users) == (user1, user2)


@mark.asyncio
async def test_session_storage_with_invalid_password(
    case: Case,
    sessions: adapters.repos.InMemorySessions,
) -> None:
    with raises(authorize_user.IncorrectPasswordError):
        await case("usernameX", "ab345678")

    assert len(sessions) == 0


@mark.asyncio
async def test_logger_with_invalid_password(
    case: Case,
    logger: adapters.loggers.InMemoryStorageLogger,
) -> None:
    with raises(authorize_user.IncorrectPasswordError):
        await case("usernameX", "ab345678")

    assert logger.is_empty


@mark.asyncio
async def test_user_storage_with_inappropriate_username(
    case: Case,
    users: adapters.repos.InMemoryUsers,
    user1: entities.User,
    user2: entities.User,
) -> None:
    with raises(authorize_user.NoUserError):
        await case("usernameX", "Ab345678")

    assert tuple(users) == (user1, user2)


@mark.asyncio
async def test_session_storage_with_inappropriate_username(
    case: Case,
    sessions: adapters.repos.InMemorySessions,
) -> None:
    with raises(authorize_user.NoUserError):
        await case("usernameX", "Ab345678")

    assert len(sessions) == 0


@mark.asyncio
async def test_logger_with_inappropriate_username(
    case: Case,
    logger: adapters.loggers.InMemoryStorageLogger,
) -> None:
    with raises(authorize_user.IncorrectPasswordError):
        await case("usernameX", "ab345678")

    assert logger.is_empty


@mark.asyncio
async def test_user_storage_with_inappropriate_password(
    case: Case,
    users: adapters.repos.InMemoryUsers,
    user1: entities.User,
    user2: entities.User,
) -> None:
    with raises(authorize_user.IncorrectPasswordError):
        await case("username1", "Ab345678")

    assert tuple(users) == (user1, user2)


@mark.asyncio
async def test_session_storage_with_inappropriate_password(
    case: Case,
    sessions: adapters.repos.InMemorySessions,
) -> None:
    with raises(authorize_user.IncorrectPasswordError):
        await case("username1", "Ab345678")

    assert len(sessions) == 0


@mark.asyncio
async def test_logger_with_inappropriate_password(
    case: Case,
    logger: adapters.loggers.InMemoryStorageLogger,
) -> None:
    with raises(authorize_user.IncorrectPasswordError):
        await case("username1", "Ab345678")

    assert logger.is_empty


@mark.asyncio
async def test_result_user(
    case: Case,
    user1: entities.User,
) -> None:
    result = await case("username1", "pAssword1")

    assert result.user == user1


@mark.asyncio
async def test_result_session(case: Case) -> None:
    result = await case("username1", "pAssword1")

    assert result.session.user_id == result.user.id
    assert result.session.lifetime.start_time == IsNow(tz=UTC)
    assert result.session.lifetime.end_time == IsDatetime(
        approx=datetime.now(UTC) + timedelta(days=60),
    )


@mark.asyncio
async def test_user_storage(
    case: Case,
    users: adapters.repos.InMemoryUsers,
    user1: entities.User,
    user2: entities.User,
) -> None:
    await case("username1", "pAssword1")

    assert tuple(users) == (user1, user2)


@mark.asyncio
async def test_session_storage(
    case: Case,
    sessions: adapters.repos.InMemorySessions,
) -> None:
    result = await case("username1", "pAssword1")

    assert tuple(sessions) == (result.session,)


@mark.asyncio
async def test_logger_log_size(
    case: Case,
    logger: adapters.loggers.InMemoryStorageLogger,
) -> None:
    await case("username1", "pAssword1")

    assert len(logger.session_extension_logs) == 0
    assert len(logger.registration_logs) == 0
    assert len(logger.login_logs) == 1


@mark.asyncio
async def test_logger_log_values(
    case: Case,
    logger: adapters.loggers.InMemoryStorageLogger,
) -> None:
    result = await case("username1", "pAssword1")

    assert logger.login_logs[0].user == result.user
    assert logger.login_logs[0].session == result.session
