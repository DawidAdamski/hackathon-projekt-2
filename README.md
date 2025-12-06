# Weryfikacja autentyczności stron gov.pl za pomocą aplikacji mobilnej mObywatel

## Przegląd projektu

Projekt ma na celu stworzenie rozwiązania, które pozwoli obywatelom na wiarygodną weryfikację stron w domenach administracji publicznej (gov.pl). W związku z rosnącą liczbą prób oszustw wykorzystujących strony stylizowane na strony rządowe i podszywanie się pod dostawców usług publicznych, potrzebna jest prosta i szybka ścieżka pozwalająca na sprawdzenie przez obywatela wiarygodności takich stron.

## Problem

Oszustwa phishingowe w Polsce coraz częściej wykorzystują strony publiczne, takie jak portale administracji rządowej, serwisy samorządowe czy platformy usług publicznych. Cyberprzestępcy tworzą fałszywe kopie tych witryn, które wyglądają niemal identycznie jak oryginały, aby wzbudzić zaufanie użytkowników. Najczęściej celem jest wyłudzenie danych logowania do usług ePUAP, Profilu Zaufanego, bankowości elektronicznej lub pozyskanie informacji osobowych.

**Brakuje obecnie skutecznych, powszechnie dostępnych rozwiązań**, które pomagałyby obywatelom w zapobieganiu tego typu oszustwom.

## Rozwiązanie

Stworzenie narzędzia wbudowanego na stronach gov.pl, które umożliwia weryfikację autentyczności strony poprzez zeskanowanie kodu QR w aplikacji mobilnej mObywatel. Rozwiązanie obejmuje:

- **Moduł weryfikacji na stronie gov.pl** z przyciskiem CTA i podstawowymi informacjami o bezpieczeństwie
- **Generowanie jednorazowego kodu QR** (nonce) dla każdej sesji weryfikacji
- **Weryfikacja w aplikacji mObywatel** na podstawie listy oficjalnych domen gov.pl
- **Jasna informacja zwrotna** o wyniku weryfikacji (pozytywny/negatywny)

## Dokumentacja projektu

- **[README.PRD.md](README.PRD.md)** - Product Requirements Document zawierający szczegółowe wymagania produktu, funkcjonalności, wymagania techniczne i kryteria oceny
- **[README.MVP.md](README.MVP.md)** - Minimum Viable Product zawierający zakres MVP, kryteria sukcesu, realizację techniczną i plan implementacji

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

## Wymagania techniczne

- **Bezpieczeństwo:** Szyfrowana komunikacja, jednorazowe kody QR (nonce), walidacja wejścia
- **Wydajność:** Lekki moduł, niewpływający na wydajność aplikacji
- **Integracja:** Kompatybilność z aplikacją mObywatel i infrastrukturą gov.pl

## Kryteria oceny

1. **Związek z wyzwaniem** — 25%
2. **Wdrożeniowy potencjał rozwiązania** — 25%
3. **Walidacja i bezpieczeństwo danych** — 20%
4. **UX i ergonomia pracy** — 15%
5. **Innowacyjność i prezentacja** — 15%

## Dostępne zasoby

- Lista oficjalnych domen i subdomen gov.pl w formacie JSON
- Przykładowy zbiór metadanych o certyfikatach SSL
- Sandbox z przykładowymi stronami (w tym strony symulującymi fałszywe witryny)

## Kontekst wdrożeniowy

Najlepsze rozwiązania mogą zostać skierowane do pilotażowego wdrożenia w procesie rozwoju aplikacji mObywatel. Organizator przewiduje możliwość kontynuowania prac projektowych po hackathonie.

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

## Kontakt i wsparcie

Podczas wydarzenia dostępni będą:
- Mentorzy techniczni i merytoryczni w specjalnie oznaczonym punkcie konsultacyjnym
- Kanał komunikacyjny na Discord z dostępem do zasobów i dokumentacji

---

**Źródło:** [Zadanie/PRAWDA_W_SIECI.md](Zadanie/PRAWDA_W_SIECI.md)
