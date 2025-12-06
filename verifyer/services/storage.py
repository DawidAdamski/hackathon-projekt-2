# Dodaj TTL na 2 min tstowo - ma sie wygaszac
# maowanie klucz - domena
# mapowanie tylko w backu

# Dodaj ttl na klucze
# musze miec jakies opcje zeby wygaszac


class TokenStorage:
    def __init__(self):
        self.storage = {}

    def save(self, key, value):
        self.storage[key] = value

    def load(self, key):
        return self.storage.get(key, None)
