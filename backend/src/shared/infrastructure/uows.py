from typing import Never

from src.shared.application.ports import uows


class UoW(uows.UoW[Never]):
    def register_new(self, value: Never) -> None:
        ...

    def register_dirty(self, value: Never) -> None:
        ...

    def register_deleted(self, value: Never) -> None:
        ...

    async def __aexit__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]  # noqa: ANN003, ANN002
        ...
