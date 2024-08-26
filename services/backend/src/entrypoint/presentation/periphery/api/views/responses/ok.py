from fastapi import status

from entrypoint.presentation.periphery.api.views import bodies
from entrypoint.presentation.periphery.api.views.responses.common import View


registered_user_view = View(
    bodies.ok.RegisteredUserView, status.HTTP_201_CREATED
)

user_view = View(bodies.ok.UserView)

day_view = View(bodies.ok.DayView)

new_record_view = View(bodies.ok.NewRecordView, status.HTTP_201_CREATED)
