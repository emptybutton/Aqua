from fastapi import HTTPException, status

from src.aqua.presentation import errors as aqua_errors
from src.auth.presentation import errors as auth_errors


def for_api(error: Exception) -> Exception:  # noqa: PLR0911
    if isinstance(error, aqua_errors.IncorrectWaterAmount):
        return HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="water milligrams must be > 0",
        )

    if isinstance(error, aqua_errors.IncorrectWeightAmount):
        return HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="weight killograms must be > 0",
        )

    if isinstance(error, aqua_errors.NoWeightForWaterBalance):
        return HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="weight is needed to calculate water balance",
        )

    if isinstance(error, aqua_errors.ExtremeWeightForWaterBalance):
        return HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="not normal weight for calculating water balance",
        )

    if isinstance(error, aqua_errors.NotUTCRecordingTime):
        return HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="recording time must be in UTC time zone",
        )

    if isinstance(error, auth_errors.EmptyUsername):
        return HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="username must not be empty",
        )

    if isinstance(error, auth_errors.WeekPassword):
        return HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=(
                "password must not contain only numbers or only letters, "
                "but must contain both upper and lower case letters and be 8 "
                "or more characters long"
            ),
        )

    if isinstance(
        error,
        aqua_errors.ValidationError | auth_errors.ValidationError,
    ):
        return HTTPException(status.HTTP_400_BAD_REQUEST)

    return error
