from copy import deepcopy

from aqua.application.ports.views import RegistrationViewOf
from aqua.domain.model.core.aggregates.user.root import User
from aqua.infrastructure.periphery.views.in_memory.registration_view import (
    InMemoryRegistrationView,
)


class InMemoryRegistrationViewOf(RegistrationViewOf[InMemoryRegistrationView]):
    def __call__(self, user: User) -> InMemoryRegistrationView:
        return InMemoryRegistrationView(user=deepcopy(user))
