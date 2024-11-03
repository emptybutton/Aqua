from pymongo import AsyncMongoClient

from aqua.infrastructure.periphery.pymongo.document import Document
from shared.infrastructure.periphery.envs import Env


def client_with(
    *, read_preference: str | None = None
) -> AsyncMongoClient[Document]:
    if read_preference is None:
        read_preference = "secondaryPreferred"

    return AsyncMongoClient(
        Env.mongo_uri,
        uuidRepresentation="standard",
        tz_aware=True,
        readPreference=read_preference,
    )
