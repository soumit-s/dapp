import jwt
from datetime import datetime, UTC, timedelta


class JWTService:
    def __init__(self, secret: str):
        self.secret = secret

    def generate_user_token(self, user_id: str):
        payload = {
            "iss": "com:dapp",
            "sub": user_id,
            "role": "user",
            "exp": datetime.now(UTC) + timedelta(hours=24),
        }
        return jwt.encode(payload, key=self.secret, algorithm="HS256")
