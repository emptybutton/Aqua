from datetime import date, datetime

from aqua.infrastructure.periphery.pymongo.document import DocumentDate


def document_date_of(date_: date) -> DocumentDate:
    return datetime(date_.year, date_.month, date_.day)
