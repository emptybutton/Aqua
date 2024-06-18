from datetime import datetime, UTC, date
from typing import Optional, Annotated
from uuid import UUID

from fastapi import APIRouter, Response, HTTPException, status, Header, Cookie
from pydantic import BaseModel

from src.aqua.presentation import facade as aqua
from src.auth.presentation import facade as auth
from src.entrypoint.presentation import cookies
from src.entrypoint.presentation.error_responses import (
    default_error_with, detail_of, detail_from, handle_base_errors
)
from src.entrypoint.presentation.facade import controllers
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
        result = await controllers.registration.register_user(
            request_model.username,
            request_model.password,
            request_model.water_balance_milliliters,
            request_model.glass_milliliters,
            request_model.weight_kilograms,
        )
    except auth.controllers.registration.UserIsAlreadyRegisteredError as error:
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
            result = await auth.controllers.authorization.authorize_user(
                request.username,
                request.password,
                session=session,
            )
        except auth.controllers.authorization.NoUserError as error:
            message = "there is no user with this name"
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail=detail_of(error, message=message),
            ) from error
        except auth.controllers.authorization.IncorrectPasswordError as error:
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
        result = auth.controllers.access_extension.extend_access(
            jwt,
            refresh_token,
            expiration_date,
        )
    except auth.controllers.access_extension.InvalidJWTError as error:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail=detail_of(error),
        ) from error
    except auth.controllers.access_extension.ExpiredRefreshTokenError as error:
        detail = detail_of(auth.controllers.access_extension.InvalidJWTError())
        new_error = HTTPException(status.HTTP_401_UNAUTHORIZED, detail=detail)

        raise new_error from error

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
        result = await controllers.writing.write_water(
            jwt,
            request.milliliters,
        )
    except aqua.controllers.writing.NoUserError as error:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=detail_of(error),
        ) from error

    return RecordCreationResponseModel(
        record_id=result.record_id,
        drunk_water_milliliters=result.drunk_water_milliliters,
    )


class DayReadingRequestModel(BaseModel):
    date_: date


class DayReadingResponseModel(BaseModel):
    target_water_balance: int
    real_water_balance: int
    result_code: int


@router.get("/user/day", tags=["days"])
@handle_base_errors
async def read_day(
    request: DayReadingRequestModel,
    jwt: Annotated[str, Header()],
) -> DayReadingResponseModel:
    try:
        result = await controllers.day_reading.read_day(jwt, request.date_)
    except aqua.controllers.day_reading.NoUserError as error:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=detail_of(error),
        ) from error

    return DayReadingResponseModel(
        target_water_balance=result.target_water_balance,
        real_water_balance=result.real_water_balance,
        result_code=result.result_code,
    )


class DayRecordsReadingRequestModel(BaseModel):
    date_: date


class DayRecordModel(BaseModel):
    id: UUID
    drunk_water: int
    recording_time: datetime

    @classmethod
    def of(
        cls,
        dto: controllers.day_record_reading.RecordDTO,
    ) -> "DayRecordModel":
        return cls(
            id=dto.id,
            drunk_water=dto.drunk_water,
            recording_time=dto.recording_time,
        )


class DayRecordsReadingResponseModel(BaseModel):
    records: tuple[DayRecordModel, ...]


@router.get("/user/day/records", tags=["records"])
@handle_base_errors
async def read_day_records(
    request: DayReadingRequestModel,
    jwt: Annotated[str, Header()],
) -> DayRecordsReadingResponseModel:
    try:
        result = await controllers.day_record_reading.read_day_records(
            jwt,
            request.date_,
        )
    except aqua.controllers.day_record_reading.NoUserError as error:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=detail_of(error),
        ) from error

    records = tuple(map(DayRecordModel.of, result.records))
    return DayRecordsReadingResponseModel(records=records)
