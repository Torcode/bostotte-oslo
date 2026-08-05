# Instruksjoner for arbeid i repoet

Reglene gjelder hele repoet. Et lokalt AGENTS.md kan skjerpe, men ikke svekke dem.

## Fasit og prioritet

Ved konflikt gjelder denne rekkefølgen:

1. Eksplisitte brukerbeskjeder og godkjent GitHub-issue.
2. docs/PROJECT.md og vedtatte poster i docs/DECISIONS.md.
3. velferdsetaten-data/docs/kodebok.md og docs/EVIDENCE_REGISTER.md.
4. Eksisterende tester, valideringer og kode.
5. Antakelser gjort av agenten.

Ikke endre forskningsspørsmål, prognoseobjekt, variabeldefinisjoner eller evalueringsdesign i stillhet. Foreslå en beslutningspost og forklar konsekvensene.

## Før redigering

1. Les README.md, docs/PROJECT.md, docs/STATUS.md og relevant issue.
2. Gjengi leveranse, akseptansekriterier og eksplisitte ikke-mål.
3. Identifiser berørte filer og kontroller.
4. Bekreft at arbeidet ikke krever persondata eller ulovlig eksport.
5. Bevar brukerens eksisterende arbeid og unngå tilgrensende omskriving.

## Faser

- Fase 1 gjelder data, måling, kilder, deskriptiv analyse og rapportens analytiske rekkevidde.
- Fase 2 gjelder modellutvikling og ML i Colab, med testbar logikk flyttet til repoet etter evaluering.
- Fase 3 gjelder operasjonalisering og MLOps bare etter dokumentert modellverdi.

Ikke flytt et problem til en senere fase for å pynte på dagens status, og ikke introduser fase-3-infrastruktur før behovet er dokumentert.

## Ufravikelige faglige regler

- Bruk aldri tilfeldig train/test-splitt for tidsserier.
- All preprocessing, feature-seleksjon og tuning estimeres innenfor treningsfolden.
- Seasonal naïve med sesonglengde 12 er obligatorisk prognosebaseline.
- Evaluering skal være pseudo-out-of-sample med rolling origin.
- Rapporter ytelse per prognosehorisont, ikke bare ett aggregert mål.
- Kjente regelendringer behandles eksplisitt som mulige intervensjoner eller regimeskift.
- Termin, utbetaling, behov, berettigelse og take-up er forskjellige størrelser.
- ant_soknader er terminbehandlede saker i kildens datamodell, ikke nødvendigvis nye søknader.
- Prediksjon er ikke kausal identifikasjon.
- Alle eksterne tall skal kunne spores til kilde, uttaksmetode, uttaksdato og datavintage.
- Historiske datarevisjoner og sanntidskanter skal være synlige.
- En modell kan bare bruke informasjon som var tilgjengelig ved prognoseopprinnelsen.

## Data og personvern

- Ingen person-, register- eller konfidensielle mikrodata i Git.
- Microdata.no-data forblir i det sikre miljøet; bare tillatt kode og godkjente aggregater kan eksporteres.
- Nye datafiler krever dokumentert kilde, lisens/bruksvilkår, skjema, uttaksdato og formål.
- Hemmeligheter skal komme fra GitHub Secrets eller miljøvariabler, aldri fra kode eller notebooks.
- Offentlige aggregater skal fortsatt vurderes for prikking og differensieringsrisiko ved fine kryss.
- Ikke overskriv en frosset datavintage uten å bevare eller dokumentere endringen.

## Språk og kode

- Python brukes for innhenting, validering, modellering og eventuell operativ pipeline.
- R og Quarto brukes i fase 1 til økonometrisk analyse, visualisering og rapport.
- Notebooks er eksperimentflater; gjenbrukbar logikk flyttes til testbar kode.
- Nye avhengigheter må begrunnes og låses i samme eller et eksplisitt oppfølgingsissue.
- Bruk repo-roten som arbeidskatalog, eller gjør stier eksplisitt uavhengige av arbeidskatalog.
- Ikke fang brede exceptions uten å bevare årsak og kontekst.
- Maskinelle feil skal gi ikke-null exit-kode.

## Kontroller

Kjør minst:

~~~bash
python scripts/validate_phase1.py
python -m compileall -q scripts velferdsetaten-data/scripts
~~~

Ved R-dataendringer:

~~~bash
Rscript velferdsetaten-data/scripts/velferdsetaten_data.R
~~~

Ved rapportendringer:

~~~bash
quarto render unt_1.qmd
~~~

Hvis miljøet ikke kan kjøre en kontroll, skal dette rapporteres eksplisitt. Ikke oppgi kontrollen som bestått.

## Kilder og tekst

- Bruk primærkilder for regelverk, statistikkdefinisjoner og offentlige beslutninger.
- Bruk fagfellevurderte originalkilder for teori og metode når tilgjengelig.
- Ikke la en bibliografisk plassholder fremstå som verifisert.
- Skill mellom datakontroll, kildekontroll og tolkning.
- Ikke kopier lange tekstavsnitt eller hele rapporter inn i repoet når en lenke og presis referanse er tilstrekkelig.

## Ferdigdefinisjon

En leveranse er ferdig når:

- akseptansekriteriene er oppfylt;
- relevante kontroller og CI passerer;
- datadefinisjoner og antakelser er dokumentert;
- nye materielle påstander er registrert i evidensregisteret;
- metodiske valg er oppdatert i beslutningsloggen;
- PR-en oppgir endrede filer, testresultater, begrensninger og åpne problemer.

Én issue skal normalt gi én avgrenset branch og én PR.
