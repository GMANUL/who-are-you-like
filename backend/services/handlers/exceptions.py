class NameAlreadyExistsError(Exception):

    def __init__(self, failure: str) -> None:
        self.failure = failure
        super().__init__(failure)


class ActionConfirmationRequired(Exception):
    
    def __init__(self, message: str, details: dict):
        self.message = message
        self.details = details
        super().__init__(message)