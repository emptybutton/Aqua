from uuid import UUID

from pytest import fixture

from aqua.domain.framework.entity import Entities
from aqua.domain.model.core.aggregates.user.root import User
from aqua.domain.model.core.vos.glass import Glass
from aqua.domain.model.core.vos.target import Target
from aqua.domain.model.core.vos.water_balance import (
    WaterBalance,
)
from aqua.domain.model.primitives.vos.water import Water
from aqua.domain.model.primitives.vos.weight import Weight
from aqua.infrastructure.periphery.pymongo.document import Document


@fixture
def user1() -> User:
    return User(
        id=UUID(int=1),
        events=list(),
        target=Target(
            water_balance=WaterBalance(
                water=Water.with_(milliliters=2000).unwrap()
            )
        ),
        glass=Glass(capacity=Water.with_(milliliters=200).unwrap()),
        weight=Weight.with_(kilograms=70).unwrap(),
        days=Entities(),
        records=Entities(),
    )


@fixture
def user1_document() -> Document:
    return {
        "_id": UUID(int=1),
        "target": 2000,
        "glass": 200,
        "weight": 70,
        "days": [],
        "records": [],
    }
