from typing import TypeVar

from entrypoint.application.ports import clients
from shared.application.ports.transactions import Transaction


_TransactionT = TypeVar("_TransactionT", bound=Transaction)
_AuthT = TypeVar("_AuthT", bound=clients.auth.Auth[_TransactionT])  # type: ignore[valid-type]
_AquaT = TypeVar("_AquaT", bound=clients.aqua.Aqua[_TransactionT])  # type: ignore[valid-type]


async def perform(
    *,
    auth: clients.auth.Auth,
    aqua: clients.aqua.Aqua,
) -> None:
    await auth.close()
    await aqua.close()
