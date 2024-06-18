from datetime import datetime, UTC
from typing import Optional, Annotated
from uuid import UUID

from fastapi import APIRouter, Response, HTTPException, status, Header, Cookie
from pydantic import BaseModel

from src.aqua.presentation.adapters import writing as aqua_writing
from src.auth.presentation.adapters import (
    registration as auth_registration,
    authorization,
    access_extension,
)
from src.entrypoint.presentation import cookies
from src.entrypoint.presentation.error_responses import (
    default_error_with, detail_of, detail_from, handle_base_errors
)
from src.entrypoint.presentation.adapters import registration, writing
from src.shared.infrastructure.db.sessions import postgres_session_factory


router = APIRouter(prefix="/api/0.1v")


class UserRegistrationRequestModel(BaseModel):
    username: str
    password: str
    water_balance_milliliters: Optional[int] = None
    glass_milliliters: Optional[int] = None
    weight_kilograms: Optional[int] = None


class UserRegistrationResponseModel(BaseModel):
    jwt: str


@router.post("/user/register", tags=["access"])
@handle_base_errors
async def register_user(
    request_model: UserRegistrationRequestModel,
    response: Response,
) -> UserRegistrationResponseModel:
    try:
        result = await registration.register_user(
            request_model.username,
            request_model.password,
            request_model.water_balance_milliliters,
            request_model.glass_milliliters,
            request_model.weight_kilograms,
        )
    except auth_registration.UserIsAlreadyRegisteredError as error:
        raise default_error_with(detail_of(error)) from error

    cookies.set_refresh_token(
        response,
        result.refresh_token,
        result.refresh_token_expiration_date,
    )

    return UserRegistrationResponseModel(jwt=result.access_token)


class AuthorizationRequestModel(BaseModel):
    username: str
    password: str


class AuthorizationResponseModel(BaseModel):
    jwt: str


@router.post("/user/authorize", tags=["access"])
@handle_base_errors
async def authorize_user(
    request: AuthorizationRequestModel,
    response: Response
) -> AuthorizationResponseModel:
    async with postgres_session_factory() as session:
        try:
            result = await authorization.authorize_user(
                request.username,
                request.password,
                session=session,
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

    return AuthorizationResponseModel(jwt=result.jwt)


class AccessTokenRefreshingResponseModel(BaseModel):
    jwt: str


@router.post("/user/access-token", tags=["access"])
@handle_base_errors
async def refresh_access_token(
    refresh_token: Annotated[str, Cookie()],
    refresh_token_expiration_timestamp: Annotated[float, Cookie()],
    jwt: Annotated[str, Header()],
) -> AccessTokenRefreshingResponseModel:
    expiration_date = datetime.fromtimestamp(
        refresh_token_expiration_timestamp,
        UTC,
    )

    if expiration_date is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=detail_from(type_="InvalidRefreshTokenExpirationTimestamp"),
        )

    try:
        result = access_extension.extend_access(
            jwt,
            refresh_token,
            expiration_date,
        )
    except access_extension.InvalidJWTError as error:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail=detail_of(error),
        ) from error
    except access_extension.ExpiredRefreshTokenError as error:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail=detail_of(access_extension.InvalidJWTError()),
        ) from error

    return AccessTokenRefreshingResponseModel(jwt=result.jwt)


class RecordCreationRequestModel(BaseModel):
    milliliters: Optional[int] = None


class RecordCreationResponseModel(BaseModel):
    record_id: UUID
    drunk_water_milliliters: int


@router.post("/user/records", tags=["records"])
@handle_base_errors
async def create_record(
    request: RecordCreationRequestModel,
    jwt: Annotated[str, Header()],
) -> RecordCreationResponseModel:
    try:
        result = await writing.write_water(
            jwt,
            request.milliliters,
        )
    except aqua_writing.NoUserError as error:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=detail_of(error),
        ) from error

    return RecordCreationResponseModel(
        record_id=result.record_id,
        drunk_water_milliliters=result.drunk_water_milliliters,
    )
