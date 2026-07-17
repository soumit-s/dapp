import bcrypt

class PasswordService:
    def __init__(self):
        pass

    def hash_pwd(self, password: str) -> str:
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")

    def verify_pwd(self, hashed_pwd: str, pwd: str):
        return bcrypt.checkpw(pwd.encode("utf-8"), hashed_pwd.encode("utf-8"))