# Testy Backend API

## Uruchomienie testów

Z katalogu `backend` uruchom:

```bash
pytest tests/ -v
```

Lub z katalogu głównego projektu:

```bash
cd backend
pytest tests/ -v
```

## Uruchomienie konkretnego testu

```bash
pytest tests/test_verification.py::TestTokenGeneration -v
```

## Uruchomienie z pokazaniem printów

```bash
pytest tests/ -v -s
```

## Pokrycie testami

```bash
pytest tests/ --cov=app --cov-report=html
```

## Opis testów

### TestTokenGeneration
- Testuje generowanie unikalnych tokenów
- Sprawdza format qr_payload

### TestSessionCreation
- Testuje tworzenie sesji weryfikacyjnej
- Sprawdza walidację domen (.gov i zaufane domeny)
- Weryfikuje zapisywanie tokenów w storage

### TestVerificationResult
- Testuje endpoint `/verify/result`
- Sprawdza statusy: `waiting for scan`, `trusted`, `untrusted`
- Testuje walidację domeny

### TestScanEndpoint
- Testuje endpoint `/verify/scan`
- Sprawdza aktualizację tokenu po skanowaniu

### TestTokenStorage
- Testuje bezpośrednio serwis TokenService
- Sprawdza zapisywanie, ładowanie, aktualizację tokenów
- Testuje wygasanie tokenów (TTL)

### TestIntegrationFlow
- Testuje pełny przepływ weryfikacji
- Sprawdza niezależność wielu sesji

## Wymagania

Testy wymagają zainstalowanych zależności z `requirements.txt`:
- pytest
- httpx (używany przez TestClient)

