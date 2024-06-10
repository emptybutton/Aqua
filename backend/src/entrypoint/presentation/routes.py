from typing import Optional

from src.entrypoint.presentation import cookies
from src.entrypoint.presentation.error_responses import (
    default_error_with, detail_of
)
from src.entrypoint.presentation.adapters import registration
from src.auth.presentation.adapters import (
    registration as auth_registration,
    authorization,
)
from src.shared.infrastructure.db.engines import engine

from fastapi import APIRouter, Response, HTTPException, status
from pydantic import BaseModel


router = APIRouter(prefix="/api/0.1v")


class UserRegistrationRequestModel(BaseModel):
    name: str
    password: str
    water_balance_milliliters: Optional[int] = None
    glass_milliliters: Optional[int] = None
    weight_kilograms: Optional[int] = None


class UserRegistrationResponseModel(BaseModel):
    user_id: int
    username: str
    access_token: str


@router.post("/user/register", tags=["access"])
async def register_user(
    request_model: UserRegistrationRequestModel,
    response: Response,
) -> UserRegistrationResponseModel:
    try:
        result = await registration.register_user(
            request_model.name,
            request_model.password,
            request_model.water_balance_milliliters,
            request_model.glass_milliliters,
            request_model.weight_kilograms,
            engine=engine,
        )
    except auth_registration.UserIsAlreadyRegisteredError as error:
        raise default_error_with(detail_of(error)) from error

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


class AuthorizationRequestModel(BaseModel):
    username: str
    password: str


class AuthorizationResponseModel(BaseModel):
    user_id: int
    username: str
    jwt: str


@router.post("/user/authorize", tags=["access"])
async def authorize_user(
    request: AuthorizationRequestModel,
    response: Response
) -> AuthorizationResponseModel:
    async with engine.connect() as connection:
        try:
            result = await authorization.authorize_user(
                request.username,
                request.password,
                connection=connection,
            )
        except authorization.NoUserError as error:
            message = "there is no user with this name"
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail=detail_of(error, message=message),
            ) from error
        except authorization.IncorrectPasswordError as error:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail=detail_of(error),
            ) from error

    cookies.set_refresh_token(
        response,
        result.refresh_token,
        result.refresh_token_expiration_date,
    )

    return AuthorizationResponseModel(
        user_id=result.user_id,
        username=result.username,
        jwt=result.jwt,
    )
