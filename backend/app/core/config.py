from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Hacknation GOV Verification"

    TRUSTED_DOMAINS: List[str] = [
        "datki.gov",
        "podatki.gov",
        "wydatki.gov",
    ]

    TOKEN_TTL: int = 2 * 60  # 2min

    # NOTE: We can load trusted domains from env
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
