class DAppError(Exception):
    """
    Base class of all exceptions
    """
    pass


class AuthError(DAppError):
    pass

class ProductNotFoundError(DAppError):
    pass
