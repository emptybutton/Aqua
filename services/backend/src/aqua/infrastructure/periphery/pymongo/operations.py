from typing import Any, Iterable, Literal

from pymongo import (
    DeleteMany,
    DeleteOne,
    InsertOne,
    ReplaceOne,
    UpdateMany,
    UpdateOne,
)
from pymongo.asynchronous.client_session import AsyncClientSession

from aqua.infrastructure.periphery.pymongo.document import Document


type Operation = (
    InsertOne[Document]
    | ReplaceOne[Document]
    | UpdateOne
    | UpdateMany
    | DeleteOne
    | DeleteMany
)
type Put = UpdateOne
type Map = UpdateOne
type Push = UpdateOne


type Sort = Literal[1, -1] | None


class ArrayOperations:
    def __init__(
        self, *, namespace: str, prefix: str, sort: Sort = None
    ) -> None:
        self.__namespace = namespace
        self.__prefix = prefix
        self.__sort = sort

    def to_map(self, document: Document, *, id: Any) -> Map:  # noqa: ANN401
        return UpdateOne(
           {"_id": id},
           {"$set": self.__for_iteration(document)},
           array_filters=[{f"{self.__prefix}._id": document["_id"]}],
           namespace=self.__namespace,
        )

    def to_push(self, document: Document, *, id: Any) -> Push:  # noqa: ANN401
        pushing = self.__pushing_of(document)

        return UpdateOne(
            {"_id": id}, pushing, upsert=True, namespace=self.__namespace
        )

    def __pushing_of(self, document: Document) -> Document:
        params: Document = {"$each": [document]}

        if self.__sort is not None:
            params["$sort"] = self.__sort

        return {
            "$push": {f"{self.__prefix}s": params}
        }

    def __for_iteration(self, document: Document) -> Document:
        return {
            f"{self.__prefix}s.$[{self.__prefix}].key": v
            for k, v in document.items()
            if k != "_id"
        }


class RootOperations:
    def __init__(self, *, namespace: str) -> None:
        self.__namespace = namespace

    def to_put(self, document: Document) -> Put:
        filter_ = {"_id": document["_id"]}
        command = {"$set": _command_of(document)}

        return UpdateOne(
            filter_, command, upsert=True, namespace=self.__namespace
        )


async def execute(
    raw_operations: Iterable[Operation],
    *,
    session: AsyncClientSession,
    comment: str | None = None,
) -> None:
    operations = tuple(raw_operations)

    if not operations:
        return

    await session.client.bulk_write(
        operations,
        session=session,
        ordered=False,
        comment=comment,
    )


def _command_of(document: Document) -> Document:
    command_document = dict(document.items())
    del command_document["_id"]

    return command_document
