# NONCE upon a time

## In SHORT

Pokazujemy kompletny przepływ weryfikacji stron przez mObywatela — od kliknięcia w widget, po potwierdzenie w aplikacji.

**Co zrobiliśmy:**

- Zbudowaliśmy **backend**, który generuje jednorazowe tokeny (nonce), zapisuje je z czasem ważności i statusem oraz sprawdza, czy domena jest zaufana.
- Stworzyliśmy **frontowy widget**, który pobiera token z backendu, wyświetla z niego **QR kod** i cyklicznie sprawdza status weryfikacji.
- Przygotowaliśmy **symulowaną aplikację mObywatel**, która skanuje QR, wysyła token do backendu i odblokowuje proces.
- Dorzuciliśmy **fake-frontend**, żeby pokazać, że niezaufana domena nie przejdzie procesu.

**Jak to działa:**

1. Użytkownik klika „Zweryfikuj tę stronę”.
2. Widget pyta backend o token → backend sprawdza domenę → generuje nonce.
3. Widget wyświetla QR zakodowany tokenem.
4. „Aplikacja” mObywatel skanuje QR i wysyła token do backendu.
5. Backend oznacza token jako zweryfikowany.
6. Widget dostaje potwierdzenie i kończy proces.
7. Jeśli token wygasł, jest niepoprawny lub domena nie jest zaufana → proces zatrzymany.

**Efekt:**
Mamy działające MVP pokazujące pełny flow weryfikacji strony przez mObywatela, z kontrolą domeny, ważności tokenów i komunikacją między trzema niezależnymi modułami.

## Detale implementacji MVP

### Uruchomienie wersji MVP

Całość jest skonteneryzowana i składa się z 3 głównych modułów:

- `backend` – serwer API zarządzający tokenami i weryfikacją
- `legit-front` – mock strony gov z komponentem JS generującym okno z kodem QR
- `mObywatel` – symulowana aplikacja mObywatel do skanowania kodu QR i weryfikacji

Katalog projektu zawiera plik `docker-compose.yml`, który definiuje usługi dla każdego z modułów.
Aby uruchomić wersję MVP, wykonaj:

```bash
docker compose up --build -d
```

Wersja demonstracyjna działa lokalnie i wymaga dodania reguł do pliku `/etc/hosts`, żeby poprawnie symulować działanie systemu. Reguły:

```bash
127.0.0.1 podatki.gov
127.0.0.1 mobywatel
```

- domena `podatki.gov` – symuluje stronę gov.pl z widgetem do weryfikacji
- domena `mobywatel` – symuluje aplikację mObywatel
- serwis `backend` ma w demonstracyjnej liście zaufanych domen dodaną domenę `podatki.gov`, z której możliwe jest przeprowadzenie symulacji prawidłowego przebiegu weryfikacji

Po przygotowaniu środowiska demonstracyjnego serwisy są dostępne kolejno pod adresami:

- mock aplikacji mObywatel — `http://mobywatel:7777/`
- mock strony gov z widgetem — `http://podatki.gov:8888/`

### Backend (verifier)

Moduł `backend`:

- odpowiada za zarządzanie tokenami
- zawiera reguły walidacyjne oraz zbiór „trusted” domen
- weryfikuje requestory i zarządza cyklem życia tokenów
- komunikuje się z komponentem `legit-front` oraz aplikacją mObywatel (symulowaną)
- wystawia API dla modułu `legit-front` oraz aplikacji mObywatel

#### Scope MVP dla modułu `backend`

1. Setup projektu i środowiska
2. Implementacja endpointów API
3. Generowanie nonce i kodów QR
4. Weryfikacja domen na podstawie listy JSON
5. Testy jednostkowe
6. Konfiguracja i konteneryzacja

### Frontend Widget

Moduł `legit-front`:

- symulowana strona gov.pl
- zawiera okno „popup” z przyciskiem do weryfikacji strony przez aplikację mObywatel
- przygotowuje i wyświetla kod QR w modalu
- przyjmuje dane z modułu `backend` i na ich podstawie wyświetla reprezentację tokena w formie kodu QR
- odpytuje `backend` o stan weryfikacji tokena — czy użytkownik zeskanował kod QR i czy strona jest zaufana

#### Scope MVP dla modułu `legit-front`

1. Stworzenie komponentu JavaScript
2. Integracja z biblioteką QR
3. Stylizacja widgetu
4. Integracja z backend API
5. Konfiguracja i konteneryzacja

### Symulacja mObywatel

Moduł `mObywatel`:

- symulowana aplikacja mObywatel
- komunikuje się z `backend` używając tokena z kodu QR
- mock ma pokazywać przebieg procesu weryfikacji
- wyświetla dane przygotowane przez `backend`

#### Scope MVP dla modułu `mObywatel`

1. Stworzenie aplikacji demo
2. Funkcjonalność skanowania/symulacji QR
3. Wyświetlanie wyniku weryfikacji
4. Konfiguracja i konteneryzacja

### Integracja i testy

1. Testy jednostkowe komponentow backendu (komenda `pytest` w katalogu `backend` po instalacji paczek z pliku `requirements.txt`)
2. Manualna weryfikacja przepływu end-to-end

### `fake-frontend` – dodatkowy moduł do testów

- WIP
- symulowana podrobiona strona podszywająca się pod gov.pl
- inna domena, która generuje linki niepojawiające się w repozytorium tokenów
- używana do symulacji

### Dokumentacja

1. Dokumentacja
2. Instrukcja użycia
3. Przygotowanie prezentacji
4. Nagranie demo video

## Opis działania serwisu i kluczowych komponentów

- po naciśnięciu przycisku „Zweryfikuj tę stronę w mObywatel” widget wysyła informację do backendu
- backend odbiera wiadomość i wstępnie weryfikuje requestora, sprawdzając:
  - czy pochodzi z domeny `.gov`
  - czy znajduje się na liście zaufanych domen

- dla pomyślnej weryfikacji backend generuje unikalny token (nonce) i zapisuje go w `TokenService`
  - na potrzeby demo tokeny są trzymane w pamięci — w przyszłości można je przenieść np. do Redis

- token zawiera dodatkowe informacje:
  - dla jakiej domeny został wygenerowany
  - flagę statusu weryfikacji (czy kod QR został zeskanowany)
  - timestamp wygenerowania — potrzebny do unieważniania tokenów po czasie (aktualnie 60s)

- po zapisie backend zwraca dane do widgetu, który generuje kod QR w przeglądarce
- pozytywna odpowiedź backendu uruchamia w widgetcie pętlę sprawdzającą status weryfikacji
- zeskanowanie kodu QR przez mObywatel powoduje wysłanie requestu do backendu — token dostaje flagę „verified”, co kończy pętlę
- aplikacja mObywatel dostaje informację o statusie oraz dane wyciągnięte z certyfikatu SSL (w demo użyto przykładowych dla gov.pl)
- w przypadku wygaśnięcia tokena, nieprawidłowego tokena lub braku certyfikatu SSL backend zwróci negatywną weryfikację
