import json
import time
from datetime import datetime, timedelta
from functools import lru_cache
from time import sleep

from app.core.config import Settings


class TokenService:

    def __init__(self):
        self.storage = {}
        self.clenup_interval = 5
        self.clenup_job()

    def save_token(self, token, domain):

        entry = {
            "domain": domain,
            "created_at": int(time.time()),
        }

        # NOTE: In case of REDIS in future
        self.storage[token] = json.dumps(entry)
        return entry

    def load(self, token):
        token_data = self.storage.get(token, None)

        if not token_data:
            return None

        # NOTE: In case of REDIS in future
        created_at = json.loads(token_data).get("created_at", 0)
        if self.token_expired(created_at):
            del self.storage[token]
            return None

        return self.storage.get(token, None)

    def token_expired(self, created_at: int):
        age = int(time.time()) - created_at
        return age > Settings.TOKEN_TTL

    # NOTE: Simple cleanup job running in background to remove expired tokens
    def clenup_job(self):
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
