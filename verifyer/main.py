from contextlib import asynccontextmanager

from fastapi import FastAPI
from routes import verifyer_router

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    from verifyer.services.storage import TokenStorage

    print("Start verifyer!")

    # NOTE: Inicjalizacja obiektu TokenStorage
    # Na potrzeby MVP - to jest zwykla klasa ktora trzyma tokeny w pamieci
    # Normalnie moze to byc jakas baza NoSQL albo Redis
    token_storage = TokenStorage()
    app.state.token_storage = token_storage

    yield

    print("Stop verifyer!")


# NOTE: For Dependency Injection
def get_token_storage():
    return app.state.token_storage


# Endpoint do sprawdzania wyniku weryfikacji
@app.get("/")
async def test_connection():
    return {"status": "verifyer is running"}


app.include_router(verifyer_router, prefix="/verify")
