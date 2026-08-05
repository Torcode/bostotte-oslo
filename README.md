# Bostøtte Oslo

[![Phase 1 CI](https://github.com/Torcode/bostotte-oslo/actions/workflows/ci.yml/badge.svg)](https://github.com/Torcode/bostotte-oslo/actions/workflows/ci.yml)

Et uavhengig og reproducerbart data science-prosjekt som undersøker hvor presist månedlig statlig bostøtte i Oslo kan prognostiseres med åpne data, og hvordan prognosene kan evalueres og etterprøves under realistiske databegrensninger.

> **Status: Fase 1 – datagrunnlag og analytisk rekkevidde.** Prosjektet har hentet og dokumentert reelle, aggregerte data, men har ennå ikke publisert validerte prognoseresultater. Nå kvalitetssikres måling, kilder, datavintage, institusjonelle brudd og hva miljøet faktisk kan reprodusere.

Prosjektet er et privat portefølje- og læringsprosjekt. Det er ikke utviklet på oppdrag fra eller i samarbeid med Oslo kommune, Velferdsetaten eller Husbanken.

## Kort fortalt

- **Problem:** Hvor presist kan månedlig antall husstander med statlig bostøtte i Oslo prognostiseres 1–12 måneder frem?
- **Arbeidende hovedserie:** Antall husstander med positivt terminvedtak per måned. Terminserien holdes eksplisitt atskilt fra utbetalingskalenderen.
- **Datagrunnlag:** Husbanken 2010m1–2026m7, supplert med SSB, Oslo kommunes statistikkbank og en kildebelagt regelverkskalender.
- **Nåværende leveranse:** En reproducerbar fase-1-rapport om datakvalitet, måling, mekanismer, brudd og prognosepotensial.
- **Prosjektlogikk:** Datamulighet → modellverdi → driftsverdi.
- **Viktig avgrensning:** Registrert mottak er ikke det samme som boligbehov, berettigelse eller full take-up.

Stillingsannonsen for dataanalytiker/data scientist i Velferdsetaten fungerer som en kompetanseramme for analyseverdikjeden:

> datainnhenting → validering → analyse → prediktive modeller → evaluering → visualisering → reproduksjon → mulig operasjonalisering

Jobbannonsen er ikke forskningsobjektet. Forskningsobjektet er bostøtte og prognoseproblemet.

## Problemstilling

Prosjektets arbeidende forskningsspørsmål er:

> Hvor presist kan månedlig antall husstander som mottar statlig bostøtte i Oslo prognostiseres 1–12 måneder frem ved hjelp av åpne data, og i hvilken grad forbedres prognosenes treffsikkerhet og prediksjonsintervallenes dekning når kjente regelendringer modelleres eksplisitt?

Fase 1 besvarer først et mer grunnleggende spørsmål:

> Har vi relevante, konsistente og tidsriktige data til å definere og etterprøve et realistisk prognoseproblem?

## Målekontrakt

Bostøtten finnes i to kalendre:

- $M^T_t$: husstander med positivt vedtak for **terminmåned** $t$;
- $M^U_t$: husstander med **utbetaling i kalendermåned** $t$.

Bostøtten utbetales etterskuddsvis. I det frosne uttrekket holder derfor identiteten

$$
M^U_{t+1}=M^T_t
$$

for samtlige 198 observerbare månedspar. Analysen føres foreløpig i terminkalenderen fordi regelendringer og inntektsgrunnlag gjelder terminen. Utbetalingskalenderen beholdes for operativ rapportering og som en uavhengig konsistenskontroll.

Datasettet inneholder også samlet utbetalt beløp, gjennomsnittlig bostøtte, gjennomsnittlig inntekt og boutgift, avslag, terminbehandlede saker, bydeler og brukergrupper. Disse er sekundære utfall, drivere eller diagnostiske mål; de er ikke automatisk alternative mål på behov.

## Datagrunnlag

| Kilde | Rolle | Frekvens og nivå | Dekning i frosset uttrekk |
|---|---|---|---|
| [Husbankens statistikkbank](https://statistikk.husbanken.no/bostotte) | Mottak, utbetaling, beløp, bydeler og brukergrupper | Måned × Oslo/Norge/bydel/brukergruppe | 2010m1–2026m7 |
| [SSB tabell 09895](https://www.ssb.no/statbank/table/09895/) | Leiemarkedsundersøkelsen | År × prissone × rom | 2012–2025 |
| [SSB tabell 03013](https://www.ssb.no/statbank/table/03013/) | KPI for betalt husleie | Måned | 1979m1–2025m12 |
| [SSB tabell 14710](https://www.ssb.no/statbank/table/14710/) | KPI-bro inn i 2026 | Måned | 1920m3–2026m6 |
| [SSB tabell 01222](https://www.ssb.no/statbank/table/01222/) | Befolkning og kvartalsvise endringer | Kvartal × Oslo | 1997K4–2026K1 |
| [Oslo kommunes statistikkbank](https://statistikkbanken.oslo.kommune.no/) | AAP, uføretrygd, sosialhjelp, befolkning og framskriving per bydel | År × bydel | Tabellavhengig |
| Husbankens årsrapporter og regelverksveileder | Intervensjoner og beregningsparametre | Hendelsesdatert | 2020–2026 |

Husbanken-uttrekket er fra 4. august 2026, etter Qlik-reload 05:33 UTC. Kilden revideres bakover, og historiske vintager er ikke offentlig tilgjengelige. Resultater må derfor alltid knyttes til uttaksdatoen.

Detaljer finnes i [datakildedokumentasjonen](velferdsetaten-data/docs/datakilder.md), [kodeboken](velferdsetaten-data/docs/kodebok.md) og [evidensregisteret](docs/EVIDENCE_REGISTER.md).

## Verifisert status i fase 1

Følgende er datafakta, ikke prognoseresultater:

| Kontroll | Resultat for vintage 2026-08-04 |
|---|---|
| Oslo-total, månedlig | 199 rader, 2010m1–2026m7, unik og sammenhengende månedsindeks |
| Termin → utbetaling | 198 av 198 observerbare månedspar er identiske etter én måneds forskyvning |
| Bydel → Oslo | Alle additive mål summerer eksakt til Oslo-totalen per måned |
| Brukergruppe → Oslo | De fem brukergruppene summerer eksakt til Oslo-totalen per måned |
| Sanntidskant | 2026m7 har utbetaling, men termin er ennå ikke kjørt og står som 0 |
| Personvern | Repoet bruker offentlige, aggregerte data; ingen person- eller registerdata |

Maskinelle kontroller kjøres med:

~~~bash
python scripts/validate_phase1.py
~~~

Skriptet skriver strukturerte JSON-hendelser, returnerer feilstatus dersom en kontrakt brytes, og kan skrive et maskinlesbart manifest med filhash, kodeversjon i CI og kontrollresultater.

## Tre faser

| Fase | Hovedspørsmål | Hovedleveranse | Port videre |
|---|---|---|---|
| **1. Data og rekkevidde** | Hva måler dataene, og hva kan de støtte? | Reproduserbar datakvalitets- og mulighetsrapport | Verifiserte definisjoner, kilder, informasjonssett og valgt prognoseobjekt |
| **2. Modeller og ML** | Skaper mer avanserte modeller stabil prognoseverdi? | Colab-notebooks og tidsriktig sammenligning mot baselines | Robust gevinst uten lekkasje og med dokumenterte feilsituasjoner |
| **3. Operasjonalisering** | Kan dokumentert modellverdi bli en forsvarlig prosess? | MLOps-mulighetsstudie og driftsdemonstrator | Klart bruksbehov, eierskap, overvåkning og sikkerhetskrav |

### Fase 1 – data og analytisk rekkevidde

Fase 1 omfatter innhenting, kildeverifikasjon, datakvalitet, måleregimer, sesong, regelverksendringer, deskriptiv analyse og en Quarto-rapport. Fasen avsluttes med en eksplisitt beslutning om:

1. hoved- og sekundærutfall;
2. forklaringsvariabler som er tilgjengelige ved faktisk prognosetidspunkt;
3. lovlige prognosehorisonter;
4. spørsmål dataene ikke kan besvare;
5. om prosjektet går videre til fase 2.

### Fase 2 – modellutvikling i Google Colab

Verifiserte data tas inn i Colab for å sammenligne seasonal naïve, statistiske tidsseriemodeller og relevante ML-modeller. Alle modeller evalueres med expanding-window rolling origin, separat for hver horisont. Feature engineering, skalering og seleksjon skal skje innenfor treningsfolden.

ML er en hypotese, ikke en konklusjon: en mer kompleks modell må skape stabil merverdi mot enklere alternativer.

### Fase 3 – MLOps-potensial

Fase 3 gjennomføres bare dersom fase 2 dokumenterer modellverdi. Da vurderes automatisert innhenting, datavalidering, versjonering, strukturerte logger, run-manifest, CI, planlagte kjøringer, driftsovervåkning, varsling, retrening, rollback, sikkerhet og eierskap.

## Evalueringsprinsipper

- Ingen tilfeldig train/test-splitt for tidsserier.
- Seasonal naïve med sesonglengde 12 er obligatorisk baseline.
- Pseudo-out-of-sample rolling-origin-evaluering.
- Ytelse rapporteres separat for $h=1,\ldots,12$.
- Alle transformasjoner estimeres innenfor hver treningsfold.
- Prediksjonsintervaller vurderes på både dekning og bredde.
- Regelendringer behandles som mulige intervensjoner eller regimeskift.
- Prediksjon og forklaring holdes atskilt fra kausal identifikasjon.

## Reproduser prosjektet

Fra repo-roten:

~~~bash
# Maskinell fase-1-kontrakt
python scripts/validate_phase1.py --manifest artifacts/phase1-validation.json

# Eksisterende R-baserte kontroller og datasammendrag
Rscript velferdsetaten-data/scripts/velferdsetaten_data.R

# Fase-1-rapport
quarto render unt_1.qmd
~~~

Python-valideringen bruker bare standardbiblioteket. R/Quarto-miljøet er foreløpig ikke låst; full ren-checkout-rendering er derfor en åpen fase-1-leveranse og skal ikke omtales som løst før CI bekrefter det.

## Prosjektstruktur

| Sti | Innhold |
|---|---|
| [unt_1.qmd](unt_1.qmd) | Arbeidende teori-, metode- og rapportdokument |
| [velferdsetaten-data/](velferdsetaten-data/) | Uttrekksskript, frosne data, kildekart og kodebok |
| [scripts/](scripts/) | Repo- og datakontrakter som skal kjøre i CI |
| [docs/PROJECT.md](docs/PROJECT.md) | Kanonisk prosjekt- og fasekontrakt |
| [docs/STATUS.md](docs/STATUS.md) | Faktisk status, risikoer og neste port |
| [docs/DECISIONS.md](docs/DECISIONS.md) | Vedtatte og foreløpige metodevalg |
| [docs/EVIDENCE_REGISTER.md](docs/EVIDENCE_REGISTER.md) | Påstand → kilde → verifiseringsstatus |
| [docs/BACKLOG.md](docs/BACKLOG.md) | Prioritert arbeid etter issue #1 |

## Begrensninger og ansvarlig tolkning

Tilgjengelige aggregater identifiserer ikke:

- underliggende eller udekket boligbehov;
- hvem som er berettiget, men ikke søker;
- full take-up;
- individuelle velferdsutfall;
- kausale virkninger av bostøtte eller regelendringer.

En presis prognose viser heller ikke nødvendigvis hvilken mekanisme som skapte utviklingen. Resultatene vil være betinget på den observerte datavintagen og kan svekkes av nye regler, økonomiske sjokk, endret søkeatferd og revisjoner.

## Nåværende resultatstatus

Det foreligger **ingen godkjent modellrangering, ingen backtest og ingen publisert fremtidsprognose**. Teori- og metodeutkastet inneholder deskriptive mønstre og testbare hypoteser; empiriske prognosepåstander publiseres først etter fase-2-evaluering.

Se [prosjektstatus](docs/STATUS.md) og [åpne issues](https://github.com/Torcode/bostotte-oslo/issues) for neste arbeid.
