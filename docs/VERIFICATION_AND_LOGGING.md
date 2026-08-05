# Verifisering, logging og sporbarhet

## To forskjellige spørsmål

**Verifisering** spør om data, kode og resultater oppfyller avtalte kontrakter.

Eksempler:

- er månedsnøkkelen unik og sammenhengende?
- summerer bydelene til Oslo-totalen?
- er termin $t$ lik utbetaling $t+1$?
- stopper kjøringen ved et brudd?
- er backtesten tidsriktig?

**Logging** dokumenterer hva som skjedde i én bestemt kjøring.

Eksempler:

- start- og sluttid;
- kodeversjon;
- datavintage og filhash;
- kontrollnavn og resultat;
- konfigurasjon;
- feiltype og kontekst.

En logg beviser ikke at analysen er riktig. En test uten kjøremetadata gjør det vanskelig å etterprøve hvilken kode og hvilke data som faktisk ble testet. Prosjektet trenger begge deler.

## Nåværende fase-1-beviskjede

~~~mermaid
flowchart TD
    A["Frossen datavintage"] --> B["Skjema og nøkkelkontroller"]
    B --> C["Kalender- og summeringskontroller"]
    C --> D["JSON-hendelser"]
    D --> E["Run-manifest med filhash"]
    E --> F["GitHub Actions og PR"]
~~~

Fase-1-validatoren:

1. finner filene fra repo-roten;
2. beregner SHA-256 for hver kontrollert fil;
3. validerer skjema, nøkler, måneder og ikke-negative additive mål;
4. tester termin→utbetaling;
5. tester bydel→Oslo og brukergruppe→Oslo;
6. kontrollerer intervensjonstabellen og citation keys;
7. skriver én JSON-hendelse per kontroll;
8. returnerer exit-kode 1 hvis minst én kontrakt brytes;
9. kan skrive et samlet JSON-manifest.

Kjør lokalt:

~~~bash
python scripts/validate_phase1.py --manifest artifacts/phase1-validation.json
~~~

I GitHub Actions legges Git-SHA og workflow-metadata til fra runnerens miljø, og manifestet lastes opp som en build-artifact.

## Hva et manifest minst skal inneholde

| Felt | Hvorfor |
|---|---|
| run_id og timestamp_utc | Identifiserer kjøringen |
| git_sha og git_ref | Binder resultatet til kode |
| data_vintage | Binder resultatet til kildeuttaket |
| filsti, størrelse og SHA-256 | Oppdager usynlige datavariasjoner |
| kontrollnavn, status og detaljer | Viser hva som faktisk ble verifisert |
| Python-versjon og CI-miljø | Dokumenterer kjøremiljø |
| error_count og warning_count | Gjør porten maskinlesbar |

Fase 2 utvider manifestet med treningsperiode, origin, horisont, features, modellkonfigurasjon, seed og prognosemål. Fase 3 kan legge til modell-ID, deploy-ID, overvåkningsvinduer og rollback-status.

## Demonstrasjon i intervju

En presis formulering er:

> Hver kjøring validerer datakontrakten før analyse. Kontrollen stopper CI ved skjema-, kalender- eller summeringsbrudd og skriver strukturerte hendelser. Manifestet binder resultatet til Git-SHA, datavintage og SHA-256 for inputfilene. I modellfasen vil samme spor følge hver rolling-origin-fold og prognosehorisont.

Vis tre konkrete artefakter:

1. en grønn PR-kjøring;
2. et manifest fra samme commit;
3. en bevisst negativ test eller midlertidig branch der en feil faktisk stopper CI.

Det tredje punktet skiller en reell kontroll fra en sjekkliste som alltid passerer.

## Personvern og sikker logging

Logger skal aldri inneholde:

- personidentifikatorer;
- rå mikrodata;
- tokens, cookies eller API-nøkler;
- hele HTTP-responser uten vurdering;
- små celler som omgår kildens prikking.

På offentlige aggregater logges metadata, hash, radantall, skjema og kontrollresultat — ikke mer data enn nødvendig.

## Modenhetsnivå

- **Fase 1:** datakontrakt, filhash, CI, feilkode og frosset vintage.
- **Fase 2:** fold-, feature-, modell- og metrikksporbarhet.
- **Fase 3:** planlagte kjøringer, modellversjon, driftsovervåkning, varsling og rollback.

Dette gjør at «MLOps» kommer som en videreføring av en bevist analyseprosess, ikke som et separat teknologilag.
