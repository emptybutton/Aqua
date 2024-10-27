from uuid import UUID

from pytest import fixture, mark
from result import Ok

from aqua.domain.framework.entity import Entities
from aqua.domain.model.access.entities.user import User as AccessUser
from aqua.domain.model.core.aggregates.user.root import (
    TranslatedFromAccess,
    User,
)
from aqua.domain.model.core.vos.glass import Glass
from aqua.domain.model.core.vos.target import Target
from aqua.domain.model.core.vos.water_balance import (
    WaterBalance,
)
from aqua.domain.model.primitives.vos.water import Water
from aqua.domain.model.primitives.vos.weight import Weight
from aqua.infrastructure.periphery.logs.in_memory_logs import RegistredUserLog
from aqua.infrastructure.periphery.views.in_memory.registration_view import (
    InMemoryRegistrationView,
)
from aqua.tests.test_application.test_cases.test_register_user.conftest import (
    Context,
)


@fixture
def expected_user() -> User:
    user = User(
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
    access_user = AccessUser(id=UUID(int=1), events=list())
    user.events.append(TranslatedFromAccess(entity=user, from_=access_user))

    return user


@mark.asyncio
async def test_result(context: Context, expected_user: User) -> None:
    result = await context.register_user(UUID(int=1), 5000, 300, 70)

    assert result == Ok(InMemoryRegistrationView(user=expected_user))


@mark.asyncio
async def test_storage(context: Context, expected_user: User) -> None:
    await context.register_user(UUID(int=1), 5000, 300, 70)

    assert list(context.users) == [expected_user]


@mark.asyncio
async def test_logs(context: Context, expected_user: User) -> None:
    await context.register_user(UUID(int=1), 5000, 300, 70)

    log = RegistredUserLog(user=expected_user)

    assert context.logger.registred_user_logs == (log,)
    assert context.logger.registered_user_registration_logs == tuple()
    assert context.logger.record_without_day_logs == tuple()
    assert context.logger.new_day_logs == tuple()
    assert context.logger.new_day_state_logs == tuple()
    assert context.logger.new_record_logs == tuple()
    assert context.logger.record_cancellation_logs == tuple()
