from fastapi import status

from entrypoint.presentation.periphery.api.views import bodies
from entrypoint.presentation.periphery.api.views.responses.common import View


backend_is_not_working_view = View(
    bodies.bad.BackendIsNotWorkingView, status.HTTP_500_INTERNAL_SERVER_ERROR
)

week_password_view = View(
    bodies.bad.WeekPasswordView, status.HTTP_400_BAD_REQUEST
)

invalid_jwt_view = View(bodies.bad.InvalidJWTView, status.HTTP_401_UNAUTHORIZED)

expired_jwt_view = View(bodies.bad.ExpiredJWTView, status.HTTP_401_UNAUTHORIZED)

no_user_view = View(bodies.bad.NoUserView, status.HTTP_404_NOT_FOUND)

no_current_user_view = View(bodies.bad.NoUserView, status.HTTP_401_UNAUTHORIZED)

incorrect_password_view = View(
    bodies.bad.IncorrectPasswordView, status.HTTP_401_UNAUTHORIZED
)

not_utc_refresh_token_expiration_date_view = View(
    bodies.bad.NotUTCRefreshTokenExpirationDateView,
    status.HTTP_401_UNAUTHORIZED,
)

expired_refresh_token_view = View(
    bodies.bad.ExpiredRefreshTokenView, status.HTTP_404_NOT_FOUND
)

incorrect_water_amount_view = View(
    bodies.bad.IncorrectWaterAmountView, status.HTTP_400_BAD_REQUEST
)

incorrect_weight_amount_view = View(
    bodies.bad.IncorrectWeightAmountView, status.HTTP_400_BAD_REQUEST
)

no_weight_for_water_balance_view = View(
    bodies.bad.NoWeightForWaterBalanceView, status.HTTP_400_BAD_REQUEST
)

extreme_weight_for_water_balance_view = View(
    bodies.bad.ExtremeWeightForWaterBalanceView, status.HTTP_400_BAD_REQUEST
)

empty_username_view = View(
    bodies.bad.EmptyUsernameView, status.HTTP_400_BAD_REQUEST
)

user_is_already_registered_view = View(
    bodies.bad.UserIsAlreadyRegisteredView, status.HTTP_409_CONFLICT
)
