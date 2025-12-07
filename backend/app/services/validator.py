from app.core.config import Settings, get_settings
from fastapi import Depends, HTTPException

TRUSTED_DOMAINS = [
    "datki.gov",
    "podatki.gov",
    "wydatki.gov",
]


def is_gov_domain(origin: str):
    if origin.endswith(".gov") is False:
        raise HTTPException(status_code=403, detail="Domain is not .gov")
    return True


def is_trusted_domain(origin: str):
    if origin not in TRUSTED_DOMAINS:
        raise HTTPException(status_code=403, detail="Domain is not trusted")
    return True
