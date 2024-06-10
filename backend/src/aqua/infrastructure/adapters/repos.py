from typing import Optional

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncConnection

from src.aqua.application.ports import repos
from src.aqua.domain import entities, value_objects
from src.shared.infrastructure.db import tables


class Users(repos.Users):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection

    async def add(self, user: entities.User) -> None:
        water_balance = user.water_balance.water.milliliters
        weight = None
        glass = None

        if user.weight is not None:
            weight = user.weight.kilograms

        if user.glass is not None:
            glass = user.glass.capacity.milliliters

        stmt = insert(tables.AquaUser).values(
            id=user.id,
            water_balance=water_balance,
            weight=weight,
            glass=glass,
        )

        await self.__connection.execute(stmt)

    async def get_by_id(self, user_id: int) -> Optional[entities.User]:
        query = (
            select(
                tables.AquaUser.id,
                tables.AquaUser.water_balance,
                tables.AquaUser.glass,
                tables.AquaUser.weight,
            )
            .where(tables.AquaUser.id == user_id)
        )
        results = await self.__connection.execute(query)
        raw_user = results.first()

        if raw_user is None:
            return None

        if raw_user.glass is None:
            glass = None
        else:
            glass = value_objects.Glass(value_objects.Water(raw_user.glass))

        if raw_user.weight is None:
            weight = None
        else:
            weight = value_objects.Weight(raw_user.weight)

        water_balance = value_objects.WaterBalance(
            value_objects.Water(raw_user.water_balance)
        )

        return entities.User(
            weight=weight,
            glass=glass,
            __water_balance=water_balance,
            id=raw_user.id,
        )

class Records(repos.Records):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection

    async def add(self, record: entities.Record) -> None:
        stmt = insert(tables.Record).values(
            id=record.id,
            drunk_water=record.drunk_water.milliliters,
            recording_time=record.recording_time,
            user_id=record.user_id,
        )

        await self.__connection.execute(stmt)
