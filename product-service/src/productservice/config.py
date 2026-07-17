import os
from dataclasses import dataclass


@dataclass
class Config:
    database_url: str
    jwt_secret: str


def load_config() -> Config:
    database_url = os.getenv("DATABASE_URL")
    jwt_secret = os.getenv("JWT_SECRET")
    return Config(database_url=database_url, jwt_secret=jwt_secret)
