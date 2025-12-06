# SHORT INFO

## User koncowy

- wszyscy obywatele korzystający z aplikacji mObywatel
- wszycy potrzebujący weryfikacji strony podającej się za stronę rządową

## TODO

Widoczny przycisk CTA do weryfikacji strony za pomocą kodu QR – w łatwo
dostępnym miejscu na stronie.

#question jak mam to osadzic? moge zrobic mock - przycisk potem ktos doda

• Moduł z podstawowymi informacjami weryfikującymi bezpieczeństwo serwisu
#question jak? po kliknieciu moge zweryfikowac certy jesli idze z legitnej strony

• Sprawdzenie, czy domena ma rozszerzenie .gov.
#question co z man in the middle? albo jak ktos ma fake strone i forwarduje akcje przyciku?

• Link do kompendium stron rządowych, zawierającego listę oficjalnych portali.
#question link? moge zrobic ale nie osadze tego na MVP

• Informacja o certyfikacie SSL (np. „Zabezpieczona połączeniem HTTPS”).
#question gdzie to info ma byc? api moze zwracac do mobywatel ale na strone tego raczej nie wrzuce

• Weryfikacja (np. jednorazowym kodem QR) poprzez zeskanowanie w aplikacji
mObywatel:

• Informacja zwrotna po weryfikacji: Widoczny komunikat w aplikacji i na stronie,
potwierdzający wynik weryfikacji. Scenariusz pozytywny: jasny komunikat „Strona
jest zaufana” i ewentualne wskazówki do dalszego korzystania. Scenariusz
negatywny: wyraźne ostrzeżenie wraz z instrukcją, co należy zrobić w przypadku
potencjalnego zagrożenia

## Schemat

gdzie generowac qr kod?

- w backendzie w govpl
- qr trafia na fe do usera na przegladarke
- potem skan QRkodu
- user skanuje i wysyla POST 
