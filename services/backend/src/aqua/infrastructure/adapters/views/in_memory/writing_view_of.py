from copy import deepcopy

from aqua.application.ports.views import WritingViewOf
from aqua.domain.model.core.aggregates.user.root import User, WritingOutput
from aqua.infrastructure.periphery.views.in_memory.writing_view import (
    InMemoryWritingView,
)


class InMemoryWritingViewOf(WritingViewOf[InMemoryWritingView]):
    def __call__(
        self, *, user: User, output: WritingOutput
    ) -> InMemoryWritingView:
        return InMemoryWritingView(user=deepcopy(user), output=output)
