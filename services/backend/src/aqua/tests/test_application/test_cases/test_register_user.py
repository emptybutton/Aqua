from uuid import UUID, uuid4

from pytest import mark, raises

from aqua.application.cases import register_user
from aqua.domain import entities
from aqua.domain import value_objects as vos
from aqua.infrastructure import adapters
from shared.infrastructure.adapters.transactions import (
    InMemoryUoWTransactionFactory,
)


@mark.asyncio
async def test_result_user_data() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()
    expected_user = entities.User(
        id=UUID(int=1),
        weight=vos.Weight(kilograms=70),
        glass=vos.Glass(capacity=vos.Water(milliliters=300)),
        _target=vos.WaterBalance(water=vos.Water(milliliters=5000)),
    )

    user = await register_user.perform(
        UUID(int=1),
        5000,
        300,
        70,
        users=users,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert user == expected_user


@mark.asyncio
async def test_user_in_storage() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()
    expected_user = entities.User(
        id=UUID(int=1),
        weight=vos.Weight(kilograms=70),
        glass=vos.Glass(capacity=vos.Water(milliliters=300)),
        _target=vos.WaterBalance(water=vos.Water(milliliters=5000)),
    )

    await register_user.perform(
        UUID(int=1),
        5000,
        300,
        70,
        users=users,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert next(iter(users)) == expected_user


@mark.asyncio
async def test_storage_size() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    await register_user.perform(
        UUID(int=1),
        5000,
        300,
        70,
        users=users,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert len(users) == 1


@mark.asyncio
async def test_not_empty_on_start_storage_size() -> None:
    users = adapters.repos.InMemoryUsers(
        entities.User(
            id=uuid4(),
            weight=vos.Weight(kilograms=70),
            glass=vos.Glass(capacity=vos.Water(milliliters=300)),
            _target=vos.WaterBalance(water=vos.Water(milliliters=5000)),
        )
        for _ in range(10)
    )
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    await register_user.perform(
        UUID(int=1),
        5000,
        300,
        70,
        users=users,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert len(users) == 11


@mark.asyncio
async def test_registration_log() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()
    expected_user = entities.User(
        id=UUID(int=1),
        weight=vos.Weight(kilograms=70),
        glass=vos.Glass(capacity=vos.Water(milliliters=300)),
        _target=vos.WaterBalance(water=vos.Water(milliliters=5000)),
    )

    await register_user.perform(
        UUID(int=1),
        5000,
        300,
        70,
        users=users,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert logger.registered_users[0] == expected_user


@mark.asyncio
async def test_with_invalid_grass() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(vos.Water.IncorrectAmountError):
        await register_user.perform(
            UUID(int=1),
            5000,
            -300,
            70,
            users=users,
            transaction_for=transaction_factory,
            logger=logger,
        )


@mark.asyncio
async def test_with_invalid_weight() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(vos.Weight.IncorrectAmountError):
        await register_user.perform(
            UUID(int=1),
            5000,
            300,
            -70,
            users=users,
            transaction_for=transaction_factory,
            logger=logger,
        )


@mark.asyncio
async def test_with_invalid_water_balance() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(vos.Water.IncorrectAmountError):
        await register_user.perform(
            UUID(int=1),
            -5000,
            300,
            70,
            users=users,
            transaction_for=transaction_factory,
            logger=logger,
        )


@mark.asyncio
async def test_storage_on_invalid_grass() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(vos.Water.Error):
        await register_user.perform(
            UUID(int=1),
            5000,
            -300,
            70,
            users=users,
            transaction_for=transaction_factory,
            logger=logger,
        )

    assert len(users) == 0


@mark.asyncio
async def test_storage_on_invalid_weight() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(vos.Weight.Error):
        await register_user.perform(
            UUID(int=1),
            5000,
            300,
            -70,
            users=users,
            transaction_for=transaction_factory,
            logger=logger,
        )

    assert len(users) == 0


@mark.asyncio
async def test_storage_on_invalid_water_balance() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(vos.Water.Error):
        await register_user.perform(
            UUID(int=1),
            -5000,
            300,
            70,
            users=users,
            transaction_for=transaction_factory,
            logger=logger,
        )

    assert len(users) == 0


@mark.asyncio
async def test_logger_on_invalid_grass() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(vos.Water.Error):
        await register_user.perform(
            UUID(int=1),
            5000,
            -300,
            70,
            users=users,
            transaction_for=transaction_factory,
            logger=logger,
        )

    assert logger.is_empty


@mark.asyncio
async def test_logger_on_invalid_weight() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(vos.Weight.Error):
        await register_user.perform(
            UUID(int=1),
            5000,
            300,
            -70,
            users=users,
            transaction_for=transaction_factory,
            logger=logger,
        )

    assert logger.is_empty


@mark.asyncio
async def test_logger_on_invalid_water_balance() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(vos.Water.Error):
        await register_user.perform(
            UUID(int=1),
            -5000,
            300,
            70,
            users=users,
            transaction_for=transaction_factory,
            logger=logger,
        )

    assert logger.is_empty


@mark.asyncio
async def test_result_without_glass() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()
    expected_user = entities.User(
        id=UUID(int=1),
        weight=vos.Weight(kilograms=70),
        glass=vos.Glass(capacity=vos.Water(milliliters=200)),
        _target=vos.WaterBalance(water=vos.Water(milliliters=5000)),
    )

    user = await register_user.perform(
        UUID(int=1),
        5000,
        None,
        70,
        users=users,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert user == expected_user


@mark.asyncio
async def test_result_without_weight() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()
    expected_user = entities.User(
        id=UUID(int=1),
        weight=None,
        glass=vos.Glass(capacity=vos.Water(milliliters=500)),
        _target=vos.WaterBalance(water=vos.Water(milliliters=5000)),
    )

    user = await register_user.perform(
        UUID(int=1),
        5000,
        500,
        None,
        users=users,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert user == expected_user


@mark.asyncio
async def test_result_without_water_balance() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()
    expected_user = entities.User(
        id=UUID(int=1),
        weight=vos.Weight(kilograms=70),
        glass=vos.Glass(capacity=vos.Water(milliliters=500)),
        _target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
    )

    user = await register_user.perform(
        UUID(int=1),
        None,
        500,
        70,
        users=users,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert user == expected_user


@mark.asyncio
async def test_storage_without_glass() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()
    expected_user = entities.User(
        id=UUID(int=1),
        weight=vos.Weight(kilograms=70),
        glass=vos.Glass(capacity=vos.Water(milliliters=200)),
        _target=vos.WaterBalance(water=vos.Water(milliliters=5000)),
    )

    await register_user.perform(
        UUID(int=1),
        5000,
        None,
        70,
        users=users,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert next(iter(users)) == expected_user


@mark.asyncio
async def test_storage_without_weight() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()
    expected_user = entities.User(
        id=UUID(int=1),
        weight=None,
        glass=vos.Glass(capacity=vos.Water(milliliters=500)),
        _target=vos.WaterBalance(water=vos.Water(milliliters=5000)),
    )

    await register_user.perform(
        UUID(int=1),
        5000,
        500,
        None,
        users=users,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert next(iter(users)) == expected_user


@mark.asyncio
async def test_storage_without_water_balance() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()
    expected_user = entities.User(
        id=UUID(int=1),
        weight=vos.Weight(kilograms=70),
        glass=vos.Glass(capacity=vos.Water(milliliters=500)),
        _target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
    )

    await register_user.perform(
        UUID(int=1),
        None,
        500,
        70,
        users=users,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert next(iter(users)) == expected_user


@mark.asyncio
async def test_storage_without_water_balance_and_weight() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(entities.User.NoWeightForSuitableWaterBalanceError):
        await register_user.perform(
            UUID(int=1),
            None,
            500,
            None,
            users=users,
            transaction_for=transaction_factory,
            logger=logger,
        )

    assert len(users) == 0


@mark.asyncio
async def test_logger_without_weight() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()
    expected_user = entities.User(
        id=UUID(int=1),
        weight=None,
        glass=vos.Glass(capacity=vos.Water(milliliters=500)),
        _target=vos.WaterBalance(water=vos.Water(milliliters=5000)),
    )

    await register_user.perform(
        UUID(int=1),
        5000,
        500,
        None,
        users=users,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert logger.registered_users[0] == expected_user


@mark.asyncio
async def test_logger_without_water_balance() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()
    expected_user = entities.User(
        id=UUID(int=1),
        weight=vos.Weight(kilograms=70),
        glass=vos.Glass(capacity=vos.Water(milliliters=500)),
        _target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
    )

    await register_user.perform(
        UUID(int=1),
        None,
        500,
        70,
        users=users,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert logger.registered_users[0] == expected_user


@mark.asyncio
async def test_logger_without_water_balance_and_weight() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(entities.User.NoWeightForSuitableWaterBalanceError):
        await register_user.perform(
            UUID(int=1),
            None,
            500,
            None,
            users=users,
            transaction_for=transaction_factory,
            logger=logger,
        )

    assert logger.is_empty


@mark.asyncio
async def test_result_on_registred_user_registration() -> None:
    registred_user = entities.User(
        id=UUID(int=1),
        weight=vos.Weight(kilograms=70),
        glass=vos.Glass(capacity=vos.Water(milliliters=500)),
        _target=vos.WaterBalance(water=vos.Water(milliliters=5000)),
    )
    users = adapters.repos.InMemoryUsers([registred_user])
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    user = await register_user.perform(
        UUID(int=1),
        None,
        500,
        70,
        users=users,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert user == registred_user


@mark.asyncio
async def test_storage_on_registred_user_registration() -> None:
    users = adapters.repos.InMemoryUsers([
        entities.User(
            id=UUID(int=1),
            weight=vos.Weight(kilograms=70),
            glass=vos.Glass(capacity=vos.Water(milliliters=500)),
            _target=vos.WaterBalance(water=vos.Water(milliliters=5000)),
        )
    ])
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    await register_user.perform(
        UUID(int=1),
        None,
        500,
        70,
        users=users,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert len(users) == 1


@mark.asyncio
async def test_logger_on_registred_user_registration() -> None:
    registred_user = entities.User(
        id=UUID(int=1),
        weight=vos.Weight(kilograms=70),
        glass=vos.Glass(capacity=vos.Water(milliliters=500)),
        _target=vos.WaterBalance(water=vos.Water(milliliters=5000)),
    )
    users = adapters.repos.InMemoryUsers([registred_user])
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    await register_user.perform(
        UUID(int=1),
        70,
        500,
        None,
        users=users,
        transaction_for=transaction_factory,
        logger=logger,
    )

    assert logger.before_registered_users[0] == registred_user


@mark.asyncio
async def test_storage_without_water_balance_with_extreme_weight() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(vos.WaterBalance.ExtremeWeightForSuitableWaterBalanceError):
        await register_user.perform(
            UUID(int=1),
            None,
            500,
            70_000,
            users=users,
            transaction_for=transaction_factory,
            logger=logger,
        )

    assert len(users) == 0


@mark.asyncio
async def test_logger_without_water_balance_with_extreme_weight() -> None:
    users = adapters.repos.InMemoryUsers()
    logger = adapters.loggers.InMemoryStorageLogger()
    transaction_factory = InMemoryUoWTransactionFactory()

    with raises(vos.WaterBalance.ExtremeWeightForSuitableWaterBalanceError):
        await register_user.perform(
            UUID(int=1),
            None,
            500,
            70_000,
            users=users,
            transaction_for=transaction_factory,
            logger=logger,
        )

    assert logger.is_empty
