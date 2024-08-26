from datetime import datetime, UTC
from uuid import uuid4

from pytest import fixture

from aqua.domain import entities, value_objects as vos


@fixture
def user1() -> entities.User:
    return entities.User(
        id=uuid4(),
        weight=vos.Weight(kilograms=70),
        glass=vos.Glass(capacity=vos.Water(milliliters=300)),
    )


@fixture
def user1_empty_day(user1: entities.User) -> entities.Day:
    return entities.Day.empty_of(user1, date_=datetime.now(UTC).date())


@fixture
def user1_record1(user1: entities.User) -> entities.Record:
    return entities.Record(
        user_id=user1.id,
        drunk_water=vos.Water(milliliters=700),
    )


@fixture
def user1_record1_day(
    user1: entities.User,
    user1_record1: entities.Record
) -> entities.Day:
    day = entities.Day.empty_of(user1, date_=datetime.now(UTC).date())
    day.add(user1_record1)

    return day


@fixture
def record1() -> entities.Record:
    return entities.Record(
        user_id=uuid4(),
        drunk_water=vos.Water(milliliters=10_000),
        _recording_time=datetime(2006, 1, 1, tzinfo=UTC)
    )
