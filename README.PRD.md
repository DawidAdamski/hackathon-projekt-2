# Product Requirements Document (PRD)
## Weryfikacja autentyczności stron gov.pl za pomocą aplikacji mobilnej mObywatel

---

## 1. Wprowadzenie

### 1.1. Opis organizacji i sytuacji
Oszustwa phishingowe w Polsce coraz częściej wykorzystują strony publiczne, takie jak portale administracji rządowej, serwisy samorządowe czy platformy usług publicznych. Cyberprzestępcy tworzą fałszywe kopie tych witryn, które wyglądają niemal identycznie jak oryginały, aby wzbudzić zaufanie użytkowników.

### 1.2. Problem do rozwiązania (The "Why")
**Główny problem:** Brak skutecznych, powszechnie dostępnych rozwiązań, które pomagałyby obywatelom w zapobieganiu oszustwom phishingowym na stronach rządowych. Cyberprzestępcy wykorzystują:
- Fałszywe kopie stron rządowych wyglądające identycznie jak oryginały
- Certyfikaty SSL i domeny łudząco podobne do oficjalnych
- Aktualne wydarzenia i komunikaty rządowe do uwiarygodnienia oszustwa

**Skutki:** Wyłudzanie danych logowania do usług ePUAP, Profilu Zaufanego, bankowości elektronicznej lub pozyskiwanie informacji osobowych do kradzieży tożsamości.

**Grupa docelowa:** Wszyscy obywatele korzystający z aplikacji mObywatel i potrzebujący weryfikacji strony podającej się za stronę rządową.

---

## 2. Proponowane rozwiązanie (The "What")

### 2.1. Główny cel
Stworzenie rozwiązania, które umożliwi weryfikację autentyczności rządowych stron internetowych przy pomocy aplikacji mobilnej mObywatel. Narzędzie ma być wbudowane na stronach gov.pl w łatwo dostępnym, ale niewpływającym na użyteczność innych funkcjonalności miejscu.

### 2.2. Kluczowe funkcjonalności

#### 2.2.1. Moduł weryfikacji na stronie gov.pl
- **Widoczny przycisk CTA** do weryfikacji strony za pomocą kodu QR – w łatwo dostępnym miejscu na stronie
- **Moduł z podstawowymi informacjami weryfikującymi bezpieczeństwo serwisu:**
  - Sprawdzenie, czy domena ma rozszerzenie .gov.pl
  - Link do kompendium stron rządowych, zawierającego listę oficjalnych portali
  - Informacja o certyfikacie SSL (np. "Zabezpieczona połączeniem HTTPS")

#### 2.2.2. Weryfikacja QR poprzez aplikację mObywatel
- Generowanie jednorazowego kodu QR (nonce) dla każdej sesji weryfikacji
- Zeskanowanie kodu QR w aplikacji mObywatel
- Weryfikacja autentyczności strony na podstawie:
  - Listy oficjalnych domen i subdomen gov.pl
  - Metadanych certyfikatów SSL
  - Walidacji parametrów URL

#### 2.2.3. Informacja zwrotna po weryfikacji
- **Scenariusz pozytywny:** Jasny komunikat "Strona jest zaufana" i ewentualne wskazówki do dalszego korzystania
- **Scenariusz negatywny:** Wyraźne ostrzeżenie wraz z instrukcją, co należy zrobić w przypadku potencjalnego zagrożenia
- Komunikat widoczny zarówno w aplikacji mObywatel, jak i na stronie internetowej

---

## 3. Wymagania techniczne

### 3.1. Bezpieczeństwo
- **Szyfrowana komunikacja** między aplikacją mObywatel a serwerem weryfikacji
- **Jednorazowe kody QR (nonce)** – zapobieganie spoofingowi i replay attacks
- **Ograniczenie ekspozycji danych** – minimalizacja przesyłanych informacji
- **Poprawna walidacja wejścia** – odporność na manipulację kodem QR oraz kluczowymi parametrami URL
- **Obsługa przypadków błędnych:**
  - Brak połączenia
  - Nieprawidłowy kod QR
  - Timeout sesji weryfikacji

### 3.2. Wydajność
- Moduł lekki, niewpływający na wydajność aplikacji mObywatel
- Szybka weryfikacja (cel: poniżej 3 sekund)
- Minimalne obciążenie strony gov.pl

### 3.3. Integracja
- Propozycja koncepcji mechanizmu integracji z aplikacją mObywatel
- Kompatybilność z istniejącą infrastrukturą gov.pl
- Możliwość wdrożenia jako moduł/widget na stronach rządowych

---

## 4. Dane i zasoby

### 4.1. Dostępne zasoby
- Lista oficjalnych domen i subdomen gov.pl w formacie JSON
- Przykładowy zbiór metadanych o certyfikatach SSL stosowanych na stronach administracji publicznej
- Sandbox z przykładowymi stronami (w tym strony symulującymi fałszywe witryny) do testów

### 4.2. Wymagane dane
- Baza danych oficjalnych domen gov.pl
- Metadane certyfikatów SSL dla stron rządowych
- Mechanizm aktualizacji listy zaufanych domen

---

## 5. Kryteria oceny

Rozwiązanie będzie oceniane pod kątem:

1. **Związek z wyzwaniem** — 25%
   - Czy rozwiązanie adresuje problem weryfikacji autentyczności stron gov.pl?
   - Czy odpowiada na potrzeby użytkowników?

2. **Wdrożeniowy potencjał rozwiązania** — 25%
   - Czy rozwiązanie może być wdrożone w rzeczywistej infrastrukturze?
   - Czy jest skalowalne i utrzymywalne?

3. **Walidacja i bezpieczeństwo danych** — 20%
   - Czy spełnia wymagania bezpieczeństwa?
   - Czy poprawnie weryfikuje autentyczność stron?

4. **UX i ergonomia pracy** — 15%
   - Czy interfejs jest czytelny dla użytkownika nie-technicznego?
   - Czy proces weryfikacji jest intuicyjny?

5. **Innowacyjność i prezentacja** — 15%
   - Czy rozwiązanie wprowadza nowe podejście?
   - Czy prezentacja jest przekonująca?

---

## 6. Oczekiwany rezultat (Deliverable)

### 6.1. Forma projektu
Prototyp rozwiązania, pozwalający na weryfikację autentyczności strony w domenie gov.pl za pomocą aplikacji mObywatel.

### 6.2. Wymagane elementy projektu
- Szczegółowy opis i tytuł projektu
- Prezentacja w formacie PDF (maksymalnie 10 slajdów)
- Makiet rozwiązania, prezentujące jego użyteczność
- Film umieszczony w dostępnym, otwartym repozytorium (link), trwający maksymalnie 3 minuty i prezentujący projekt

### 6.3. Dodatkowe elementy (opcjonalne)
- Repozytorium kodu
- Zrzuty ekranu
- Linki do demonstracji
- Materiały graficzne lub inne elementy związane z projektem

### 6.4. Scenariusze testowe
W trakcie prezentacji uczestnicy powinni zaprezentować:
- Scenariusz pozytywny weryfikacji strony przez obywatela
- Scenariusz negatywny weryfikacji strony przez obywatela
- Zgodność rozwiązania z makietami (lo-fi)

---

## 7. Potencjalne wyzwania i ryzyka

### 7.1. Wyzwania techniczne
- **Integracja z mObywatel:** Wymaga znajomości API i architektury aplikacji
- **Generowanie bezpiecznych kodów QR:** Implementacja mechanizmu nonce i walidacji
- **Weryfikacja certyfikatów SSL:** Pobieranie i analiza metadanych certyfikatów w czasie rzeczywistym
- **Wydajność:** Zapewnienie szybkiej weryfikacji bez obciążania aplikacji

### 7.2. Wyzwania bezpieczeństwa
- **Ochrona przed spoofingiem:** Zabezpieczenie kodów QR przed podrobieniem
- **Ochrona przed replay attacks:** Właściwa implementacja mechanizmu nonce
- **Walidacja danych:** Odporność na manipulację parametrami URL i kodami QR

### 7.3. Wyzwania UX
- **Intuicyjność:** Uproszczenie procesu weryfikacji dla użytkowników nie-technicznych
- **Komunikacja błędów:** Jasne komunikaty w przypadku problemów z weryfikacją
- **Integracja wizualna:** Wkomponowanie modułu w istniejące strony gov.pl

---

## 8. Kontekst wdrożeniowy

Najlepsze rozwiązania mogą zostać skierowane do pilotażowego wdrożenia w procesie rozwoju aplikacji mObywatel. Organizator przewiduje możliwość kontynuowania prac projektowych po hackathonie.

---

## 9. Kontakt i wsparcie

Podczas wydarzenia dostępni będą:
- Mentorzy techniczni i merytoryczni w specjalnie oznaczonym punkcie konsultacyjnym
- Kanał komunikacyjny na Discord z dostępem do zasobów i dokumentacji

