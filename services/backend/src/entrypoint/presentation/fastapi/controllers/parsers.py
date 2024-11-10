from typing import Literal
from uuid import UUID


def valid_id_of(id_hex: str) -> UUID | None:
    try:
        return UUID(hex=id_hex)
    except ValueError:
        return None


def optional_valid_id_of(
    id_hex: str | None
) -> UUID | Literal["invalid_hex"] | None:
    if id_hex is None:
        return None

    id_ = valid_id_of(id_hex)

    return "invalid_hex" if id_ is None else None
