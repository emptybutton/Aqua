from datetime import UTC, datetime, timedelta

from dirty_equals import IsDatetime, IsNow
from pytest import mark, raises

from auth.application.cases import register_user
from auth.domain import entities
from auth.domain import value_objects as vos
from auth.infrastructure import adapters
from shared.infrastructure.adapters.transactions import (
    InMemoryUoWTransactionFactory,
)


@mark.asyncio
async def test_storages_with_invalid_name(
    user1: entities.User, user2: entities.User
) -> None:
    users = adapters.repos.InMemoryUsers([user1, user2])
    sessions = adapters.repos.InMemorySessions()
    transaction_factory = InMemoryUoWTransactionFactory()
    password_serializer = adapters.serializers.ConcatenatingPasswordHasher()
    logger = adapters.loggers.InMemoryStorageLogger()

    with raises(vos.Username.EmptyError):
        await register_user.perform(
            "",
            "Ab345678",
            users=users,
            sessions=sessions,
            user_transaction_for=transaction_factory,
            session_transaction_for=transaction_factory,
            password_serializer=password_serializer,
            logger=logger,
        )

    assert tuple(users) == (user1, user2)


@mark.asyncio
async def test_storages_with_invalid_password(
    user1: entities.User, user2: entities.User
) -> None:
    users = adapters.repos.InMemoryUsers([user1, user2])
    sessions = adapters.repos.InMemorySessions()
    transaction_factory = InMemoryUoWTransactionFactory()
    password_serializer = adapters.serializers.ConcatenatingPasswordHasher()
    logger = adapters.loggers.InMemoryStorageLogger()

    with raises(vos.Password.WeekError):
        await register_user.perform(
            "username1",
            "ab345678",
            users=users,
            sessions=sessions,
            user_transaction_for=transaction_factory,
            session_transaction_for=transaction_factory,
            password_serializer=password_serializer,
            logger=logger,
        )

    assert tuple(users) == (user1, user2)


@mark.asyncio
async def test_loggers_with_invalid_name(
    user1: entities.User, user2: entities.User
) -> None:
    users = adapters.repos.InMemoryUsers([user1, user2])
    sessions = adapters.repos.InMemorySessions()
    transaction_factory = InMemoryUoWTransactionFactory()
    password_serializer = adapters.serializers.ConcatenatingPasswordHasher()
    logger = adapters.loggers.InMemoryStorageLogger()

    with raises(vos.Username.EmptyError):
        await register_user.perform(
            "",
            "Ab345678",
            users=users,
            sessions=sessions,
            user_transaction_for=transaction_factory,
            session_transaction_for=transaction_factory,
            password_serializer=password_serializer,
            logger=logger,
        )

    assert logger.is_empty


@mark.asyncio
async def test_loggers_with_invalid_password(
    user1: entities.User, user2: entities.User
) -> None:
    users = adapters.repos.InMemoryUsers([user1, user2])
    sessions = adapters.repos.InMemorySessions()
    transaction_factory = InMemoryUoWTransactionFactory()
    password_serializer = adapters.serializers.ConcatenatingPasswordHasher()
    logger = adapters.loggers.InMemoryStorageLogger()

    with raises(vos.Password.WeekError):
        await register_user.perform(
            "username1",
            "ab345678",
            users=users,
            sessions=sessions,
            user_transaction_for=transaction_factory,
            session_transaction_for=transaction_factory,
            password_serializer=password_serializer,
            logger=logger,
        )

    assert logger.is_empty


@mark.asyncio
async def test_result_user(user1: entities.User, user2: entities.User) -> None:
    users = adapters.repos.InMemoryUsers([user1, user2])
    sessions = adapters.repos.InMemorySessions()
    transaction_factory = InMemoryUoWTransactionFactory()
    password_serializer = adapters.serializers.ConcatenatingPasswordHasher()
    logger = adapters.loggers.InMemoryStorageLogger()

    result = await register_user.perform(
        "usernameX",
        "Ab345678",
        users=users,
        sessions=sessions,
        user_transaction_for=transaction_factory,
        session_transaction_for=transaction_factory,
        password_serializer=password_serializer,
        logger=logger,
    )

    assert result.user.name.text == "usernameX"
    assert result.user.password_hash.text == "Ab345678_hash"


@mark.asyncio
async def test_result_session(
    user1: entities.User, user2: entities.User
) -> None:
    users = adapters.repos.InMemoryUsers([user1, user2])
    sessions = adapters.repos.InMemorySessions()
    transaction_factory = InMemoryUoWTransactionFactory()
    password_serializer = adapters.serializers.ConcatenatingPasswordHasher()
    logger = adapters.loggers.InMemoryStorageLogger()

    result = await register_user.perform(
        "usernameX",
        "Ab345678",
        users=users,
        sessions=sessions,
        user_transaction_for=transaction_factory,
        session_transaction_for=transaction_factory,
        password_serializer=password_serializer,
        logger=logger,
    )

    assert result.session.user_id == result.user.id
    assert result.session.lifetime.start_time == IsNow(tz=UTC)
    assert result.session.lifetime.end_time == IsDatetime(
        approx=datetime.now(UTC) + timedelta(days=60)
    )


@mark.asyncio
async def test_logger_log_values(
    user1: entities.User, user2: entities.User
) -> None:
    users = adapters.repos.InMemoryUsers([user1, user2])
    sessions = adapters.repos.InMemorySessions()
    transaction_factory = InMemoryUoWTransactionFactory()
    password_serializer = adapters.serializers.ConcatenatingPasswordHasher()
    logger = adapters.loggers.InMemoryStorageLogger()

    result = await register_user.perform(
        "usernameX",
        "Ab345678",
        users=users,
        sessions=sessions,
        user_transaction_for=transaction_factory,
        session_transaction_for=transaction_factory,
        password_serializer=password_serializer,
        logger=logger,
    )

    assert logger.registration_logs[0].user == result.user
    assert logger.registration_logs[0].session == result.session


@mark.asyncio
async def test_logger_log_size(
    user1: entities.User, user2: entities.User
) -> None:
    users = adapters.repos.InMemoryUsers([user1, user2])
    sessions = adapters.repos.InMemorySessions()
    transaction_factory = InMemoryUoWTransactionFactory()
    password_serializer = adapters.serializers.ConcatenatingPasswordHasher()
    logger = adapters.loggers.InMemoryStorageLogger()

    await register_user.perform(
        "usernameX",
        "Ab345678",
        users=users,
        sessions=sessions,
        user_transaction_for=transaction_factory,
        session_transaction_for=transaction_factory,
        password_serializer=password_serializer,
        logger=logger,
    )

    assert len(logger.registration_logs) == 1
    assert len(logger.login_logs) == 0
    assert len(logger.session_extension_logs) == 0


@mark.asyncio
async def test_user_storage_values(
    user1: entities.User, user2: entities.User
) -> None:
    users = adapters.repos.InMemoryUsers([user1, user2])
    sessions = adapters.repos.InMemorySessions()
    transaction_factory = InMemoryUoWTransactionFactory()
    password_serializer = adapters.serializers.ConcatenatingPasswordHasher()
    logger = adapters.loggers.InMemoryStorageLogger()

    result = await register_user.perform(
        "usernameX",
        "Ab345678",
        users=users,
        sessions=sessions,
        user_transaction_for=transaction_factory,
        session_transaction_for=transaction_factory,
        password_serializer=password_serializer,
        logger=logger,
    )

    assert tuple(users) == (user1, user2, result.user)


@mark.asyncio
async def test_session_storage_values(
    user1: entities.User, user2: entities.User
) -> None:
    users = adapters.repos.InMemoryUsers([user1, user2])
    sessions = adapters.repos.InMemorySessions()
    transaction_factory = InMemoryUoWTransactionFactory()
    password_serializer = adapters.serializers.ConcatenatingPasswordHasher()
    logger = adapters.loggers.InMemoryStorageLogger()

    result = await register_user.perform(
        "usernameX",
        "Ab345678",
        users=users,
        sessions=sessions,
        user_transaction_for=transaction_factory,
        session_transaction_for=transaction_factory,
        password_serializer=password_serializer,
        logger=logger,
    )

    assert tuple(sessions) == (result.session,)


@mark.asyncio
async def test_logger_log_size_on_registred_user_registration(
    user1: entities.User, user2: entities.User
) -> None:
    users = adapters.repos.InMemoryUsers([user1, user2])
    sessions = adapters.repos.InMemorySessions()
    transaction_factory = InMemoryUoWTransactionFactory()
    password_serializer = adapters.serializers.ConcatenatingPasswordHasher()
    logger = adapters.loggers.InMemoryStorageLogger()

    with raises(register_user.UserIsAlreadyRegisteredError):
        await register_user.perform(
            "username1",
            "Ab345678",
            users=users,
            sessions=sessions,
            user_transaction_for=transaction_factory,
            session_transaction_for=transaction_factory,
            password_serializer=password_serializer,
            logger=logger,
        )

    assert len(logger.registration_logs) == 0
    assert len(logger.login_logs) == 0
    assert len(logger.session_extension_logs) == 0


@mark.asyncio
async def test_user_storage_size_on_registred_user_registration(
    user1: entities.User, user2: entities.User
) -> None:
    users = adapters.repos.InMemoryUsers([user1, user2])
    sessions = adapters.repos.InMemorySessions()
    transaction_factory = InMemoryUoWTransactionFactory()
    password_serializer = adapters.serializers.ConcatenatingPasswordHasher()
    logger = adapters.loggers.InMemoryStorageLogger()

    with raises(register_user.UserIsAlreadyRegisteredError):
        await register_user.perform(
            "username1",
            "Ab345678",
            users=users,
            sessions=sessions,
            user_transaction_for=transaction_factory,
            session_transaction_for=transaction_factory,
            password_serializer=password_serializer,
            logger=logger,
        )

    assert len(users) == 2


@mark.asyncio
async def test_session_storage_size_on_registred_user_registration(
    user1: entities.User, user2: entities.User
) -> None:
    users = adapters.repos.InMemoryUsers([user1, user2])
    sessions = adapters.repos.InMemorySessions()
    transaction_factory = InMemoryUoWTransactionFactory()
    password_serializer = adapters.serializers.ConcatenatingPasswordHasher()
    logger = adapters.loggers.InMemoryStorageLogger()

    with raises(register_user.UserIsAlreadyRegisteredError):
        await register_user.perform(
            "username1",
            "Ab345678",
            users=users,
            sessions=sessions,
            user_transaction_for=transaction_factory,
            session_transaction_for=transaction_factory,
            password_serializer=password_serializer,
            logger=logger,
        )

    assert len(sessions) == 0
