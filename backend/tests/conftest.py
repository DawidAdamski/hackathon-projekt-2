import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Dodaj katalog backend do PYTHONPATH jeśli nie jest już dodany
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import app
from app.services.storage import get_token_service


@pytest.fixture()
def client():
    """Fixture zwracająca TestClient dla aplikacji FastAPI"""
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def clear_token_storage():
    """Automatycznie czyści storage przed każdym testem"""
    # Pobierz instancję TokenService i wyczyść storage
    token_service = get_token_service()
    token_service.storage.clear()
    yield
    # Opcjonalnie wyczyść po teście
    token_service.storage.clear()
