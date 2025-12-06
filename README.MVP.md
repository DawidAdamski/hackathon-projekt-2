# Minimum Viable Product (MVP)
## Weryfikacja autentyczności stron gov.pl za pomocą aplikacji mobilnej mObywatel

---

## 1. Definicja Produktu

### 1.1. Elevator Pitch
Budujemy prosty moduł weryfikacji, który umożliwia obywatelom sprawdzenie autentyczności strony gov.pl poprzez zeskanowanie kodu QR w aplikacji mObywatel. Rozwiązanie wyświetla podstawowe informacje o bezpieczeństwie strony i wynik weryfikacji, pomagając użytkownikowi podjąć decyzję, czy strona jest zaufana.

### 1.2. Kluczowy problem (Core Pain Point)
Dostarczenie użytkownikowi natychmiastowej, wiarygodnej weryfikacji autentyczności strony rządowej, zanim wprowadzi on swoje dane logowania lub wrażliwe informacje.

---

## 2. Zakres MVP

### 2.1. Najkrótsza ścieżka do wartości (Kluczowe funkcjonalności MVP)

#### 2.1.1. Moduł na stronie gov.pl
- **Widget/komponent JavaScript** do osadzenia na stronie gov.pl
- **Przycisk CTA "Zweryfikuj stronę"** z ikoną QR
- **Podstawowe informacje o bezpieczeństwie:**
  - Sprawdzenie rozszerzenia domeny (.gov.pl)
  - Informacja o certyfikacie SSL (HTTPS)
  - Link do listy oficjalnych portali (statyczny)

#### 2.1.2. Generowanie kodu QR
- **Backend API endpoint** generujący jednorazowy kod QR z nonce
- **Kod QR zawiera:**
  - URL strony do weryfikacji
  - Jednorazowy token (nonce)
  - Timestamp
- **Wyświetlenie kodu QR** w popup/modal na stronie

#### 2.1.3. Weryfikacja w aplikacji mObywatel (symulacja)
- **Symulacja skanowania QR** w aplikacji mObywatel
- **Weryfikacja na podstawie:**
  - Listy oficjalnych domen gov.pl (JSON)
  - Sprawdzenia, czy domena znajduje się na liście zaufanych
- **Walidacja nonce** i timestamp (zapobieganie replay attacks)

#### 2.1.4. Wynik weryfikacji
- **Komunikat w aplikacji mObywatel:**
  - ✅ Pozytywny: "Strona jest zaufana" + podstawowe informacje
  - ⚠️ Negatywny: "Uwaga: Strona może być nieautentyczna" + instrukcje
- **Aktualizacja widoku na stronie** (opcjonalnie, przez WebSocket lub polling)

### 2.2. Ścieżki użytkownika (User Stories dla MVP)

**User Story 1: Weryfikacja zaufanej strony**
```
Jako obywatel, chcę zweryfikować stronę gov.pl, 
która prosi mnie o dane logowania, 
aby upewnić się, że to oficjalna strona rządowa.
```

**User Story 2: Wykrycie podejrzanej strony**
```
Jako obywatel, chcę zweryfikować stronę podszywającą się pod gov.pl, 
aby otrzymać ostrzeżenie przed wprowadzeniem danych.
```

**User Story 3: Szybka weryfikacja podstawowych informacji**
```
Jako obywatel, chcę zobaczyć podstawowe informacje o bezpieczeństwie strony, 
zanim rozpocznę proces weryfikacji QR.
```

### 2.3. Poza zakresem MVP (Out of Scope)

- **Pełna integracja z aplikacją mObywatel** (w MVP: symulacja)
- **Zaawansowana analiza certyfikatów SSL** (w MVP: podstawowa informacja o HTTPS)
- **Automatyczne wykrywanie podobieństwa domen** (typosquatting)
- **System zgłaszania podejrzanych stron**
- **Historia weryfikacji użytkownika**
- **Weryfikacja treści strony** (tylko weryfikacja domeny)
- **Wielojęzyczność** (tylko język polski)

---

## 3. Kryteria Sukcesu MVP

### 3.1. Metryki sukcesu

1. **Czas weryfikacji:** Proces weryfikacji (od kliknięcia przycisku do otrzymania wyniku) trwa poniżej 5 sekund
2. **Dokładność weryfikacji:** System poprawnie klasyfikuje domeny z listy oficjalnych gov.pl w 100% przypadków
3. **Bezpieczeństwo:** Każdy kod QR jest jednorazowy (nonce) i nie może być użyty ponownie
4. **Czytelność:** Użytkownik nie-techniczny jest w stanie przeprowadzić weryfikację bez instrukcji
5. **Wydajność:** Widget nie wpływa na czas ładowania strony (dodatkowe obciążenie < 100ms)

### 3.2. Akceptacja MVP

MVP jest uznane za gotowe, gdy:
- ✅ Wszystkie kluczowe funkcjonalności działają
- ✅ Przetestowano scenariusz pozytywny i negatywny
- ✅ Kod QR generuje jednorazowe tokeny
- ✅ Weryfikacja działa dla co najmniej 10 przykładowych domen
- ✅ Interfejs jest czytelny i intuicyjny

---

## 4. Realizacja Techniczna

### 4.1. Sugerowany stack technologiczny

#### 4.1.1. Frontend (Widget na stronie gov.pl)
- **Vanilla JavaScript** lub **React** (lekki komponent)
- **Biblioteka do generowania QR:** `qrcode.js` lub `qrcode.react`
- **CSS** dla stylizacji widgetu (możliwość dostosowania do designu gov.pl)

#### 4.1.2. Backend/API
- **Flask** lub **FastAPI** – lekkie frameworki do stworzenia API
- **Endpoints:**
  - `POST /api/verify/generate-qr` – generowanie kodu QR z nonce
  - `POST /api/verify/validate` – walidacja tokenu i weryfikacja domeny
  - `GET /api/domains/official-list` – lista oficjalnych domen (cache)

#### 4.1.3. Bezpieczeństwo
- **Generowanie nonce:** `secrets.token_urlsafe()` (Python) lub odpowiednik
- **Walidacja timestamp:** Token ważny przez 5 minut
- **HTTPS:** Wszystkie komunikacje szyfrowane
- **CORS:** Ograniczenie do domen gov.pl

#### 4.1.4. Dane
- **Lista domen:** Plik JSON z oficjalnymi domenami gov.pl
- **Storage nonce:** Tymczasowe przechowywanie w pamięci (Redis opcjonalnie dla skalowania)
- **Brak bazy danych:** MVP nie wymaga trwałego przechowywania danych

#### 4.1.5. Symulacja aplikacji mObywatel
- **Prosta aplikacja webowa** lub **strona demo** symulująca skanowanie QR
- **Możliwość wklejenia kodu QR** lub **screenshot QR** do analizy
- **Wyświetlenie wyniku weryfikacji** w formie komunikatu

### 4.2. Architektura MVP

```
┌─────────────────┐
│  Strona gov.pl  │
│  (Widget JS)    │
└────────┬────────┘
         │
         │ 1. Kliknięcie "Zweryfikuj"
         │ 2. Request: POST /generate-qr
         │
         ▼
┌─────────────────┐
│  Backend API    │
│  (Flask/FastAPI)│
│  - Generuje QR  │
│  - Waliduje     │
│  - Weryfikuje   │
└────────┬────────┘
         │
         │ 3. Zwraca QR z nonce
         │
         ▼
┌─────────────────┐
│  mObywatel      │
│  (Symulacja)    │
│  - Skanuje QR   │
│  - Wysyła verify│
└────────┬────────┘
         │
         │ 4. Request: POST /validate
         │
         ▼
┌─────────────────┐
│  Backend API    │
│  - Sprawdza nonce│
│  - Weryfikuje   │
│    domenę       │
└────────┬────────┘
         │
         │ 5. Zwraca wynik
         │
         ▼
┌─────────────────┐
│  Wynik          │
│  (mObywatel +   │
│   strona)       │
└─────────────────┘
```

### 4.3. Struktura danych

**Request: Generowanie QR**
```json
{
  "url": "https://example.gov.pl/page",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Response: Kod QR**
```json
{
  "qr_data": "verify://gov.pl?token=abc123&url=...",
  "nonce": "abc123...",
  "expires_at": "2024-01-01T12:05:00Z"
}
```

**Request: Walidacja**
```json
{
  "nonce": "abc123...",
  "url": "https://example.gov.pl/page"
}
```

**Response: Wynik weryfikacji**
```json
{
  "verified": true,
  "domain": "example.gov.pl",
  "is_official": true,
  "ssl_valid": true,
  "message": "Strona jest zaufana"
}
```

---

## 5. Ocena Wykonalności (Feasibility)

### 5.1. Możliwość wykonania w 48h: **Wysoka**

### 5.2. Uzasadnienie

**Zalety podejścia MVP:**
- ✅ **Brak pełnej integracji z mObywatel** – symulacja znacznie upraszcza implementację
- ✅ **Proste reguły weryfikacji** – sprawdzenie domeny na liście, bez zaawansowanej analizy
- ✅ **Minimalne zależności** – lekki backend, prosty frontend widget
- ✅ **Brak bazy danych** – lista domen w pliku JSON, nonce w pamięci
- ✅ **Gotowe biblioteki** – generowanie QR, walidacja URL

**Ryzyka i ograniczenia:**
- ⚠️ **Symulacja mObywatel** – nie jest to pełna integracja, ale wystarczająca do demonstracji
- ⚠️ **Podstawowa weryfikacja** – tylko sprawdzenie domeny, bez analizy treści
- ⚠️ **Brak produkcji** – rozwiązanie demo, wymagające dalszego rozwoju dla wdrożenia

**Podział czasu (szacunkowy):**
- Backend API (generowanie QR, walidacja): 8-10h
- Frontend widget: 6-8h
- Symulacja mObywatel: 4-6h
- Integracja i testy: 6-8h
- Dokumentacja i prezentacja: 4-6h
- **Razem: ~28-38h** (wystarczająco w zakresie 48h)

---

## 6. Plan implementacji (Roadmap MVP)

### Faza 1: Backend (12h)
1. Setup projektu i środowiska
2. Implementacja endpointów API
3. Generowanie nonce i kodów QR
4. Weryfikacja domen na podstawie listy JSON
5. Testy jednostkowe

### Faza 2: Frontend Widget (8h)
1. Stworzenie komponentu JavaScript
2. Integracja z biblioteką QR
3. Stylizacja widgetu
4. Integracja z backend API

### Faza 3: Symulacja mObywatel (6h)
1. Stworzenie prostej aplikacji demo
2. Funkcjonalność skanowania/symulacji QR
3. Wyświetlanie wyniku weryfikacji

### Faza 4: Integracja i testy (8h)
1. End-to-end testy scenariuszy
2. Testy bezpieczeństwa (nonce, replay attacks)
3. Optymalizacja wydajności
4. Poprawki błędów

### Faza 5: Dokumentacja (6h)
1. Dokumentacja techniczna
2. Instrukcja użycia
3. Przygotowanie prezentacji
4. Nagranie demo video

---

## 7. Następne kroki po MVP

Po zakończeniu MVP, możliwe rozszerzenia:
- Pełna integracja z aplikacją mObywatel
- Zaawansowana analiza certyfikatów SSL
- Wykrywanie typosquattingu
- System zgłaszania podejrzanych stron
- Dashboard administracyjny do zarządzania listą domen

