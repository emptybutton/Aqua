from abc import ABC
from typing import ClassVar

from fastapi import status
from pydantic import BaseModel


class View(BaseModel, ABC):
    status_code: ClassVar[int] = status.HTTP_200_OK


def to_responses(*view_types: type[View]) -> dict:
    return {
        view_type.status_code: {"model": view_type}
        for view_type in view_types
    }
