from fastapi import APIRouter, Response
from pydantic import BaseModel

from entrypoint.presentation.di import facade
from entrypoint.presentation.periphery.api.views import (
    bodies,
    responses,
    cookies,
)


router = APIRouter(prefix="/api/0.1v")


class RegisterUserRequestModel(BaseModel):
    username: str
    password: str
    target_water_balance_milliliters: int | None = None
    glass_milliliters: int | None = None
    weight_kilograms: int | None = None


@router.post(
    "/user/register",
    tags=["access"],
    status_code=responses.ok.registered_user_view.status_code,
    responses=responses.common.to_doc(
        responses.bad.backend_is_not_working_view,
        responses.bad.incorrect_water_amount_view,
        responses.bad.incorrect_weight_amount_view,
        responses.bad.no_weight_for_water_balance_view,
        responses.bad.extreme_weight_for_water_balance_view,
        responses.bad.user_is_already_registered_view,
        responses.bad.empty_username_view,
        responses.bad.week_password_view,
        responses.ok.registered_user_view,
    ),
)
async def register_user(request_model: RegisterUserRequestModel) -> Response:
    result = await facade.register_user.perform(
        request_model.username,
        request_model.password,
        request_model.target_water_balance_milliliters,
        request_model.glass_milliliters,
        request_model.weight_kilograms,
    )

    if result == "not_working":
        return responses.bad.backend_is_not_working_view.to_response()

    if result == "incorrect_weight_amount":
        return responses.bad.incorrect_weight_amount_view.to_response()

    if result == "incorrect_water_amount":
        return responses.bad.incorrect_water_amount_view.to_response()

    if result == "extreme_weight_for_water_balance":
        return responses.bad.extreme_weight_for_water_balance_view.to_response()

    if result == "no_weight_for_water_balance":
        return responses.bad.no_weight_for_water_balance_view.to_response()

    if result == "user_is_already_registered":
        return responses.bad.user_is_already_registered_view.to_response()

    if result == "empty_username":
        return responses.bad.empty_username_view.to_response()

    if result == "week_password":
        return responses.bad.week_password_view.to_response()

    target = result.target_water_balance_milliliters
    body = bodies.ok.RegisteredUserView(
        user_id=result.user_id,
        username=result.username,
        target_water_balance_milliliters=target,
        glass_milliliters=result.glass_milliliters,
        weight_kilograms=result.weight_kilograms,
    )
    response = responses.ok.registered_user_view.to_response(body)

    jwt_cookie = cookies.JWTCookie(response)
    refresh_token_cookie = cookies.RefreshTokenCookie(response)

    jwt_cookie.set(result.jwt)
    refresh_token_cookie.set(
        result.refresh_token,
        result.refresh_token_expiration_date,
    )

    return response


"""
class AuthorizationRequestModel(BaseModel):
    username: str
    password: st


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


class DayReadingResponseModel(BaseModel):
    target_water_balance: int
    real_water_balance: int
    result_code: int


@router.get("/user/day", tags=["days"])
@handle_base_errors
async def read_day(
    date_: date,
    jwt: Annotated[str, Header()],
) -> DayReadingResponseModel:
    try:
        result = await controllers.day_reading.read_day(jwt, date_)
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


@router.get("/user/day/records", tags=["records"])
@handle_base_errors
async def read_day_records(
    date_: date,
    jwt: Annotated[str, Header()],
) -> DayRecordsReadingResponseModel:
    try:
        result = await controllers.day_record_reading.read_day_records(
            jwt, date_,
        )
    except aqua.controllers.day_record_reading.NoUserError as error:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=detail_of(error),
        ) from error

    records = tuple(map(DayRecordModel.of, result.records))
    return DayRecordsReadingResponseModel(records=records)


@router.get("/user", tags=["access"])
@handle_base_errors
async def read_user_data(
    jwt: Annotated[str, Header()],
) -> Optional[UserDataReadingResponseModel]:
    result = await controllers.user_data_reading.read_user_data(jwt)

    if result is None:
        return None

    water_balance = result.target_water_balance_milliliters

    return UserDataReadingResponseModel(
        user_id=result.user_id,
        username=result.username,
        glass_milliliters=result.glass_milliliters,
        target_water_balance_milliliters=water_balance,
        weight_kilograms=result.weight_kilograms,
    )
"""
