from typing import TypeAlias

from pydantic import BaseModel


class _DetailPart(BaseModel):
    msg: str
    type: str


_Detail: TypeAlias = tuple[_DetailPart, ...]


def _detail_with(type_: str, message: str = str()) -> _Detail:
    main_part = _DetailPart(msg=message, type=type_)
    return (main_part,)


class BackendIsNotWorkingView(BaseModel):
    detail: _Detail = _detail_with(
        type_="BackendIsNotWorkingError", message="need to try after some time"
    )


class WeekPasswordView(BaseModel):
    detail: _Detail = _detail_with(
        type_="WeekPasswordError",
        message=(
            "password must not contain only numbers or only letters, "
            "but must contain both upper and lower case letters and be 8 "
            "or more characters long"
        ),
    )


class InvalidJWTView(BaseModel):
    detail: _Detail = _detail_with(type_="InvalidJWTError")


class ExpiredJWTView(BaseModel):
    detail: _Detail = _detail_with(type_="ExpiredJWTError")


class NoUserView(BaseModel):
    detail: _Detail = _detail_with(type_="NoUserError")


class IncorrectPasswordView(BaseModel):
    detail: _Detail = _detail_with(type_="IncorrectPasswordError")


class NotUTCRefreshTokenExpirationDateView(BaseModel):
    detail: _Detail = _detail_with(
        type_="NotUTCRefreshTokenExpirationDateError"
    )


class ExpiredRefreshTokenView(BaseModel):
    detail: _Detail = _detail_with(type_="ExpiredRefreshTokenError")


class IncorrectWaterAmountView(BaseModel):
    detail: _Detail = _detail_with(
        type_="IncorrectWaterAmountError",
        message="the amount of water should be >= 0",
    )


class IncorrectWeightAmountView(BaseModel):
    detail: _Detail = _detail_with(
        type_="IncorrectWeightAmountError",
        message="weight kilograms should be >= 0",
    )


class NoWeightForWaterBalanceView(BaseModel):
    detail: _Detail = _detail_with(
        type_="NoWeightForWaterBalanceError",
        message="weight is required if water balance is not specified",
    )


class ExtremeWeightForWaterBalanceView(BaseModel):
    detail: _Detail = _detail_with(
        type_="ExtremeWeightForWaterBalanceError",
        message=(
            "weight must be between 30 and 150 kg inclusive to"
            " calculate water balance"
        ),
    )


class EmptyUsernameView(BaseModel):
    detail: _Detail = _detail_with(type_="EmptyUsernameError")


class UserIsAlreadyRegisteredView(BaseModel):
    detail: _Detail = _detail_with(type_="UserIsAlreadyRegisteredError")
