# Prosjektstatus

Sist oppdatert: 2026-08-05  
Nåværende fase: **Fase 1 – datagrunnlag og analytisk rekkevidde**  
Aktivt arbeid: [issue #1](https://github.com/Torcode/bostotte-oslo/issues/1)

## Hva repoet faktisk inneholder

Repoet er ikke lenger et tomt prosjektstillas. Følgende er allerede til stede:

- månedlige Husbanken-uttrekk for Oslo og Norge, totalt, per bydel og per brukergruppe;
- SSB-serier for leie, KPI og befolkning;
- Oslo-statistikk per bydel for AAP, uføretrygd, sosialhjelp og befolkning;
- en kuratert intervensjonstabell med 20 hendelser;
- gjeldende regelparametre, historisk grunnbeløp og månedlige strømstøttebeløp;
- Python-skript for Qlik-, SSB- og Oslo-statistikkbankinnhenting;
- en R-laster med seks eksisterende QA-kontroller;
- kodebok og kildedokumentasjon;
- teori-, metode- og rapportutkast i Quarto;
- bibliografi med 80 nøkler.

## Verifisert i denne fasen

For den frosne datavintagen 2026-08-04 er følgende kontrollert direkte mot filene:

- Oslo-totalen har 199 unike, sammenhengende måneder fra 2010m1 til 2026m7;
- termin i måned $t$ er lik utbetaling i $t+1$ i 198 av 198 observerbare månedspar;
- bydelsdata summerer eksakt til Oslo for alle additive mål og måneder;
- de fem brukergruppene summerer eksakt til Oslo for alle additive mål og måneder;
- nøklene måned, bydel × måned og brukergruppe × måned er unike;
- siste rad er en sanntidskant: juli 2026 har utbetaling, men terminkjøringen er ennå ikke gjennomført.

Disse er datakontroller. De sier ikke at en prognosemodell er validert.

## Pågår i issue #1

- offentlig og presis README;
- kanonisk prosjekt-, fase- og beslutningskontrakt;
- evidensregister;
- maskinell Python-validering med feilstatus;
- strukturert kontrollogg og manifest;
- første GitHub Actions-port;
- standard issue- og PR-mal;
- prioritert backlog for fase 1–3.

## Ikke ferdig

| Område | Status | Konsekvens |
|---|---|---|
| Prognoser og backtest | Ikke startet/godkjent | Ingen modell kan omtales som best |
| Bibliografi | 41 forekomster av plassholdermerking | Materielle påstander må verifiseres før offentlig rapport |
| R/Quarto-miljø | Avhengigheter er ikke låst | Ren checkout-rendering er ikke dokumentert |
| Rapportstruktur | unt_1.qmd og 03-metode-del1.qmd overlapper | Kanonisk tekstkilde må ryddes |
| Python-innhenting | Skript bruker arbeidskatalog-relative stier | Kjørbarhet fra repo-roten må hardnes |
| Live API-test | Ikke del av første CI-port | Skjemaendringer i eksterne API-er fanges ikke automatisk ennå |
| Historiske vintager | Ikke offentlig tilgjengelige | Ekte realtime-backtest kan ikke rekonstrueres fullt ut |
| Regelkilder | Enkelte rader står som delvis verifisert | De kan ikke behandles som endelige eksogene fakta |
| Modellens operative bruk | Ikke bekreftet med Velferdsetaten | Nytteformuleringer må være betingede |

## Nærmeste fase-1-port

Fase 1 kan lukkes når:

1. alle materielle kilder i rapporten er bibliografisk verifisert;
2. datauttrekket kan kjøres fra repo-roten med eksplisitte avhengigheter;
3. data-QA stopper ved feil og produserer manifest;
4. Quarto-rapporten renderes fra ren checkout i CI eller dokumentert miljø;
5. du godkjenner endelig prognoseobjekt og informasjonssett;
6. rapporten skiller klart mellom verifiserte funn, hypoteser og begrensninger.

## Resultatstatus

Det foreligger foreløpig:

- ingen godkjent rolling-origin-backtest;
- ingen validert sammenligning mot seasonal naïve;
- ingen ML-resultater;
- ingen fremtidsprognose;
- ingen produksjonsmodell.

Dette er en styrke så lenge statusen er eksplisitt: fase 1 skal avgjøre om fase 2 er faglig forsvarlig.
