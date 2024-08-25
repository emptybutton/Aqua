from typing import Self, Type, Any
from types import TracebackType

from shared.application.ports import transactions
from shared.application.tests.periphery import uows


class UoWTransaction(transactions.Transaction):
    def __init__(self, uow: uows.InMemoryUoW[Any]) -> None:
        self.__is_rollbacked = False
        self.__uow = uow

    async def rollback(self) -> None:
        self.__is_rollbacked = True
        self.__uow.rollback()

    async def __aenter__(self) -> Self:
        self.__uow.begin()
        return self

    async def __aexit__(
        self,
        error_type: Type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if self.__is_rollbacked:
            return error is None

        if error is None:
            self.__uow.commit()
        else:
            self.__uow.rollback()

        return error is None


class UoWTransactionFactory(
    transactions.TransactionFactory[Any]
):
    def __call__(self, uow: Any) -> UoWTransaction:  # noqa: ANN401
        assert isinstance(uow, uows.InMemoryUoW)
        return UoWTransaction(uow)
