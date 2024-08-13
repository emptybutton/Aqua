from typing import ClassVar, TypedDict, TypeAlias

from fastapi import status

from entrypoint.presentation.periphery.api.views.common import View


class _DetailBody(TypedDict):
    msg: str
    type: str


_Detail: TypeAlias = list[_DetailBody]


def _detail_of(type_: str, message: str = str()) -> _Detail:
    return [
        {
            "msg": message,
            "type": type_,
        }
    ]


class BackendIsNotWorkingView(View):
    status_code: ClassVar[int] = status.HTTP_400_BAD_REQUEST

    detail = _detail_of(
        type_="BackendIsNotWorkingError",
        message="need to try after some time",
    )


class WeekPasswordView(View):
    status_code: ClassVar[int] = status.HTTP_500_INTERNAL_SERVER_ERROR

    detail = _detail_of(
        type_="WeekPasswordError",
        message=(
            "password must not contain only numbers or only letters, "
            "but must contain both upper and lower case letters and be 8 "
            "or more characters long"
        ),
    )


class InvalidJWTView(View):
    status_code: ClassVar[int] = status.HTTP_401_UNAUTHORIZED

    detail = _detail_of(type_="InvalidJWTError")


class ExpiredJWTView(View):
    status_code: ClassVar[int] = status.HTTP_401_UNAUTHORIZED

    detail = _detail_of(type_="ExpiredJWTError")


class NoUserView(View):
    status_code: ClassVar[int] = status.HTTP_404_NOT_FOUND

    detail = _detail_of(type_="NoUserError")


class IncorrectPasswordView(View):
    status_code: ClassVar[int] = status.HTTP_401_UNAUTHORIZED

    detail = _detail_of(type_="IncorrectPasswordError")


class NotUTCRefreshTokenExpirationDateView(View):
    status_code: ClassVar[int] = status.HTTP_401_UNAUTHORIZED

    detail = _detail_of(type_="NotUTCRefreshTokenExpirationDateError")


class ExpiredRefreshTokenView(View):
    status_code: ClassVar[int] = status.HTTP_401_UNAUTHORIZED

    detail = _detail_of(type_="ExpiredRefreshTokenError")


class IncorrectWaterAmountView(View):
    status_code: ClassVar[int] = status.HTTP_400_BAD_REQUEST

    detail = _detail_of(
        type_="IncorrectWaterAmountError",
        message="the amount of water should be >= 0",
    )


class IncorrectWeightAmountView(View):
    status_code: ClassVar[int] = status.HTTP_400_BAD_REQUEST

    detail = _detail_of(
        type_="IncorrectWeightAmountError",
        message="weight kilograms should be >= 0",
    )


class IncorrectWeightAmountView(View):
    status_code: ClassVar[int] = status.HTTP_400_BAD_REQUEST

    detail = _detail_of(
        type_="IncorrectWeightAmountError",
        message="weight kilograms should be >= 0",
    )


class NoWeightForWaterBalanceView(View):
    status_code: ClassVar[int] = status.HTTP_400_BAD_REQUEST

    detail = _detail_of(
        type_="NoWeightForWaterBalanceError",
        message="weight is required if water balance is not specified",
    )


class ExtremeWeightForWaterBalanceView(View):
    status_code: ClassVar[int] = status.HTTP_400_BAD_REQUEST

    detail = _detail_of(
        type_="ExtremeWeightForWaterBalanceError",
        message=(
            "weight must be between 30 and 150 kg (not inclusive) to"
            " calculate water balance"
        ),
    )


class EmptyUsernameView(View):
    status_code: ClassVar[int] = status.HTTP_400_BAD_REQUEST

    detail = _detail_of(type_="EmptyUsernameError")


class UserIsAlreadyRegisteredView(View):
    status_code: ClassVar[int] = status.HTTP_409_CONFLICT

    detail = _detail_of(type_="UserIsAlreadyRegisteredError")
