from dataclasses import dataclass
import os


@dataclass
class Config:
    database_url: str


def load_config() -> Config:
    return Config(database_url=os.getenv("DATABASE_URL"))
