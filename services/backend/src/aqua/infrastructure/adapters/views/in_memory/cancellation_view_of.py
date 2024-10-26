from copy import deepcopy
from typing import Iterable

from aqua.application.ports.views import CancellationViewOf
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import CancellationOutput, User
from aqua.infrastructure.periphery.views.in_memory.cancellation_view import (
    InMemoryCancellationView,
)


class InMemoryCancellationViewOf(CancellationViewOf[InMemoryCancellationView]):
    def __call__(
        self, *, user: User, output: CancellationOutput
    ) -> InMemoryCancellationView:
        return InMemoryCancellationView(
            user=deepcopy(user),
            day=deepcopy(output.day),
            cancelled_record=deepcopy(output.cancelled_record),
            records=self.__ordered(user.records),
        )

    def __ordered(self, records: Iterable[Record]) -> tuple[Record, ...]:
        return tuple(sorted(
            records,
            key=lambda record: record.recording_time.datetime_,
            reverse=True,
        ))
