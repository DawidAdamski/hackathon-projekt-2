# Prawda W sieci

## Elementy projektu

`legit-front`

- symulowana strona gov.pl
- zawiera okno "popup" z przyciskiem do weryfikacji strony poprzez aplikację mObywatel
- przyjmuje dane z modulu `backend` i na jego podstawie wyswietla jego reprezentacj w postaci kody QR
- odpytuje `backend` o stan weryfikacji tokena - czy urzytkownik zeskanowal kod QR i czy strona jest zaufana

W skrocie tutaj jest:

- przycisk z modalem i wyswietlaniem kody QR

`backend`

- odpowiedzialny za zarzadzanie tokenami
- zawiera regoly validacyjne oraz zbior "trusted" domen
- weryfikuje requestorw i zarzadza cyklem zycia tokenow
- komunikuje sie z komponentem `legit-front` oraz aplikacja mObywatel (symulowana)
- wystawia API dla modulu `legit-front` oraz aplikacji mObywatel

`mObywatel`

- symulowana aplikacja mObywatel
- komunikuje sie po API z modulem `backend` uzywajac udostepnionego API i tokena z kodu QR
- mock strony ma na celu zedemonstrowac przebieg procesu
- komunikuje sie z modulem `backend` i wyswietla dane

## Kluczowe funkcjonalności

1. **Widget na stronie gov.pl**
   - Przycisk CTA do weryfikacji za pomocą kodu QR
   - Podstawowe informacje o bezpieczeństwie (domena .gov.pl, certyfikat SSL)
   - Link do kompendium stron rządowych

2. **Weryfikacja QR**
   - Generowanie jednorazowego kodu QR z nonce
   - Zeskanowanie w aplikacji mObywatel
   - Weryfikacja na podstawie listy oficjalnych domen

3. **Wynik weryfikacji**
   - Komunikat "Strona jest zaufana" (scenariusz pozytywny)
   - Ostrzeżenie z instrukcjami (scenariusz negatywny)
   - Widoczny w aplikacji mObywatel i na stronie

## Kryteria oceny

1. **Związek z wyzwaniem** — 25%
2. **Wdrożeniowy potencjał rozwiązania** — 25%
3. **Walidacja i bezpieczeństwo danych** — 20%
4. **UX i ergonomia pracy** — 15%
5. **Innowacyjność i prezentacja** — 15%

## Wymagane elementy projektu

- Szczegółowy opis i tytuł projektu
- Prezentacja w formacie PDF (maksymalnie 10 slajdów)
- Makiet rozwiązania, prezentujące jego użyteczność
- Film umieszczony w dostępnym, otwartym repozytorium (link), trwający maksymalnie 3 minuty

**Dodatkowo (opcjonalnie):**

- Repozytorium kodu
- Zrzuty ekranu
- Linki do demonstracji
- Materiały graficzne
