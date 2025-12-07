import json
import time
from functools import lru_cache
from time import sleep
from typing import Optional

from app.core.logger import logger

TOKEN_TTL: int = 2 * 60


class TokenService:

    def __init__(self):
        self.storage = {}
        self.clenup_interval = 5

    def save_token(self, token: str, domain: str) -> dict:

        logger.info(f"Save token: {token} for domain: {domain}")

        entry = {
            "domain": domain,
            "created_at": int(time.time()),
            "mobywatel_scan": 0,
        }

        # NOTE: In case of REDIS in future
        self.storage[token] = json.dumps(entry)
        logger.info(self.storage)
        return entry

    def remove(self, token: str) -> None:
        # NOTE: After verification there is no point to keep the token in stroage
        del self.storage[token]

    def load(self, token: str) -> Optional[dict]:
        token_data = self.storage.get(token, None)

        if not token_data:
            logger.info(f"Missing token: {token}")
            return None

        # NOTE: In case of REDIS in future
        token_data = json.loads(token_data)
        created_at = token_data.get("created_at", 0)
        if self.token_expired(created_at):
            logger.info(f"Expired token: {token}")
            del self.storage[token]
            return None

        logger.info(f"Token found: {token}")
        return token_data

    def update(self, token: str) -> Optional[dict]:
        logger.info(f"Update for token: {token}")
        token_data = self.storage.get(token, None)

        if not token_data:
            logger.info(f"Missing token: {token}")
            return None

        # NOTE: In case of REDIS in future
        token_data = json.loads(token_data)
        created_at = token_data.get("created_at", 0)
        if self.token_expired(created_at):
            logger.info(f"Expired token: {token}")
            del self.storage[token]
            return None

        logger.info(f"Token updated: {token}")
        token_data["mobywatel_scan"] = 1
        # Save updated token back to storage
        self.storage[token] = json.dumps(token_data)
        return token_data

    def token_expired(self, created_at: int) -> bool:
        age = int(time.time()) - created_at
        return age > TOKEN_TTL

    # NOTE: Simple cleanup job running in background to remove expired tokens
    def clenup_job(self) -> None:
        while True:
            tokens_to_delete = []
            for token, data in self.storage.items():
                created_at = json.loads(data).get("created_at", 0)
                if self.token_expired(created_at):
                    del self.storage[token]

            for token in tokens_to_delete:
                del self.storage[token]

            sleep(self.clenup_interval)


@lru_cache
def get_token_service() -> TokenService:
    # NOTE: Inicjalizacja obiektu TokenStorage
    # Na potrzeby MVP - to jest zwykla klasa ktora trzyma tokeny w pamieci
    # Normalnie moze to byc Redis ktory bedzie trzymal info o tokenach
    return TokenService()
