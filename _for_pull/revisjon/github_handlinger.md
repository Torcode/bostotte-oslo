# GitHub-handlinger, klare til utførelse (revisjon 2026-08-09)

Chrome-broen fikk ikke sendt skjemaer mot github.com i denne økten (klikk/tastetrykk
nådde ikke Reacts skjematilstand), og git-proxyen nekter push for dette repoet. Alt
under er derfor formulert ferdig — lim inn, eller gi økten push-tilgang så gjøres det
maskinelt. Ingen av handlingene er destruktive; lukkede issues og PR-er kan gjenåpnes.

## 1. Kommentar på #6 (behold åpen)

> **Revisjon 2026-08-09** (gren `revisjon/2026-08-09-audit`, fil
> `revisjon/regelverksregister_kunnskapsdatoer.csv`): kunnskapsdatoene er etablert fra
> primærkilder (Norsk Lovtidend, stortingsinnstillinger, regjeringen.no).
>
> - **I12** (avvikling, termin april 2024): foreslått **06.10.2023** (Prop. 1 S
>   (2023–2024)/A-til-Å), vedtatt 15.12.2023, forskrift FOR-2024-01-04-35
>   («oppheves 1. april 2024»), kunngjort 05.01.2024. `effect_known_from = 2023-10-06`.
> - I **juli 2023** var kunngjort sluttdato **31.12.2023** (FOR-2023-07-10-1262);
>   sluttdatoen ble lovfestet fem ganger før faktisk utløp. Manuell kontroll av
>   opprinnelse juli 2023 → april 2024: **ikke mulig som pseudo-sanntid** —
>   ni-månederstallet er en betinget orakelberegning.
> - PIT-formen av flaggskipet overlever og er sterkere: opprinnelse 2023-10 (første
>   etter kunngjøringen), h=6: **15 552 mot fasit 15 588 (0,2 %)** — tabell 19.
> - **I14/I15/I16** (høstpakken): oppsto i RNB-forliket (Innst. 447 S, 18.06.2024) —
>   ikke i Prop. 104 S (den hadde bare utgiftsanslag +232 mill.). Forskrifter
>   28.06 / 28.08 / 23.09.2024.
> - **I17**: budsjettforlik 01.12.2024 (ikke i Prop. 1 S 07.10.2024), forskrift
>   FOR-2024-12-19-3386. Innholdet er en «tre meldekortutbetalinger i samme måned
>   regnes med 2/3»-regel — etiketten «AAP/dagpenger-skjerming» bør presiseres.
>
> Designmerknad: «kunngjort sluttdato per opprinnelse» er en tredje informasjonsbane
> mellom K7-frysingen (konservativ nedre grense) og dagens fasitkalender (øvre) —
> solnedgangsdatoer var upålitelige prediktorer og skal ikke tolkes som framtidskunnskap.

## 2. Lukk #13 med kommentar

> Verifisert i revisjon 2026-08-09 (`revisjon/01_release_audit.md`): M10-rettelsen står
> i koden (vektorisert `str_detect` + `LAMBDA_ORAKEL`), begge invariansene finnes som
> `stopifnot` i qmd (M7 ≠ M6 der pakken er ute; M7 = M6 ellers), M10-loggen dokumenterer
> tallene (MASE −31,5 % på de 138 rammede punktene, dekning +16 pp), PDF regenerert i
> `7043473`, M7 er merket orakel/øvre grense i tabelltekst og brødtekst, og
> «tredjedel»-formuleringen er ute av kilden (0 grep-treff). Akseptansekriteriene er
> oppfylt; prosa-sweepen ligger i #15. Lukkes.

## 3. Kommentar på #17 (behold åpen)

> Revisjon 2026-08-09: fortsatt udekket i PDF-en (som nå er 38 sider): tabell 17 s. 30
> (73/42, N=372) mot brødtekst og figur 4 s. 32 (81/45, K-utvalget N=336) — uten note.
> Sidetallene i issue-teksten (29/31) er foreldet. Konformalrettingen på gren
> `revisjon/2026-08-09-audit` endrer K-tallene ved neste render; harmoniseringen bør
> gjøres i samme render.

## 4. Kommentar på #15 (behold åpen, innsnevret)

> Revisjon 2026-08-09: «opptil en tredjedel» er ute av kilden og M7-prosaen er
> inline-bundet — hoveddelen av issuen er løst av M10 + `7043473`. Gjenstår:
> (i) «innenfor tre prosent» om et 3,2 %-avvik (rettet på revisjonsgrenen, krever
> render); (ii) generell sweep for hardkodede kvantitative påstander i kapittel 4.

## 5. Lukk PR #12 som supersedert, med kommentar

> Lukkes som supersedert (revisjon 2026-08-09, jf. #1): main har allerede de
> verdifulle delene — `validate_phase1.py`, `ci.yml` og README ble hentet inn i
> `d0d1a40` — mens grenen bygger på utgått struktur (`unt_1.qmd`,
> `velferdsetaten-data/`, `docs/`-stillas) og står i konflikt. Ingen unike endringer
> gjenstår å portere; `docs/`-stillaset er erstattet av `logg/`-praksisen.

## 6. Lukk #1 med kommentar (etter 5)

> Avgjort i revisjon 2026-08-09: PR #12 er lukket som supersedert (begrunnelse der).
> Diffen er gjennomgått mot main: de 47 datakontrollene og CI virker på main; ingen
> referanser til `unt_1.qmd`/`velferdsetaten-data/` gjeninnføres; ingen unike
> kontroller gjenstår. Grenen `docs/phase-1-contract` kan slettes ved anledning.

## 7. Kommentar på #8 (foreslått lukking)

> Revisjon 2026-08-09: notebooks 01–07 oppfyller kjernekriteriene — kjørbare topp til
> bunn i Colab, data fra versjonert klone med sjekksum, fold-riktige trekk med
> lekkasjetest, regularisert regresjon (L0) og gradient boosting (G1/G2) mot naiv og
> sesongnaiv baseline, variabelviktighet omtalt ikke-kausalt. Gjenstår kun «gjenbrukbar
> logikk i testbar pakke» (protokollen er duplisert per notebook). Foreslår å lukke og
> flytte resten til eget issue eller #7.

## 8. Oppdatering av #18-typen (valgfritt)

Sidetall og tellinger i README er rettet på revisjonsgrenen; ingen issue-handling.
