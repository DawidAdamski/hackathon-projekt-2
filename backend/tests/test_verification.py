import json
import time
from unittest.mock import patch

import pytest
from app.services.storage import TokenService


@pytest.fixture
def trusted_domain():
    """Fixture zwracająca zaufaną domenę do testów"""
    return "datki.gov"


@pytest.fixture
def token_service():
    """Fixture zwracająca nową instancję TokenService dla każdego testu"""
    return TokenService()


class TestTokenGeneration:
    """Testy generowania tokenów"""

    def test_generate_token_creates_unique_tokens(self, client, trusted_domain):
        """Test czy generowane tokeny są unikalne"""
        response1 = client.post(
            "/verify/session",
            json={"url": "https://example.com", "service_id": "test"},
            headers={"host": trusted_domain},
        )
        response2 = client.post(
            "/verify/session",
            json={"url": "https://example.com", "service_id": "test"},
            headers={"host": trusted_domain},
        )

        assert response1.status_code == 200
        assert response2.status_code == 200

        data1 = response1.json()
        data2 = response2.json()

        assert data1["nonce"] != data2["nonce"]
        assert "nonce" in data1
        assert "qr_payload" in data1
        assert data1["qr_payload"].startswith("moby-sim://verify?nonce=")

    def test_qr_payload_contains_nonce(self, client, trusted_domain):
        """Test czy qr_payload zawiera nonce"""
        response = client.post(
            "/verify/session",
            json={"url": "https://example.com", "service_id": "test"},
            headers={"host": trusted_domain},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["nonce"] in data["qr_payload"]


class TestSessionCreation:
    """Testy tworzenia sesji weryfikacyjnej"""

    def test_create_session_success(self, client, trusted_domain):
        """Test poprawnego utworzenia sesji"""
        response = client.post(
            "/verify/session",
            json={"url": "https://example.com", "service_id": "test"},
            headers={"host": trusted_domain},
        )

        assert response.status_code == 200
        data = response.json()
        assert "nonce" in data
        assert "qr_payload" in data
        assert len(data["nonce"]) > 0

    def test_create_session_without_gov_domain(self, client):
        """Test odrzucenia żądania z domeny nie .gov"""
        response = client.post(
            "/verify/session",
            json={"url": "https://example.com", "service_id": "test"},
            headers={"host": "example.com"},
        )

        assert response.status_code == 403
        assert "not .gov" in response.json()["detail"].lower()

    def test_create_session_with_untrusted_domain(self, client):
        """Test odrzucenia żądania z niezaufanej domeny .gov"""
        response = client.post(
            "/verify/session",
            json={"url": "https://example.com", "service_id": "test"},
            headers={"host": "other.gov"},
        )

        assert response.status_code == 403
        assert "not trusted" in response.json()["detail"].lower()

    def test_create_session_saves_token(self, client, trusted_domain):
        """Test czy token jest zapisywany w storage"""
        from app.services.storage import get_token_service

        response = client.post(
            "/verify/session",
            json={"url": "https://example.com", "service_id": "test"},
            headers={"host": trusted_domain},
        )

        assert response.status_code == 200
        data = response.json()
        nonce = data["nonce"]

        # Sprawdź czy token istnieje w storage (używamy tej samej instancji co app)
        token_service = get_token_service()
        token_data = token_service.load(nonce)
        assert token_data is not None
        assert token_data["domain"] == trusted_domain
        assert token_data["mobywatel_scan"] == 0


class TestVerificationResult:
    """Testy sprawdzania wyniku weryfikacji"""

    def test_result_waiting_for_scan(self, client, trusted_domain):
        """Test statusu 'waiting for scan' gdy token nie został jeszcze zeskanowany"""
        # Utwórz sesję
        session_response = client.post(
            "/verify/session",
            json={"url": "https://example.com", "service_id": "test"},
            headers={"host": trusted_domain},
        )
        nonce = session_response.json()["nonce"]

        # Sprawdź wynik przed skanowaniem
        result_response = client.get(
            f"/verify/result?nonce={nonce}",
            headers={"host": trusted_domain},
        )

        assert result_response.status_code == 200
        data = result_response.json()
        assert data["status"] == "waiting for scan"

    def test_result_trusted_after_scan(self, client, trusted_domain):
        """Test statusu 'trusted' po zeskanowaniu"""
        # Utwórz sesję
        session_response = client.post(
            "/verify/session",
            json={"url": "https://example.com", "service_id": "test"},
            headers={"host": trusted_domain},
        )
        nonce = session_response.json()["nonce"]

        # Zeskanuj kod
        scan_response = client.post(
            "/verify/scan",
            json={"nonce": nonce, "mobywatel": "mObywatel-mock"},
            headers={"host": trusted_domain},
        )
        assert scan_response.status_code == 200

        # Sprawdź wynik po skanowaniu
        result_response = client.get(
            f"/verify/result?nonce={nonce}",
            headers={"host": trusted_domain},
        )

        assert result_response.status_code == 200
        data = result_response.json()
        assert data["status"] == "trusted"

    def test_result_untrusted_for_missing_token(self, client, trusted_domain):
        """Test statusu 'untrusted' dla nieistniejącego tokenu"""
        fake_nonce = "00000000-0000-0000-0000-000000000000"

        result_response = client.get(
            f"/verify/result?nonce={fake_nonce}",
            headers={"host": trusted_domain},
        )

        assert result_response.status_code == 200
        data = result_response.json()
        assert data["status"] == "untrusted"

    def test_result_untrusted_for_different_domain(self, client, trusted_domain):
        """Test statusu 'untrusted' gdy domena się nie zgadza"""
        # Utwórz sesję z jedną domeną
        session_response = client.post(
            "/verify/session",
            json={"url": "https://example.com", "service_id": "test"},
            headers={"host": trusted_domain},
        )
        nonce = session_response.json()["nonce"]

        # Sprawdź wynik z innej domeny
        result_response = client.get(
            f"/verify/result?nonce={nonce}",
            headers={"host": "podatki.gov"},  # Inna domena
        )

        assert result_response.status_code == 200
        data = result_response.json()
        assert data["status"] == "untrusted"


class TestScanEndpoint:
    """Testy endpointu skanowania"""

    def test_scan_updates_token(self, client, trusted_domain):
        """Test czy skanowanie aktualizuje token"""
        # Utwórz sesję
        session_response = client.post(
            "/verify/session",
            json={"url": "https://example.com", "service_id": "test"},
            headers={"host": trusted_domain},
        )
        nonce = session_response.json()["nonce"]

        # Zeskanuj kod
        scan_response = client.post(
            "/verify/scan",
            json={"nonce": nonce, "mobywatel": "mObywatel-mock"},
            headers={"host": trusted_domain},
        )

        assert scan_response.status_code == 200
        data = scan_response.json()
        assert data["status"] == "trusted"
        assert data["origin"] == trusted_domain

    def test_scan_untrusted_for_missing_token(self, client, trusted_domain):
        """Test skanowania nieistniejącego tokenu"""
        fake_nonce = "00000000-0000-0000-0000-000000000000"

        scan_response = client.post(
            "/verify/scan",
            json={"nonce": fake_nonce, "mobywatel": "mObywatel-mock"},
            headers={"host": trusted_domain},
        )

        assert scan_response.status_code == 200
        data = scan_response.json()
        assert data["status"] == "untrusted"


class TestTokenStorage:
    """Testy serwisu przechowywania tokenów"""

    def test_save_token(self, token_service):
        """Test zapisywania tokenu"""
        token = "test-token-123"
        domain = "test.gov"

        result = token_service.save_token(token, domain)

        assert result["domain"] == domain
        assert result["mobywatel_scan"] == 0
        assert "created_at" in result

    def test_load_token(self, token_service):
        """Test ładowania tokenu"""
        token = "test-token-456"
        domain = "test.gov"

        token_service.save_token(token, domain)
        loaded = token_service.load(token)

        assert loaded is not None
        assert loaded["domain"] == domain
        assert loaded["mobywatel_scan"] == 0

    def test_load_nonexistent_token(self, token_service):
        """Test ładowania nieistniejącego tokenu"""
        loaded = token_service.load("nonexistent-token")
        assert loaded is None

    def test_update_token(self, token_service):
        """Test aktualizacji tokenu"""
        token = "test-token-789"
        domain = "test.gov"

        token_service.save_token(token, domain)
        updated = token_service.update(token)

        assert updated is not None
        assert updated["mobywatel_scan"] == 1

        # Sprawdź czy zmiana została zapisana
        loaded = token_service.load(token)
        assert loaded["mobywatel_scan"] == 1

    def test_token_expiration(self, token_service):
        """Test wygasania tokenu"""
        token = "test-token-expired"
        domain = "test.gov"

        token_service.save_token(token, domain)

        # Symuluj wygasły token poprzez modyfikację created_at
        token_data = token_service.load(token)
        old_created_at = token_data["created_at"]

        # Ustaw created_at na 3 minuty temu (więcej niż TTL = 2 minuty)
        expired_time = int(time.time()) - (3 * 60)
        token_data["created_at"] = expired_time
        token_service.storage[token] = json.dumps(token_data)

        # Token powinien być wygasły
        loaded = token_service.load(token)
        assert loaded is None

    def test_update_nonexistent_token(self, token_service):
        """Test aktualizacji nieistniejącego tokenu"""
        updated = token_service.update("nonexistent-token")
        assert updated is None


class TestIntegrationFlow:
    """Testy pełnego przepływu weryfikacji"""

    def test_full_verification_flow(self, client, trusted_domain):
        """Test pełnego przepływu: sesja -> skanowanie -> weryfikacja"""
        # 1. Utwórz sesję
        session_response = client.post(
            "/verify/session",
            json={"url": "https://example.com", "service_id": "test"},
            headers={"host": trusted_domain},
        )
        assert session_response.status_code == 200
        nonce = session_response.json()["nonce"]

        # 2. Sprawdź status przed skanowaniem
        result_before = client.get(
            f"/verify/result?nonce={nonce}",
            headers={"host": trusted_domain},
        )
        assert result_before.json()["status"] == "waiting for scan"

        # 3. Zeskanuj kod
        scan_response = client.post(
            "/verify/scan",
            json={"nonce": nonce, "mobywatel": "mObywatel-mock"},
            headers={"host": trusted_domain},
        )
        assert scan_response.status_code == 200
        assert scan_response.json()["status"] == "trusted"

        # 4. Sprawdź status po skanowaniu
        result_after = client.get(
            f"/verify/result?nonce={nonce}",
            headers={"host": trusted_domain},
        )
        assert result_after.json()["status"] == "trusted"

    def test_multiple_sessions_independent(self, client, trusted_domain):
        """Test czy wiele sesji działa niezależnie"""
        # Utwórz dwie sesje
        session1 = client.post(
            "/verify/session",
            json={"url": "https://example.com", "service_id": "test1"},
            headers={"host": trusted_domain},
        )
        session2 = client.post(
            "/verify/session",
            json={"url": "https://example.com", "service_id": "test2"},
            headers={"host": trusted_domain},
        )

        nonce1 = session1.json()["nonce"]
        nonce2 = session2.json()["nonce"]

        # Zeskanuj tylko pierwszą
        client.post(
            "/verify/scan",
            json={"nonce": nonce1, "mobywatel": "mObywatel-mock"},
            headers={"host": trusted_domain},
        )

        # Sprawdź statusy
        result1 = client.get(
            f"/verify/result?nonce={nonce1}",
            headers={"host": trusted_domain},
        )
        result2 = client.get(
            f"/verify/result?nonce={nonce2}",
            headers={"host": trusted_domain},
        )

        assert result1.json()["status"] == "trusted"
        assert result2.json()["status"] == "waiting for scan"
