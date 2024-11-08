from dataclasses import dataclass
from datetime import UTC, date, datetime
from typing import Awaitable, Callable, TypeAlias
from uuid import UUID

from pytest import fixture
from result import Result

from aqua.application.cases.write_water import (
    NoUserError,
)
from aqua.application.cases.write_water import (
    write_water as case,
)
from aqua.domain.framework.entity import Entities
from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import (
    User,
)
from aqua.domain.model.core.vos.glass import Glass
from aqua.domain.model.core.vos.target import Target
from aqua.domain.model.core.vos.water_balance import (
    WaterBalance,
)
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import (
    NegativeWaterAmountError,
    Water,
)
from aqua.domain.model.primitives.vos.weight import Weight
from aqua.infrastructure.adapters.loggers.in_memory_logger import (
    InMemoryLogger,
)
from aqua.infrastructure.adapters.mappers.in_memory.day_mapper import (
    InMemoryDayMapperTo,
)
from aqua.infrastructure.adapters.mappers.in_memory.record_mapper import (
    InMemoryRecordMapperTo,
)
from aqua.infrastructure.adapters.mappers.in_memory.user_mapper import (
    InMemoryUserMapperTo,
)
from aqua.infrastructure.adapters.repos.in_memory.users import InMemoryUsers
from aqua.infrastructure.adapters.transactions.in_memory import (
    storage_transaction as _storage_transaction,
)
from aqua.infrastructure.adapters.views.in_memory.writing_view_of import (
    InMemoryWritingViewOf,
)
from aqua.infrastructure.periphery.views.in_memory.writing_view import (
    InMemoryWritingView,
)


_InMemoryStorageTransactionFor: TypeAlias = (
    _storage_transaction.InMemoryStorageTransactionFor
)


type WriteWater = Callable[
    [UUID, int | None],
    Awaitable[
        Result[InMemoryWritingView, NoUserError | NegativeWaterAmountError]
    ],
]


@dataclass(kw_only=True, frozen=True, slots=True)
class Context:
    write_water: WriteWater
    users: InMemoryUsers
    logger: InMemoryLogger


@fixture
def context() -> Context:
    users = InMemoryUsers()
    logger = InMemoryLogger()

    async def write_water(
        user_id: UUID, water: int | None
    ) -> Result[InMemoryWritingView, NoUserError | NegativeWaterAmountError]:
        async with case(
            user_id,
            water,
            view_of=InMemoryWritingViewOf(),
            users=users,
            transaction_for=_InMemoryStorageTransactionFor(),
            logger=logger,
            user_mapper_to=InMemoryUserMapperTo(),
            day_mapper_to=InMemoryDayMapperTo(),
            record_mapper_to=InMemoryRecordMapperTo(),
        ) as result:
            return result

    return Context(write_water=write_water, users=users, logger=logger)


@fixture
def user1_day1() -> Day:
    return Day(
        id=UUID(int=10),
        events=list(),
        user_id=UUID(int=1),
        date_=date(2000, 1, 1),
        target=Target(
            water_balance=WaterBalance(
                water=Water.with_(milliliters=2000).unwrap()
            )
        ),
        water_balance=WaterBalance(water=Water.with_(milliliters=200).unwrap()),
        pinned_result=None,
    )


@fixture
def user1_day1_record1() -> Record:
    return Record(
        id=UUID(int=100),
        events=list(),
        user_id=UUID(int=1),
        drunk_water=Water.with_(milliliters=200).unwrap(),
        recording_time=(
            Time.with_(datetime_=datetime(2000, 1, 1, tzinfo=UTC)).unwrap()
        ),
        is_cancelled=False,
    )


@fixture
def user1_day2() -> Day:
    return Day(
        id=UUID(int=11),
        events=list(),
        user_id=UUID(int=1),
        date_=datetime.now(UTC).date(),
        target=Target(
            water_balance=WaterBalance(
                water=Water.with_(milliliters=1000).unwrap()
            )
        ),
        water_balance=WaterBalance(water=Water.with_(milliliters=650).unwrap()),
        pinned_result=None,
    )


@fixture
def user1_day2_record1() -> Record:
    return Record(
        id=UUID(int=101),
        events=list(),
        user_id=UUID(int=1),
        drunk_water=Water.with_(milliliters=500).unwrap(),
        recording_time=Time.with_(datetime_=datetime.now(UTC)).unwrap(),
        is_cancelled=False,
    )


@fixture
def user1_day2_record2() -> Record:
    return Record(
        id=UUID(int=102),
        events=list(),
        user_id=UUID(int=1),
        drunk_water=Water.with_(milliliters=150).unwrap(),
        recording_time=Time.with_(datetime_=datetime.now(UTC)).unwrap(),
        is_cancelled=False,
    )


@fixture
def user1(
    user1_day1: Day,
    user1_day1_record1: Record,
    user1_day2: Day,
    user1_day2_record1: Record,
    user1_day2_record2: Record,
) -> User:
    return User(
        id=UUID(int=1),
        events=list(),
        weight=Weight.with_(kilograms=70).unwrap(),
        target=Target(
            water_balance=WaterBalance(
                water=Water.with_(milliliters=1000).unwrap()
            )
        ),
        glass=Glass(capacity=Water.with_(milliliters=300).unwrap()),
        days=Entities([user1_day1, user1_day2]),
        records=Entities([
            user1_day1_record1,
            user1_day2_record1,
            user1_day2_record2,
        ]),
    )


@fixture
def user2() -> User:
    return User(
        id=UUID(int=2),
        events=list(),
        weight=Weight.with_(kilograms=70).unwrap(),
        target=Target(
            water_balance=WaterBalance(
                water=Water.with_(milliliters=2000).unwrap()
            )
        ),
        glass=Glass(capacity=Water.with_(milliliters=300).unwrap()),
        days=Entities(),
        records=Entities(),
    )


@fixture
def context_with_user1(  # noqa: PLR0917
    context: Context,
    user1: User,
    user1_day1: Day,
    user1_day1_record1: Record,
    user1_day2: Day,
    user1_day2_record1: Record,
    user1_day2_record2: Record,
) -> Context:
    context.users.add_user(user1)
    context.users.add_day(user1_day1)
    context.users.add_day(user1_day2)
    context.users.add_record(user1_day1_record1)
    context.users.add_record(user1_day2_record1)
    context.users.add_record(user1_day2_record2)

    return context


@fixture
def context_with_user2(context: Context, user2: User) -> Context:
    context.users.add_user(user2)

    return context
