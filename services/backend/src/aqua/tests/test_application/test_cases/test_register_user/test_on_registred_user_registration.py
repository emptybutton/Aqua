from uuid import UUID

from pytest import fixture, mark
from result import Ok

from aqua.domain.framework.entity import Entities
from aqua.domain.model.core.aggregates.user.root import (
    User,
)
from aqua.domain.model.core.vos.glass import Glass
from aqua.domain.model.core.vos.target import Target
from aqua.domain.model.core.vos.water_balance import (
    WaterBalance,
)
from aqua.domain.model.primitives.vos.water import Water
from aqua.domain.model.primitives.vos.weight import Weight
from aqua.infrastructure.periphery.logs.in_memory_logs import (
    RegisteredUserRegistrationLog,
)
from aqua.infrastructure.periphery.views.in_memory.registration_view import (
    InMemoryRegistrationView,
)
from aqua.tests.test_application.test_cases.test_register_user.conftest import (
    Context,
)


@fixture
def stored_user() -> User:
    return User(
        id=UUID(int=1),
        events=list(),
        weight=Weight.with_(kilograms=70).unwrap(),
        target=Target(
            water_balance=WaterBalance(
                water=Water.with_(milliliters=5000).unwrap()
            )
        ),
        glass=Glass(capacity=Water.with_(milliliters=300).unwrap()),
        days=Entities(),
        records=Entities(),
    )


@fixture
def active_context(context: Context, stored_user: User) -> Context:
    context.users.add_user(stored_user)

    return context


@mark.asyncio
async def test_result(active_context: Context, stored_user: User) -> None:
    result = await active_context.register_user(UUID(int=1), 2000, 220, 100)

    assert result == Ok(InMemoryRegistrationView(user=stored_user))


@mark.asyncio
async def test_storage(active_context: Context, stored_user: User) -> None:
    await active_context.register_user(UUID(int=1), 2000, 220, 100)

    assert list(active_context.users) == [stored_user]


@mark.asyncio
async def test_logs(active_context: Context, stored_user: User) -> None:
    await active_context.register_user(UUID(int=1), 2000, 220, 100)

    log = RegisteredUserRegistrationLog(user=stored_user)

    assert active_context.logger.registred_user_logs == tuple()
    assert active_context.logger.registered_user_registration_logs == (log, )
    assert active_context.logger.record_without_day_logs == tuple()
    assert active_context.logger.new_day_logs == tuple()
    assert active_context.logger.new_day_state_logs == tuple()
    assert active_context.logger.new_record_logs == tuple()
    assert active_context.logger.record_cancellation_logs == tuple()
