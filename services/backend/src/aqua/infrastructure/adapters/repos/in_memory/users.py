from copy import deepcopy
from datetime import date
from typing import Iterator
from uuid import UUID

from aqua.application.ports.repos import Users
from aqua.domain.framework.entity import Entities
from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import User
from aqua.infrastructure.periphery.storages import (
    transactional_storage as _transactional_storage,
)
from aqua.infrastructure.periphery.storages.user_storage import (
    InMemoryUserStorage,
)


class InMemoryUsers(
    Users,
    _transactional_storage.TransactionalInMemoryStorage[InMemoryUserStorage],
):
    def __init__(self, storage: InMemoryUserStorage | None = None) -> None:
        super().__init__()
        self._storage = (
            InMemoryUserStorage() if storage is None else deepcopy(storage)
        )

    def __iter__(self) -> Iterator[User]:
        return map(self.__with_aggregation, self._storage.users)

    def __bool__(self) -> bool:
        return bool(
            self._storage.users or self._storage.days or self._storage.records
        )

    async def user_with_id(self, user_id: UUID) -> User | None:
        root = self._storage.user_with_id(user_id)

        return None if root is None else self.__with_aggregation(root)

    def day_with_user_id_and_date(
        self, *, user_id: UUID, date_: date
    ) -> Day | None:
        return self._storage.day_with_user_id_and_date(
            user_id=user_id, date_=date_
        )

    def add_user(self, user: User) -> None:
        self._storage.add_user(user)

    def add_day(self, day: Day) -> None:
        self._storage.add_day(day)

    def add_record(self, record: Record) -> None:
        self._storage.add_record(record)

    def update_user(self, user: User) -> None:
        self._storage.update_user(user)

    def update_day(self, day: Day) -> None:
        self._storage.update_day(day)

    def update_record(self, record: Record) -> None:
        self._storage.update_record(record)

    def __with_aggregation(self, root: User) -> User:
        days = Entities(self._storage.days_with_user_id(root.id))
        records = Entities(self._storage.records_with_user_id(root.id))

        return User(
            id=root.id,
            weight=root.weight,
            glass=root.glass,
            target=root.target,
            events=root.events,
            days=days,
            records=records,
        )
