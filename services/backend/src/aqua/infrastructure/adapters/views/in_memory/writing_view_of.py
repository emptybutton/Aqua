from copy import deepcopy
from typing import Iterable

from aqua.application.ports.views import WritingViewOf
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import User, WritingOutput
from aqua.infrastructure.periphery.views.in_memory.writing_view import (
    InMemoryWritingView,
)


class InMemoryWritingViewOf(WritingViewOf[InMemoryWritingView]):
    def __call__(
        self, *, user: User, output: WritingOutput
    ) -> InMemoryWritingView:
        return InMemoryWritingView(
            user=deepcopy(user),
            day=deepcopy(output.day),
            new_record=deepcopy(output.new_record),
            previous_records=self.__viewable(output.previous_records),
        )

    def __viewable(self, records: Iterable[Record]) -> tuple[Record, ...]:
        sorted_records = sorted(
            records,
            key=lambda record: record.recording_time.datetime_,
            reverse=True,
        )

        return tuple(
            record
            for record in sorted_records
            if not record.is_cancelled
        )
