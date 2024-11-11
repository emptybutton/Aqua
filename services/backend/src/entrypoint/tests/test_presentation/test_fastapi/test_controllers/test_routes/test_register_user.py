from uuid import uuid4

from dirty_equals import IsUUID
from httpx import AsyncClient
from pytest import mark


@mark.parametrize("stage", ("json", "status_code"))
async def test_with_valid_data(stage: str, client: AsyncClient) -> None:
    username = uuid4().hex

    input_json = {
        "username": username,
        "password": "Ab345678",
        "weight_kilograms": 70,
    }
    output_json = {
        "user_id": IsUUID,
        "username": username,
        "target_water_balance_milliliters": 2000,
        "glass_milliliters": 200,
        "weight_kilograms": 70,
    }

    response = await client.post("/api/0.1v/user/register", json=input_json)

    if stage == "json":
        assert response.json() == output_json

    if stage == "status_code":
        assert response.status_code == 201


@mark.parametrize("stage", ("json", "status_code"))
async def test_with_invalid_target(stage: str, client: AsyncClient) -> None:
    username = uuid4().hex

    input_json = {
        "username": username,
        "password": "Ab345678",
        "target_water_balance_milliliters": -2000,
    }
    output_json = {
        "detail": [
            {
                "type": "InvalidWaterAmountError",
                "msg": "the amount of water should be >= 0",
            }
        ]
    }

    response = await client.post("/api/0.1v/user/register", json=input_json)

    if stage == "json":
        assert response.json() == output_json

    if stage == "status_code":
        assert response.status_code == 400
