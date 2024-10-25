from copy import deepcopy

from aqua.application.ports.views import CancellationViewOf
from aqua.domain.model.core.aggregates.user.root import CancellationOutput, User
from aqua.infrastructure.periphery.views.in_memory.cancellation_view import (
    InMemoryCancellationView,
)


class InMemoryCancellationViewOf(CancellationViewOf[InMemoryCancellationView]):
    def __call__(
        self, *, user: User, output: CancellationOutput
    ) -> InMemoryCancellationView:
        return InMemoryCancellationView(user=deepcopy(user), output=output)
