from pymongo import AsyncMongoClient

from aqua.infrastructure.periphery.pymongo.document import Document
from shared.infrastructure.periphery.envs import Env


client: AsyncMongoClient[Document] = AsyncMongoClient(
    Env.mongo_uri, uuidRepresentation="standard", tz_aware=True
)
