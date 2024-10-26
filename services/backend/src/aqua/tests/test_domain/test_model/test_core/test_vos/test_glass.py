from aqua.domain.model.core.vos.glass import Glass
from aqua.domain.model.primitives.vos.water import Water


def test_identity() -> None:
    water = Water.with_(milliliters=100).unwrap()

    assert Glass(capacity=water) == Glass(capacity=water)
