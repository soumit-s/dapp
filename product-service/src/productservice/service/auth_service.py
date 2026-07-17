from ..models import JWTPayload
from ..errors import AuthError

from pydantic import ValidationError
import jwt


class AuthService:
    def __init__(self, secret: str):
        self.secret = secret

    def verify_jwt(self, token: str) -> JWTPayload:
        try:
            payload = jwt.decode(
                token, key=self.secret, algorithms=["HS256"], issuer="com:delivery-app"
            )
            return JWTPayload.model_validate(payload)
        except jwt.ExpiredSignatureError as e:
            raise AuthError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise AuthError("Invalid Token")
        except ValidationError as e:
            raise AuthError("Invalid token")
