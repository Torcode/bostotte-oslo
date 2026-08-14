# Render-notat for point-in-time-porten (issue #6, gren revisjon/2026-08-09-audit)

Grenen endrer beregningsgrunnlaget i `bostotte_oslo.qmd` og krever én full render
(`quarto render bostotte_oslo.qmd`, ca. 20 min første gang — kryssvalideringen
kjøres nå for to informasjonssett). Renderen skal skje i et miljø der
tegnsettvakten faktisk stopper, så escapene i dagens PDF dør i samme operasjon.

## Hva som er endret i beregningen

1. **PIT-port** (`pit_gate` i res-cv-chunken): ved hver opprinnelse brukes bare
   regelverkssteg med `effect_known_from` ≤ utgangen av opprinnelsesmåneden
   (`data/clean/regelverk_kunnskap.csv`, primærkildebelagt). Ukjente steg bærer
   siste kjente verdi videre. k_pre/k_post-skillet gates på I17
   (kjent 2024-12-17). Treningsdata røres ikke.
2. **To kjøringer**: `cv` (PIT, hovedløp — alle tabeller og inline-tall) og
   `cv_fasit` (dagens fulle kalender, merket orakel/scenario; brukes bare i
   tbl-res-april-kolonnen og der teksten eksplisitt sier det).
3. **Konformal**: tidsgyldig skjema + endelig-utvalgsnivå (fra forrige commit).
4. Tre stopifnot-kontroller på porten (juli/oktober 2023, november 2024) og én
   på PIT==fasit for opprinnelser ≥ 2024-12.

## Hva som VIL flytte seg ved render, og må leses etterpå

- **Tabell 17** (samlet): M4–M7-radene blir PIT-tall — MASE for M5/M6/M7 vil
  stige på lange horisonter (K7 tilsier retning: mot/over naiv ved h 6–12).
  M0–M3 er upåvirket. Kontroller at prosaen i 4.1–4.2 fortsatt stemmer.
- **Tabell 19** (april): M6-kolonnen er nå PIT (h ≥ 7 vil ligge nær 19–20 000);
  ny merket kolonne «M6, fasitkalender (orakel)» bærer de gamle tallene
  (15 093 ved h = 9). Flaggskipsavsnittet er skrevet om til å peke riktig.
- **4.5/tabellene for dekning**: K-tallene er nå tidsgyldige + korrigerte;
  «45 → 73» erstattes av de nye verdiene. #17-harmoniseringen (utvalg 372 mot
  336) står IGJEN å gjøre i teksten — gjør den i samme render-runde.
- **T-oppgjøret (4.8)**: T1/T2/T5-radene må leses på nytt mot PIT-tallene.
- **tbl-res-overgang og skjevhetstabellen**: bygger på R (PIT) — verifiser at
  tolkningsprosaen holder.
- **README «Hovedfunn»**: avsnittet med 15 093 må oppdateres etter render
  (README er ellers rettet på grenen).
- Clark–West-tabellen: par som involverer M5/M6 endres; les konklusjonene på nytt.

## Kontrollrekkefølge etter render

1. `python scripts/validate_phase1.py` (55 kontrakter, inkl. det nye
   kunnskapsregisteret med I12-anker).
2. `source("verifiser.R")` — skal nå stoppe på escapede tegn.
3. Gullsettet (`revisjon/gullsett_referanse.csv`): L0/G2-referansene er
   notebook-side og upåvirket av qmd-porten; bruk dem uendret.
4. Diff gamle mot nye tabell 17/19-tall og arkiver gammel PDF med erratum-note
   (M15/K3, #17, PIT) før den nye sjekkes inn.
