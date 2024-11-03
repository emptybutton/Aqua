from datetime import timedelta

from aqua.infrastructure.periphery.pymongo.document import (
    Document,
    DocumentDate,
)


def in_date_range(document_date: DocumentDate) -> Document:
    return {
        "$gte": document_date,
        "$lt": document_date + timedelta(days=1),
    }


def cond_about(query: Document, *, field: str) -> list[Document]:
    return [{operator: [field, operand]} for operator, operand in query.items()]
