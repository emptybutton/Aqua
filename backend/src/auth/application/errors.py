class ApplicationError(Exception): ...


class UserIsAlreadyRegistered(ApplicationError): ...


class UserIsNotAuthenticated(ApplicationError): ...
