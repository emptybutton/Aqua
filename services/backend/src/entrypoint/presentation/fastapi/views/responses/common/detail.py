from pydantic import BaseModel


class DetailPartSchema(BaseModel):
    msg: str
    type: str


type Detail = list[DetailPartSchema]
