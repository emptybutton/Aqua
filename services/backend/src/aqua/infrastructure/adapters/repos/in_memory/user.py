from copy import deepcopy
from datetime import date
from uuid import UUID

from aqua.application.ports.repos import Users
from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import User
from aqua.infrastructure.periphery.storages.in_memory.user import (
    InMemoryUserStorage,
)
from shared.infrastructure.periphery.containers import TransactionalContainer


class InMemoryUsers(Users, TransactionalContainer[InMemoryUserStorage]):
    def __init__(self, storage: InMemoryUserStorage | None = None) -> None:
        super().__init__()
        self._storage = (
            InMemoryUserStorage() if storage is None else deepcopy(storage)
        )

    async def user_with_id(self, user_id: UUID) -> User | None:
        root = self._storage.user_with_id(user_id)

        if root is None:
            return None

        days = set(self._storage.days_with_user_id(user_id))
        records = set(self._storage.records_with_user_id(user_id))

        return User(
            id=root.id,
            weight=root.weight,
            glass=root.glass,
            target=root.target,
            events=list(),
            days=days,
            records=records,
        )

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
