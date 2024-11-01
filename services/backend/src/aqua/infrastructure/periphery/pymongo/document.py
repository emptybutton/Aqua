from typing import Any


type Document = dict[str, Any]


def command_of(document: Document) -> Document:
    command_document = dict(document.items())
    del command_document["_id"]

    return command_document


def for_iteration(document: Document, *, prefix: str) -> Document:
    return {
        f"{prefix}s.$[{prefix}].key": v
        for k, v in document.items()
        if k != "_id"
    }
