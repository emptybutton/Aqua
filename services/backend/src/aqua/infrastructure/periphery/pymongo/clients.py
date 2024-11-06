from pymongo import AsyncMongoClient

from aqua.infrastructure.periphery import envs
from aqua.infrastructure.periphery.pymongo.document import Document


def client_with(
    *, read_preference: str | None = None
) -> AsyncMongoClient[Document]:
    if read_preference is None:
        read_preference = "secondaryPreferred"

    return AsyncMongoClient(
        envs.mongo_uri,
        uuidRepresentation="standard",
        tz_aware=True,
        readPreference=read_preference,
    )
