# Legit Front – legitna gov-strona

- np. `https://podatki.gov.local`
- ma przycisk „Zweryfikuj stronę w mObywatel”
- po kliknięciu:
  - robi `POST /verify/session` do Verifiera,
  - dostaje `nonce` + `qr_payload`,
  - pokazuje QR (albo chociaż tekst `mobywatel://verify?nonce=...`),
  - zaczyna polling `/verify/result?nonce=...`.
