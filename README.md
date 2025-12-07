# NONCE upon a time

## Uruchomienie wersji MVP

Calość jest skonteneryzowana i sklada sie z 3 głównych modułów:

- `backend` - serwer API zarzadzajacy tokenami i weryfikacja
- `legit-front` - mock strony gov z komponentem JS generujacym okno z kodem QR
- `mObywatel` - symulowana aplikacja mObywatel do skanowania kodu QR i weryfikacji

Katalog projektu zawiera plik `docker-compose.yml`, który definiuje usługi dla każdego z modułów.
Aby uruchomić wersję MVP, wykonaj następujące kroki:

```bash
docker compose up --build -d
```

Wersja demonstracyjna dziala lokalnie i wymaga dodania regul do pliki `/etc/hosts` zeby poprawnie symulowac dzialanie
systemu. Regoly do dodania:

```bash
127.0.0.1 podatki.gov
127.0.0.1 mobywatel
```

- domena `podatki.gov` - symuluje strone gov.pl z widgetem do weryfikacji
- domena `mobywatel` - symuluje aplikacje mObywatel
- serwis `backend` w demonstracyjnej liscie dozwolonych domen mam dodana domene: `podatki.gov`, z tej domeny mozliwe
  jest przeprowadzenie symulacji prawidlowego przebiegu weryfikacji.

Po przygotowaniu srodowiska demonstracyjen serwisy sa dostepne kolejno pod adresami:

- mock aplikacji mobywatel `http://mobywatel:7777/`
- mock strony gov z widgetem `http://podatki.gov:8888/`

## Elementy projektu oraz ich implementacja

### Backend (verifier)

Moduł `backend`:

- odpowiedzialny za zarzadzanie tokenami
- zawiera regoly validacyjne oraz zbior "trusted" domen
- weryfikuje requestorw i zarzadza cyklem zycia tokenow
- komunikuje sie z komponentem `legit-front` oraz aplikacja mObywatel (symulowana)
- wystawia API dla modulu `legit-front` oraz aplikacji mObywatel

#### Scope MVP dla modulu `backend`

1. Setup projektu i środowiska
2. Implementacja endpointów API
3. Generowanie nonce i kodów QR
4. Weryfikacja domen na podstawie listy JSON
5. Testy jednostkowe
6. Konfiguracja i konteneryzacja

### Frontend Widget

Moduł `legit-front`:

- symulowana strona gov.pl
- zawiera okno "popup" z przyciskiem do weryfikacji strony poprzez aplikację mObywatel
- przygotowuje i wyswietla QR kod w modalu modalu
- przyjmuje dane z modulu `backend` i na jego podstawie wyswietla jego reprezentacj w postaci kody QR
- odpytuje `backend` o stan weryfikacji tokena - czy urzytkownik zeskanowal kod QR i czy strona jest zaufana

#### Scope MVP dla modulu `legit-front`

1. Stworzenie komponentu JavaScript
2. Integracja z biblioteką QR
3. Stylizacja widgetu
4. Integracja z backend API
5. Konfiguracja i konteneryzacja

### Symulacja mObywatel

Moduł `mObywatel`:

- symulowana aplikacja mObywatel
- komunikuje sie po API z modulem `backend` uzywajac udostepnionego API i tokena z kodu QR
- mock strony ma na celu zedemonstrowac przebieg procesu
- komunikuje sie z modulem `backend` i wyswietla dane przygotowane prze `backend`

#### Scope MVP dla modulu symulacji `mObywatel`

1. Stworzenie aplikacji demo
2. Funkcjonalność skanowania/symulacji QR
3. Wyświetlanie wyniku weryfikacji
4. Konfiguracja i konteneryzacja

### Integracja i testy

1. End-to-end testy scenariuszy
2. Testy bezpieczeństwa (nonce, replay attacks)
3. Poprawki błędów

### `fake-frontend` - dodatkowy moduł do testów

- WIP
- symulowana podrobiona strona podszywajaca sie pod gov.pl
- inna domena ktora generuje linki ktore nie sa zapisywane w rpozytorium tokenow
- na potrzeby symulacji

### Dokumentacja

1. Dokumentacja
2. Instrukcja użycia
3. Przygotowanie prezentacji
4. Nagranie demo video

## Opis dzialania serwisu i kluczowych komponentow

- po naduszeniu przycisku "Zweryfikuj tę stronę w mObywatel" widget wysyla informace do backendu
- backend odbiera wiadomosc i wstepnie weryfikuje requestora, sprawdzajac:
  - czy requestor pochodzi z domeny .gov
  - czy znajduje sie na liscie zaufanych domen
- dla pomyslnej weryfikacji backend generuje unikalny token (nonce) oraz zapisuje go uzywajac `TokenService`
  - na potrzeby demonstracji token serwis trzyma tokeny w pmaieci - w przyszloci mozna zaimplementowac przevchowywanie
    tokenow w zewnetrznym serwisie na przyklad w REDIS - wystarczy zmodufikowac implemntacje metod clasy `TokenService`
- tokeny zapisywane sa z dodatkowymi informacjami:
  - dla jakiej domeny zostal wygenerowany token
  - flaga statusu weryfikacji (czy qr kod zostal zeskanowany)
  - czas wygenerowania tokena - potrzebny do invalidacji tokena po okreslonym czasie (aktualnie 60s)
- po zapisie backend zwraca informacje do widgetu z wygenerowanym tokenem na podstawie ktorego widget generuje kod QR w
  przegladarce uzytkownika
- pozytywna odpowiedz z backendu wyzwala w widgecie akcje sprawdzajaca status weryfikacji - to jest czy qr kod zostal
  zeskanowany
- zeskanowanie kodu QR przez aplikacje mObywatel (symulowana) powoduje wyslanie requestu do backendu z tokenem dla
  jakiego QR kod zostal wygenerowany - odpowiednia flaga jest ustawiona dla tego tokena co przerywa petle sprwadzajca
- po zeskananiu kodu qr aplikacja mobuwatel dostaje informacje o sttusie weryfikacji oraz dodatkowe informacje
  wyciagniete z certyfkatu SSL (w wersji demo sa przykladowe dla domeny gov.pl)
- w przyadku wygasnienac tokena lub nieprawidlowego tokena lub braku certyfikatu ssl dla powiazanej domeny backend
  zwroci informacje o negatywnej weryfikacji

## Wymagane elementy projektu

- Szczegółowy opis i tytuł projektu
- Prezentacja w formacie PDF (maksymalnie 10 slajdów)
- Makieta rozwiązania, prezentujące jego użyteczność
- Film umieszczony w dostępnym, otwartym repozytorium (link), trwający maksymalnie 3 minuty

**Dodatkowo (opcjonalnie):**

- Repozytorium kodu
- Zrzuty ekranu
- Linki do demonstracji
- Materiały graficzne
