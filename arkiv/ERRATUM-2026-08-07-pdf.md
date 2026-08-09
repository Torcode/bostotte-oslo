# Erratum: bostotte_oslo.pdf, bygget 7. august 2026 (arkivert)

Denne PDF-en var leveransen til og med 9. august 2026 og er arkivert uendret
som revisjonsspor. Den skal ikke siteres for resultater. Fire grunner,
dokumentert i `revisjon/01_release_audit.md` og rettet i kilden samme dag:

1. Konformalkalibreringen brukte feil som ikke var realisert ved opprinnelsen
   (t_j < t_i i stedet for t_j + h <= t_i), uten endelig-utvalgsnivå.
   «45 → 73 %» er derfor for gunstig; tidsgyldig tall er 48 → 79 % på det
   navngitte kalibreringsutvalget.
2. Flaggskipsresultatet «15 093 fra ni måneders horisont» forutsatte
   regelverkskunnskap som først ble offentlig 6. oktober 2023
   (effect_known_from, primærkildebelagt). Point-in-time-formen er 15 552 mot
   15 588 (0,2 %) ved seks måneder; ni-månederstallet består kun som merket
   orakelscenario.
3. Tabell 17 og brødteksten i 4.5 blandet to evalueringsutvalg (372 mot 336)
   uten note.
4. 294 escapede tegnsekvenser (<U+00E5>, <U+00A0>) i maskingenererte tabeller
   og figuretiketter — prosessens locale flippet til C etter tegnsettvakten.

Gjeldende leveranse: `bostotte_oslo.pdf` i repo-roten, bygget fra kilden på
gren `revisjon/2026-08-09-audit` eller senere `main`.
