class DappError(Exception):
    pass


class PhoneNumberAlreadyTakenError(DappError):
    def __init__(self, phone: str, user_id: int):
        DappError.__init__(self)
        self.phone = phone
        self.user_id = user_id

class InvalidTokenError(DappError):
    def __init__(self, token: str, msg: str):
        DappError.__init__(self, msg)
        self.token = token
        self.msg = msg

class UserNotFoundError(DappError):
    pass

class UserNotAuthorizedError(DappError):
    """Raised when the user is not authorized to do something."""
    pass

class EmailAlreadyTakenError(DappError):
    """
    Raised when trying to create an user with an email which 
    has already been taken
    """
    pass

class RoleAlreadyExistsError(DappError):
    """
    Raised when trying to create a role with a duplicate name.
    """