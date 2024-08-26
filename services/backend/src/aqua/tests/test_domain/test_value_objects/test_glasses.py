from aqua.domain import value_objects as vos


def test_identity() -> None:
    water = vos.Water(milliliters=100)

    assert vos.Glass(capacity=water) == vos.Glass(capacity=water)
