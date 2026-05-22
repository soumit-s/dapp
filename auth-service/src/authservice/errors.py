class DappError(Exception):
    pass


class PhoneNumberAlreadyTakenError(DappError):
    def __init__(self, phone: str, user_id: int):
        DappError.__init__(self)
        self.phone = phone
        self.user_id = user_id
