from uuid import UUID

from pydantic import BaseModel


class IdentifiedUserSchema(BaseModel):
    user_id: UUID
    username: str
