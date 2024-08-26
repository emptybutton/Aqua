from datetime import date
from copy import copy
from typing import Any
from uuid import UUID

from sqlalchemy import insert, exists, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.ports import repos
from aqua.domain import entities, value_objects as vos
from shared.infrastructure.periphery import uows
from shared.infrastructure.periphery.db import tables
from shared.infrastructure.periphery.db.stmt_builders import STMTBuilder


class DBUsers(repos.Users):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session
        self.__builder = STMTBuilder.of(session)

    async def add(self, user: entities.User) -> None:
        water_balance = user.target.water.milliliters
        weight = None
        glass = None

        if user.weight is not None:
            weight = user.weight.kilograms

        if user.glass is not None:
            glass = user.glass.capacity.milliliters

        await self.__session.execute(
            insert(tables.AquaUser).values(
                id=user.id,
                water_balance=water_balance,
                weight=weight,
                glass=glass,
            )
        )

    async def find_with_id(self, user_id: UUID) -> entities.User | None:
        query = (
            self.__builder.select(
                tables.AquaUser.id,
                tables.AquaUser.water_balance,
                tables.AquaUser.glass,
                tables.AquaUser.weight,
            )
            .build()
            .where(tables.AquaUser.id == user_id)
        )
        results = await self.__session.execute(query)
        raw_user = results.first()

        if raw_user is None:
            return None

        glass = vos.Glass(capacity=vos.Water(milliliters=raw_user.glass))
        weight = (
            None
            if raw_user.weight is None
            else vos.Weight(kilograms=raw_user.weight)
        )

        target = vos.WaterBalance(
            water=vos.Water(milliliters=raw_user.water_balance)
        )

        return entities.User(
            id=raw_user.id,
            weight=weight,
            glass=glass,
            _target=target,
        )

    async def contains_with_id(self, user_id: UUID) -> bool:
        query = self.__builder.select(
            exists(1).where(tables.AquaUser.id == user_id)
        ).build()

        result = await self.__session.scalar(query)
        return bool(result)


class DBRecords(repos.Records):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session
        self.__builder = STMTBuilder.of(session)

    async def add(self, record: entities.Record) -> None:
        await self.__session.execute(
            insert(tables.Record).values(
                id=record.id,
                drunk_water=record.drunk_water.milliliters,
                recording_time=record.recording_time,
                user_id=record.user_id,
            )
        )

    async def find_from(
        self,
        date_: date,
        *,
        user_id: UUID,
    ) -> tuple[entities.Record, ...]:
        query = (
            self.__builder.select(
                tables.Record.id,
                tables.Record.drunk_water,
                tables.Record.recording_time,
            )
            .build()
            .where(
                (tables.Record.user_id == user_id)
                & (func.date(tables.Record.recording_time) == date_)
            )
        )

        results = await self.__session.execute(query)

        return tuple(self.__record_of(data, user_id) for data in results.all())

    def __record_of(
        self,
        record_data: Any,  # noqa: ANN401
        user_id: UUID,
    ) -> entities.Record:
        return entities.Record(
            id=record_data.id,
            user_id=user_id,
            drunk_water=vos.Water(milliliters=record_data.drunk_water),
            _recording_time=record_data.recording_time,
        )


class DBDays(repos.Days):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session
        self.__builder = STMTBuilder.of(session)

    async def add(self, day: entities.Day) -> None:
        await self.__session.execute(
            insert(tables.Day).values(
                id=day.id,
                user_id=day.user_id,
                real_water_balance=day.water_balance.water.milliliters,
                target_water_balance=day.target.water.milliliters,
                date_=day.date_,
                result=day.result.value,
            )
        )

    async def find_from(
        self,
        date_: date,
        *,
        user_id: UUID,
    ) -> entities.Day | None:
        query = (
            self.__builder.select(
                tables.Day.id,
                tables.Day.real_water_balance,
                tables.Day.target_water_balance,
                tables.Day.date_,
                tables.Day.result,
                tables.Day.is_result_pinned,
            )
            .build()
            .where(
                (tables.Day.date_ == date_) & (tables.Day.user_id == user_id)
            )
            .limit(1)
        )

        results = await self.__session.execute(query)
        raw_data = results.first()

        if raw_data is None:
            return None

        return self.__day_of(raw_data, user_id, date_)

    async def update(self, day: entities.Day) -> None:
        await self.__session.execute(
            update(tables.Day)
            .where(tables.Day.id == day.id)
            .values(
                user_id=day.user_id,
                real_water_balance=day.water_balance.water.milliliters,
                target_water_balance=day.target.water.milliliters,
                date_=day.date_,
                result=day.result.value,
                is_result_pinned=day.is_result_pinned,
            )
        )

    def __day_of(
        self,
        raw_data: Any,  # noqa: ANN401
        user_id: UUID,
        date_: date,
    ) -> entities.Day:
        target = vos.WaterBalance(
            water=vos.Water(
                milliliters=raw_data.target_water_balance,
            )
        )
        water_balance = vos.WaterBalance(
            water=vos.Water(
                milliliters=raw_data.real_water_balance,
            )
        )
        result = vos.WaterBalance.Status(raw_data.result)
        is_result_pinned = raw_data.is_result_pinned

        if is_result_pinned is None:
            is_result_pinned = False

        return entities.Day(
            id=raw_data.id,
            user_id=user_id,
            date_=date_,
            target=target,
            _water_balance=water_balance,
            _result=result,
            _is_result_pinned=is_result_pinned,
        )


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
            if day.id == stored_day.id:
                self._storage.remove(stored_day)
                self._storage.append(day)
                break
