from dataclasses import dataclass
from functools import partial
from typing import Awaitable, Callable, TypeAlias
from uuid import UUID

from pytest import fixture
from result import Result

from aqua.application.cases.register_user import (
    NegativeGlassMillilitersError,
    NegativeTargetWaterBalanceMillilitersError,
    NegativeWeightKilogramsError,
)
from aqua.application.cases.register_user import (
    register_user as case,
)
from aqua.domain.model.core.aggregates.user.root import (
    NoWeightForSuitableWaterBalanceError,
)
from aqua.domain.model.core.vos.water_balance import (
    ExtremeWeightForSuitableWaterBalanceError,
)
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
from aqua.infrastructure.adapters.views.in_memory.registration_view_of import (
    InMemoryRegistrationViewOf,
)
from aqua.infrastructure.periphery.views.in_memory.registration_view import (
    InMemoryRegistrationView,
)


_InMemoryStorageTransactionFor: TypeAlias = (
    _storage_transaction.InMemoryStorageTransactionFor
)


type RegisterUser = Callable[
    [UUID, int | None, int | None, int | None],
    Awaitable[
        Result[
            InMemoryRegistrationView,
            (
                ExtremeWeightForSuitableWaterBalanceError
                | NoWeightForSuitableWaterBalanceError
                | NegativeTargetWaterBalanceMillilitersError
                | NegativeGlassMillilitersError
                | NegativeWeightKilogramsError
            ),
        ]
    ],
]


@dataclass(kw_only=True, frozen=True, slots=True)
class Context:
    register_user: RegisterUser
    users: InMemoryUsers
    logger: InMemoryLogger


@fixture
def context() -> Context:
    users = InMemoryUsers()
    logger = InMemoryLogger()

    register_user: RegisterUser = partial(
        case,
        view_of=InMemoryRegistrationViewOf(),
        users=users,
        transaction_for=_InMemoryStorageTransactionFor(),
        logger=logger,
        user_mapper_to=InMemoryUserMapperTo(),
        day_mapper_to=InMemoryDayMapperTo(),
        record_mapper_to=InMemoryRecordMapperTo(),
    )

    return Context(register_user=register_user, users=users, logger=logger)
