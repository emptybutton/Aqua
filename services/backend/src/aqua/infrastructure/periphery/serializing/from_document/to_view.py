class UnhandledResultError(Exception): ...


def new_result_view_of(document_result: int) -> str:
    match document_result:
        case 1:
            return "good"
        case 2:
            return "not_enough_water"
        case 3:
            return "excess_water"
        case _:
            raise UnhandledResultError


def old_result_view_of(document_result: int) -> int:
    return document_result


def new_maybe_result_view_of(document_result: int | None) -> str | None:
    if document_result is None:
        return None

    return new_result_view_of(document_result)


def old_maybe_result_view_of(document_result: int | None) -> int | None:
    return document_result
