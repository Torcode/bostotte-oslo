# Evidensregister

Registeret skiller mellom en påstand, hvor evidensen finnes, og hvor langt verifikasjonen faktisk har kommet. «Data verifisert» betyr ikke automatisk at bibliografiske metadata eller en kausal tolkning er verifisert.

| ID | Påstand eller bruk | Primærkilde | Repoartefakt | Status | Neste kontroll |
|---|---|---|---|---|---|
| E-001 | Husbankens statistikkbank inneholder månedlige mål for termin, utbetaling, beløp, Oslo, bydeler og brukergrupper. | [Husbankens statistikkbank](https://statistikk.husbanken.no/bostotte), Qlik-app ee185fe5-e94d-463e-bff8-cd1c5f2f566f | velferdsetaten-data/scripts/extract_bostotte_v2.py og data/raw/husbanken_bostotte_*.csv | Data og uttrekkskode verifisert for vintage 2026-08-04 | Re-kjør uttrekk i dokumentert miljø og test skjemaendring |
| E-002 | Termin $t$ tilsvarer utbetaling $t+1$ i det frosne uttrekket. | Samme Qlik-datamodell for begge mål | scripts/validate_phase1.py og velferdsetaten_data.R | Reprodusert: 198/198 månedspar | Bevar kontrollen for hver ny vintage |
| E-003 | Bydeler og fem brukergrupper summerer til Oslo-totalen. | Husbankens Qlik-datamodell | Tre Oslo-filer i data/raw | Reprodusert for alle additive mål og måneder | CI-port på hver endring |
| E-004 | Juli 2026 er sanntidskant: utbetaling finnes, termin står som 0. | Husbankens uttrekk 2026-08-04 | husbanken_bostotte_oslo_manedlig.csv | Verifisert i fil | Gjør regelen robust for nye vintager |
| E-005 | Oslo/Bærum hadde 15 260 kr i gjennomsnittlig månedsleie for toroms bolig i 2025. | [SSB 09895](https://www.ssb.no/statbank/table/09895/) | ssb_09895_leiemarked_oslo.csv og R-kontroll | Reprodusert i eksisterende QA | Verifiser tabellfotnoter og presis ordlyd i rapport |
| E-006 | Husleie-KPI og total KPI kan brukes som eksterne prisserier. | [SSB 03013](https://www.ssb.no/statbank/table/03013/) og [SSB 14710](https://www.ssb.no/statbank/table/14710/) | fetch_ssb.py og data/clean | Data hentet | Dokumenter publiseringslag og transformasjon før modellbruk |
| E-007 | Oslo-bydelsdata finnes for AAP, uføretrygd, sosialhjelp, befolkning og framskriving. | [Oslo kommunes statistikkbank](https://statistikkbanken.oslo.kommune.no/) | fetch_oslo_statbank.py og data/clean/oslo_*.csv | Data hentet og kodebokført | Verifiser tabellmetadata og konsistente bydelsgrenser |
| E-008 | Midlertidig redusert progressivt egenandelsledd gjaldt fra termin desember 2021 til og med mars 2024. | Husbankens årsrapporter og regelverksveileder | intervensjonstabell.csv, arkiverte rapporter | Kildehenvisning registrert; bibliografisk kontroll gjenstår | Kontroller side, ordlyd og virkningsdato mot primær-PDF |
| E-009 | Flere regelendringer i 2024 må dateres separat i terminkalenderen. | Husbankens årsrapport 2024 og revidert nasjonalbudsjett | intervensjonstabell.csv | Hendelser registrert | Fullfør primærkildekontroll før modellspesifikasjon |
| E-010 | Fra januar 2025 skjermes tre meldekortutbetalinger ved at to tredeler medregnes. | KDD/Husbanken-regelverk | intervensjonstabell.csv og teori-/metodeutkast | Mekanisme kildebelagt i utkast; bibliografisk kontroll gjenstår | Verifiser primærtekst og implementeringsdato |
| E-011 | Volatiliteten i gruppen med midlertidige trygdeytelser falt fra 2024 til 2025. | Husbankens brukergruppeserie | velferdsetaten_data.R og metodeutkast | Deskriptiv kontroll i frosset vintage | Gjenta fold-/periodeuavhengig og unngå kausal språkbruk |
| E-012 | Historikken i Qlik kan revideres bakover og eldre vintager er ikke offentlig tilgjengelige. | Husbankens statistikkbank og uttrekksobservasjon | datakilder.md og kodebok.md | Dokumentert som kildebegrensning | Søk eksplisitt kildebekreftelse eller API-metadata |
| E-013 | Rapportens faglitteratur og offentlige kilder er korrekt bibliografert. | Originalartikler og primærkilder | referanser.bib | **Ikke ferdig:** plassholdermerking finnes | Verifiser DOI/forfatter/år/sider/URL og fjern plassholdere én for én |

## Statusregler

- **Verifisert:** kontrollert direkte mot primærkilde eller maskinelt mot data.
- **Reprodusert:** en angitt kodekontroll produserer resultatet for navngitt vintage.
- **Registrert:** påstanden har kandidat/evidens, men full kontroll mangler.
- **Delvis:** minst ett felt, tidspunkt eller beløp mangler sikker primærkilde.
- **Ikke ferdig:** skal ikke presenteres som endelig evidens.

Nye materielle påstander skal få en rad før de brukes som premiss i modell eller konklusjon.
