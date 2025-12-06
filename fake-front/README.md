# Legit Front – legitna gov-strona

- np. `https://podatki.gov.local`
- ma przycisk „Zweryfikuj stronę w mObywatel”
- po kliknięciu:
  - robi `POST /verify/session` do Verifiera,
  - dostaje `nonce` + `qr_payload`,
  - pokazuje QR (albo chociaż tekst `mobywatel://verify?nonce=...`),
  - zaczyna polling `/verify/result?nonce=...`.

## Co to jest

- symuluje legitna strone rzadowa w domenie `.gov`.
- ma przycisk ktory komunikuje sie z kontenerem Verifiera, zeby wygenerowac QR kod do weryfikacji.
- ten QR kod pod spodem musi wygenerowac jakis secret i go zapisac do jakiejs bazy do ktorej bedzie mial wlote backend
  obslugujacy mObywatela
- jak to sie zapisze to QR kod wraca na frontedn
