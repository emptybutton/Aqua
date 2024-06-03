from typing import Optional

from sqlalchemy import Connection, select, insert

from src.aqua.application.ports import repos
from src.aqua.domain import entities, value_objects
from src.shared.infrastructure.db import tables


class Users(repos.Users):
    def __init__(self, connection: Connection) -> None:
        self.__connection = connection

    def add(self, user: entities.User) -> None:
        water_balance = user.water_balance.milligrams
        weight = None
        glass = None

        if user.weight is not None:
            weight = user.weight.kilograms

        if user.glass is not None:
            glass = user.glass.milligrams

        stmt = insert(tables.AquaUser).values(
            id=user.id,
            water_balance=water_balance,
            weight=weight,
            glass=glass,
        )

        self.__connection.execute(stmt)

    def get_by_id(self, user_id: int) -> Optional[entities.User]:
        query = (
            select(
                tables.AquaUser.id,
                tables.AquaUser.water_balance,
                tables.AquaUser.glass,
                tables.AquaUser.weight,
            )
            .where(tables.AquaUser.id == user_id)
        )

        raw_user = self.__connection.execute(query).first()

        if raw_user is None:
            return None

        return entities.User(
            value_objects.Weight(raw_user.weight),
            value_objects.Water(raw_user.glass),
            value_objects.Water(raw_user.water_balance),
            raw_user.id,
        )


class Records(repos.Records):
    def __init__(self, connection: Connection) -> None:
        self.__connection = connection

    def add(self, record: entities.Record) -> None:
        stmt = insert(tables.Record).values(
            id=record.id,
            drunk_water=record.drunk_water.milligrams,
            recording_time=record.recording_time,
            user_id=record.user_id,
        )

        self.__connection.execute(stmt)
