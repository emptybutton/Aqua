from datetime import date

from aqua.infrastructure.periphery.pymongo.document import DocumentDate


def native_date_of(document_date: DocumentDate) -> date:
    return date(document_date.year, document_date.month, document_date.day)
