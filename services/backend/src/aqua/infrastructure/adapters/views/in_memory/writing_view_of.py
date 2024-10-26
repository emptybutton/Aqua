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
            previous_records=self.__ordered(output.previous_records),
        )

    def __ordered(self, records: Iterable[Record]) -> tuple[Record, ...]:
        return tuple(sorted(
            records,
            key=lambda record: record.recording_time.datetime_,
            reverse=True,
        ))
