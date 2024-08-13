from typing import TypeVar

from entrypoint.application.ports import clients
from shared.application.ports.transactions import Transaction


_TransactionT = TypeVar("_TransactionT", bound=Transaction)


async def perform(
    *,
    auth: clients.auth.Auth[_TransactionT],
    aqua: clients.aqua.Aqua[_TransactionT],
) -> None:
    await auth.close()
    await aqua.close()
