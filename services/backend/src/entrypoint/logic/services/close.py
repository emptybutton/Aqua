from entrypoint.infrastructure.facades.clients import aqua, auth


async def close() -> None:
    await aqua.close()
    await auth.close()
