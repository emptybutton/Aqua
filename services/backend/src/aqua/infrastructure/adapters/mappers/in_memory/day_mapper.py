from aqua.application.ports.mappers import DayMapper, DayMapperTo
from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.infrastructure.adapters.repos.in_memory.users import InMemoryUsers


class InMemoryDayMapper(DayMapper):
    def __init__(self, in_memory_users: InMemoryUsers) -> None:
        self.__in_memory_users = in_memory_users

    async def add_all(self, days: frozenset[Day]) -> None:
        for day in days:
            self.__in_memory_users.add_day(day)

    async def update_all(self, days: frozenset[Day]) -> None:
        for day in days:
            self.__in_memory_users.update_day(day)


class InMemoryDayMapperTo(DayMapperTo[InMemoryUsers]):
    def __call__(self, in_memory_users: InMemoryUsers) -> InMemoryDayMapper:
        return InMemoryDayMapper(in_memory_users)
