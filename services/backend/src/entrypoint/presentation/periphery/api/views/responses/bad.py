from fastapi import status

from entrypoint.presentation.periphery.api.views import bodies
from entrypoint.presentation.periphery.api.views.responses.common import View


backend_is_not_working_view = View(
    bodies.bad.BackendIsNotWorkingView, status.HTTP_500_INTERNAL_SERVER_ERROR
)

week_password_view = View(
    bodies.bad.WeekPasswordView, status.HTTP_400_BAD_REQUEST
)

no_user_view = View(bodies.bad.NoUserView, status.HTTP_404_NOT_FOUND)

no_current_user_view = View(bodies.bad.NoUserView, status.HTTP_401_UNAUTHORIZED)

incorrect_password_view = View(
    bodies.bad.IncorrectPasswordView, status.HTTP_401_UNAUTHORIZED
)

not_authenticated_view = View(
    bodies.bad.NotAuthenticatedView,
    status.HTTP_401_UNAUTHORIZED,
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
