from uuid import UUID


def id_of(id_hex: str | None) -> UUID | None:
    if id_hex is None:
        return None

    try:
        return UUID(hex=id_hex)
    except ValueError:
        return None
