class ErrorWrapper[ErrorT: Exception](Exception):
    def __init__(self, error: ErrorT) -> None:
        super().__init__(str())
        self.__error = error

    @property
    def error(self) -> ErrorT:
        return self.__error
