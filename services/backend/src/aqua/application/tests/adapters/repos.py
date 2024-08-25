from datetime import date
from copy import copy
from uuid import UUID

from aqua.application.ports import repos
from aqua.domain import entities
from shared.application.tests.periphery import uows


class InMemoryUsers(repos.Users, uows.InMemoryUoW[entities.User]):
    async def add(self, user: entities.User) -> None:
        self._storage.append(copy(user))

    async def find_with_id(self, user_id: UUID) -> entities.User | None:
        for user in self._storage:
            if user.id == user_id:
                return copy(user)

        return None

    async def contains_with_id(self, user_id: UUID) -> bool:
        return any(user.id == user_id for user in self._storage)


class InMemoryRecords(repos.Records, uows.InMemoryUoW[entities.Record]):
    async def add(self, record: entities.Record) -> None:
        self._storage.append(copy(record))

    async def find_from(
        self,
        date_: date,
        *,
        user_id: UUID,
    ) -> tuple[entities.Record, ...]:
        found_records = list()

        for record in self._storage:
            recording_date = record.recording_time.date()
            if record.user_id == user_id and recording_date == date_:
                found_records.append(copy(record))

        return tuple(found_records)


class InMemoryDays(repos.Days, uows.InMemoryUoW[entities.Day]):
    async def add(self, day: entities.Day) -> None:
        self._storage.append(copy(day))

    async def find_from(
        self,
        date_: date,
        *,
        user_id: UUID,
    ) -> entities.Day | None:
        for day in self._storage:
            if day.date_ == date_ and day.user_id == user_id:
                return day

        return None

    async def update(self, day: entities.Day) -> None:
        for stored_day in self._storage:
            if day == stored_day:
                self._storage.remove(stored_day)
                self._storage.append(day)
                break
