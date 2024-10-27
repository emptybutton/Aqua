class UnhandledResultError(Exception): ...


def new_result_view_of(result_value: int) -> str:
    match result_value:
        case 1:
            return "good"
        case 2:
            return "not_enough_water"
        case 3:
            return "excess_water"
        case _:
            raise UnhandledResultError


def old_result_view_of(result_value: int) -> int:
    return result_value
