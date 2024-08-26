from datetime import timedelta
from uuid import uuid4

from dirty_equals import IsDatetime
from pytest import mark, raises

from auth.application.cases import authenticate_user
from auth.domain import entities
from auth.infrastructure import adapters
from shared.infrastructure.adapters.transactions import (
    InMemoryUoWTransactionFactory,
)


@mark.asyncio
async def test_storage_without_sessions() -> None:
    sessions = adapters.repos.InMemorySessions()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(authenticate_user.NoSessionError):
        await authenticate_user.perform(
            uuid4(),
            sessions=sessions,
            transaction_for=transaction_factory,
            logger=logger,
        )

    assert len(sessions) == 0


@mark.asyncio
async def test_logger_without_sessions() -> None:
    sessions = adapters.repos.InMemorySessions()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(authenticate_user.NoSessionError):
        await authenticate_user.perform(
            uuid4(),
            sessions=sessions,
            transaction_for=transaction_factory,
            logger=logger,
        )

    assert logger.is_empty


@mark.asyncio
async def test_logger_with_not_suitable_sessions(
    expired_session: entities.Session, not_expired_session: entities.Session
) -> None:
    sessions = adapters.repos.InMemorySessions([
        expired_session,
        not_expired_session,
    ])
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(authenticate_user.NoSessionError):
        await authenticate_user.perform(
            uuid4(),
            sessions=sessions,
            transaction_for=transaction_factory,
            logger=logger,
        )

    assert logger.is_empty


@mark.asyncio
async def test_storage_with_not_suitable_sessions(
    expired_session: entities.Session, not_expired_session: entities.Session
) -> None:
    sessions = adapters.repos.InMemorySessions([
        expired_session,
        not_expired_session,
    ])
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(authenticate_user.NoSessionError):
        await authenticate_user.perform(
            uuid4(),
            sessions=sessions,
            transaction_for=transaction_factory,
            logger=logger,
        )

    assert tuple(sessions) == (expired_session, not_expired_session)


@mark.asyncio
async def test_storage_with_expired_session(
    expired_session: entities.Session, not_expired_session: entities.Session
) -> None:
    sessions = adapters.repos.InMemorySessions([
        expired_session,
        not_expired_session,
    ])
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(entities.Session.ExpiredLifetimeForAuthenticationError):
        await authenticate_user.perform(
            expired_session.id,
            sessions=sessions,
            transaction_for=transaction_factory,
            logger=logger,
        )

    assert tuple(sessions) == (expired_session, not_expired_session)


@mark.asyncio
async def test_logger_log_values(
    expired_session: entities.Session, not_expired_session: entities.Session
) -> None:
    sessions = adapters.repos.InMemorySessions([
        expired_session,
        not_expired_session,
    ])
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    result_session = await authenticate_user.perform(
        not_expired_session.id,
        sessions=sessions,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert logger.session_extension_logs[0].session == result_session


@mark.asyncio
async def test_logger_log_size(
    expired_session: entities.Session, not_expired_session: entities.Session
) -> None:
    sessions = adapters.repos.InMemorySessions([
        expired_session,
        not_expired_session,
    ])
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    await authenticate_user.perform(
        not_expired_session.id,
        sessions=sessions,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert len(logger.session_extension_logs) == 1
    assert len(logger.registration_logs) == 0
    assert len(logger.login_logs) == 0


@mark.asyncio
async def test_storage(
    expired_session: entities.Session, not_expired_session: entities.Session
) -> None:
    sessions = adapters.repos.InMemorySessions([
        expired_session,
        not_expired_session,
    ])
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    result_session = await authenticate_user.perform(
        not_expired_session.id,
        sessions=sessions,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert tuple(sessions) == (expired_session, result_session)


@mark.asyncio
async def test_result(
    expired_session: entities.Session, not_expired_session: entities.Session
) -> None:
    sessions = adapters.repos.InMemorySessions([
        expired_session,
        not_expired_session,
    ])
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()
    assert not_expired_session.lifetime.start_time is not None
    lifetime_end_time = IsDatetime(
        approx=not_expired_session.lifetime.start_time + timedelta(days=62)
    )

    result_session = await authenticate_user.perform(
        not_expired_session.id,
        sessions=sessions,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert result_session.id == not_expired_session.id
    assert result_session.user_id == not_expired_session.user_id
    assert (
        result_session.lifetime.start_time
        == not_expired_session.lifetime.start_time
    )
    assert (
        result_session.lifetime.start_time
        == not_expired_session.lifetime.start_time
    )
    assert result_session.lifetime.end_time == lifetime_end_time
