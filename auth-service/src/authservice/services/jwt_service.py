import jwt
from datetime import datetime, UTC, timedelta
from pydantic import ValidationError
from ..errors import InvalidTokenError
from ..models import JWTPayload
from ..config import Config

class JWTService:
    def __init__(self, config: Config):
        self.config = config
        pass
    
    def generate_token(self, user_id: str, role: list[str]):
        payload = {
            "iss": "com:dapp",
            "sub": user_id,
            "role": role,
            "exp": datetime.now(UTC) + timedelta(hours=24),
        }
        return jwt.encode(payload, key=self.config.jwt_secret, algorithm="HS256")
    
    def generate_admin_token(self, user_id: str):
        return self.generate_token(user_id, [self.config.role_name_admin])

    def generate_user_token(self, user_id: str):
        return self.generate_token(user_id, [self.config.role_name_user])
    
    def validate(self, token: str) -> JWTPayload:
        try:
            # PyJWT automatically verifies signature and checks 'exp' / 'nbf' claims
            payload = jwt.decode(token, self.config.jwt_secret, algorithms=["HS256"])
            id = payload["sub"]
            role = payload["role"]
            if not isinstance(role, list):
                role = [role]
            return JWTPayload(id=id, role=role)
        except ValidationError:
            raise InvalidTokenError(token, f"Either invalid user_id ('{id}') or invalid role ('{role}'). Note the single quotes are not part of the values.")
        except jwt.ExpiredSignatureError:
            raise InvalidTokenError(token, "Validation failed: The token has expired.")
        except jwt.InvalidSignatureError:
            raise InvalidTokenError(token, "Validation failed: The signature is invalid.")
        except jwt.DecodeError:
            raise InvalidTokenError(token, "Validation failed: The token is malformed.")
        except jwt.InvalidTokenError as e:
            raise InvalidTokenError(token, f"Validation failed: Invalid token ({e})")