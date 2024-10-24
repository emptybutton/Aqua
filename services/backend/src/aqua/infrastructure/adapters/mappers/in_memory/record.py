from aqua.application.ports.mappers import RecordMapper, RecordMapperTo
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.infrastructure.adapters.repos.in_memory.user import InMemoryUsers


class InMemoryRecordMapper(RecordMapper):
    def __init__(self, in_memory_users: InMemoryUsers) -> None:
        self.__in_memory_users = in_memory_users

    async def add_all(self, records: frozenset[Record]) -> None:
        for record in records:
            self.__in_memory_users.add_record(record)

    async def update_all(self, records: frozenset[Record]) -> None:
        for record in records:
            self.__in_memory_users.update_record(record)


class InMemoryRecordMapperTo(RecordMapperTo[InMemoryUsers]):
    def __call__(self, in_memory_users: InMemoryUsers) -> InMemoryRecordMapper:
        return InMemoryRecordMapper(in_memory_users)
