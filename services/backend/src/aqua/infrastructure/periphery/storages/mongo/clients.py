from pymongo import AsyncMongoClient

from shared.infrastructure.periphery.envs import Env


client = AsyncMongoClient(
    Env.mongo_uri, uuidRepresentation="standard", tz_aware=True
)
