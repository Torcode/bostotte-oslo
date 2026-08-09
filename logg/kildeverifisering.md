# Kildeverifiseringslogg

Én rad per kontrollert oppføring eller kilde. «Verifisert» betyr at tittel,
utgiver og URL er kontrollert mot primærkilden på datoen som står; metadata i
`referanser.bib` er oppdatert i samme operasjon, og PLASSHOLDER-noten fjernet.
Resten av bibliografien beholder `note = {PLASSHOLDER --- verifiser}` til den
er kontrollert — `verifiser.R` teller gjenstående ved hver kjøring.

## Verifisert mot primærkilde

| Dato | Nøkkel/kilde | Kontrollert | Resultat |
|---|---|---|---|
| 2026-08-09 | `fn1948` | un.org, offisiell UDHR-side | Ny oppføring: res. 217 A (III), 10.12.1948; artikkel 25 omfatter bolig. Erstatter tidligere sitering i ren tekst |
| 2026-08-09 | `husbankenKanFaa` | husbanken.no | Tittel «Kan du få bostøtte?»; søknadsfrist den 25. og utbetaling den 20. bekreftet på siden |
| 2026-08-09 | `husbankenBeregning` | husbanken.no | Tittel «Beregning av bostøtte»; dekningsgraden 73,7 % står i beregningsoppsettet |
| 2026-08-09 | `husbankenInntekter` | husbanken.no | Tittel «Inntekter som er med i beregningen»; to-tredels-regelen for AAP/dagpenger i tre-utbetalingsmåneder sitert ordrett på siden |
| 2026-08-09 | `husbankenBoutgifter` | husbanken.no | Tittel «Boutgifter i beregningen»; godkjente boutgifter og øvre grense omtalt |
| 2026-08-09 | `husbankenStatistikk` | statistikk.husbanken.no/bostotte | Datakilden for uttrekket 4. august 2026; arkiverte rådata i `data/raw/` |
| 2026-08-09 | I18-sporet | altinget.no (statsrådens svar-seksjonen) | Skriftlig spørsmål om økt minstepensjon for enslige fra 1. mai 2025 og bostøtte-reduksjon dokumentert stilt (Kristjánsson → Brenna); selve svaret med tall var ikke maskinelt tilgjengelig i økten |

## Kontrollert tidligere (se endringsloggen)

Tre oppføringer verifisert mot primærkilde og rettet (én med feil tittel), og
fire ikke-verifiserbare fjernet — dokumentert i `logg/endringslogg-kap1-2.md`.
Regelverksregisterets kunnskapsdatoer (I01, I05, I12, I14–I17) er
primærkildebelagt i `revisjon/regelverksregister_kunnskapsdatoer.csv` med
Lovtidend-kunngjøringer, innstillinger og fremleggelser.

## Gjenstår

- 25 oppføringer med `PLASSHOLDER`-note (mest Husbanken-årsrapporter,
  SSB-tabellsider, NAV-sider og forskrifts-/lovreferanser). NAV- og
  Lovdata-sider er maskinstengt for henting; de må verifiseres manuelt.
- **I11**: månedsbeløpene for ekstrautbetalingene januar–april 2024 står som
  «delvis» — årsrapporten 2024 oppgir totalen (569 mill. til ca. 132 200
  husstander), ikke satsene per måned; satsene er antatt videreført fra
  desember 2023 og må bekreftes i forskriften eller Prop. 1 S (2023–2024).
- **I18**: forhåndsanslaget (13 000 nasjonalt) er belagt mot regjeringen.no i
  primærrunden 3. august, men ikke gjenfunnet i årsrapport 2025; det
  dokumenterte stortingsspørsmålet (over) er neste verifiseringssteg.

Rapporten kalles ikke kildeferdig før denne listen er tom.
