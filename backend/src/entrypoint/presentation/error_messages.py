from fastapi import HTTPException, status

from src.aqua.presentation import errors as aqua_errors
# from src.aqua.presentation.adapters import writing as aqua_writing  # noqa: ERA001, E501
# from src.auth.presentation import errors as auth_errors  # noqa: ERA001
# from src.auth.presentation.adapters import authentication as auth_authentication  # noqa: ERA001, E501
# from src.auth.presentation.adapters import authorization as auth_authorization  # noqa: ERA001, E501
# from src.auth.presentation.adapters import registration as auth_registration  # noqa: ERA001, E501


def for_api(error: Exception) -> Exception:  # noqa: PLR0911
    if isinstance(error, aqua_errors.NoWater):
        return HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="water milligrams must be > 0",
        )

    if isinstance(error, aqua_errors.NoWeight):
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

    if isinstance(error, aqua_errors.ValidationError):
        return HTTPException(status.HTTP_400_BAD_REQUEST)

    return error
