from typing import Optional

from src.entrypoint.presentation import cookies
from src.entrypoint.presentation.adapters import registration
from src.shared.infrastructure.db.engines import engine

from fastapi import APIRouter, Response
from pydantic import BaseModel


router = APIRouter()


class UserRegistrationResponseModel(BaseModel):
    user_id: int
    username: str
    access_token: str


@router.post("/register-user")
async def register_user(  # noqa: PLR0913
    response: Response,
    name: str,
    password: str,
    water_balance_milliliters: Optional[int],
    glass_milliliters: Optional[int],
    weight_kilograms: Optional[int],
) -> UserRegistrationResponseModel:
    result = await registration.register_user(
        name,
        password,
        water_balance_milliliters,
        glass_milliliters,
        weight_kilograms,
        engine=engine,
    )

    cookies.set_refresh_token(
        response,
        result.refresh_token,
        result.refresh_token_expiration_date,
    )

    return UserRegistrationResponseModel(
        user_id=result.user_id,
        username=result.username,
        access_token=result.access_token,
    )
