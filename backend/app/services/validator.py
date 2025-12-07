from app.core.config import Settings
from fastapi import HTTPException


def is_gov_domain(origin: str):
    if origin.endswith(".gov") is False:
        raise HTTPException(status_code=403, detail="Domain is not .gov")
    return True


def is_trusted_domain(origin: str):
    if origin not in Settings.TRUSTED_DOMAINS:
        raise HTTPException(status_code=403, detail="Domain is not trusted")
    return True
