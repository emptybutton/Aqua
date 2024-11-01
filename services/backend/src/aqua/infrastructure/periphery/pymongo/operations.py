from typing import Any, Iterable, Literal

from pymongo import (
    AsyncClientSession,
    DeleteMany,
    DeleteOne,
    InsertOne,
    ReplaceOne,
    UpdateMany,
    UpdateOne,
)

from aqua.infrastructure.periphery.pymongo.document import (
    Document,
    command_of,
    for_iteration,
)


type Operation = (
    InsertOne
    | DeleteOne
    | DeleteMany
    | ReplaceOne
    | UpdateOne
    | UpdateMany
)
type Put = UpdateOne


type Sort = Literal[1, -1] | None


def to_put(document: Document) -> Put:
    filter_ = {"_id": document["_id"]}
    command = {"$set": command_of(document)}

    return UpdateOne(filter_, command, upsert=True)


def to_map(document: Document, *, prefix: str, id: Any) -> UpdateOne:  # noqa: ANN401
    return UpdateOne(
       {"_id": id},
       {"$set": for_iteration(document, prefix=prefix)},
       array_filters=[{f"{prefix}._id": document["_id"]}],
    )


def to_push(
    document: Document, *, prefix: str, id: Any, sort: Sort = None  # noqa: ANN401
) -> UpdateOne:
    pushing = _pushing_of(document, prefix=prefix, sort=sort)

    return UpdateOne({"_id": id}, pushing, upsert=True)


async def execute(
    raw_operations: Iterable[Operation],
    *,
    session: AsyncClientSession,
    namespace: str | None = None,
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
        namespace=namespace,
    )


def _pushing_of(document: Document, *, prefix: str, sort: Sort) -> Document:
    params = {"$each": [document]}

    if sort is not None:
        params["$sort"] = sort

    return {
        "$push": {f"{prefix}s": params}
    }
