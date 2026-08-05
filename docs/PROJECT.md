# Prosjektkontrakt

Sist oppdatert: 2026-08-05  
Status: kanonisk for fase 1

## Formål

Prosjektet skal undersøke hva åpne, aggregerte data gjør det mulig å forstå og prognostisere om statlig bostøtte i Oslo. Målet er både å utvikle en faglig forsvarlig prognoseoppgave og å dokumentere hele analyseverdikjeden som er relevant for en dataanalytiker/data scientist-rolle i Velferdsetaten.

Stillingsannonsen er en kompetanseramme, ikke forskningsobjektet. Prosjektet skal vise substans i datainnhenting, validering, økonomisk og institusjonell forståelse, prediktiv modellering, evaluering, visualisering, reproduksjon og eventuell operasjonalisering.

## Forskningsspørsmål

> Hvor presist kan månedlig antall husstander som mottar statlig bostøtte i Oslo prognostiseres 1–12 måneder frem ved hjelp av åpne data, og i hvilken grad forbedres prognosenes treffsikkerhet og prediksjonsintervallenes dekning når kjente regelendringer modelleres eksplisitt?

Fase 1 har et forutgående spørsmål:

> Har prosjektet relevante, konsistente og tidsriktige data til å definere og etterprøve et realistisk prognoseproblem?

## Arbeidende prognoseobjekt

Analyseenheten er Oslo per terminmåned. Arbeidende hovedserie er

$$
y_t = M^T_t,
$$

der $M^T_t$ er antall unike husstander med positivt terminvedtak for måned $t$ i Husbankens statistikkbank.

Utbetalingsserien er

$$
M^U_{t+1}=M^T_t
$$

i den observerte datavintagen, fordi terminen utbetales etterskuddsvis. Identiteten er en datakontroll og en kalenderoversettelse, ikke en modellantakelse.

Endelig fase-2-kontrakt krever en eksplisitt beslutning om:

- hoved- og sekundærutfall;
- transformasjon og skala;
- prognoseopprinnelse og informasjonssett;
- horisonter;
- tap og evalueringsmål;
- bruk av bydels- og brukergruppehierarki.

## Sekundære størrelser

Følgende kan brukes som sekundærutfall, mekanismekontroller eller diagnostikk:

- samlet utbetalt beløp;
- gjennomsnittlig bostøtte per mottakende husstand;
- gjennomsnittlig inntekt og boutgift;
- antall avslag;
- antall terminbehandlede saker;
- mottak per bydel;
- mottak per brukergruppe.

Ingen av dem skal omtales som direkte mål på underliggende behov eller berettigelse.

## Informasjonssett

For en prognoseopprinnelse $\tau$ skal $\mathcal{I}_\tau$ bare inneholde informasjon som faktisk ville vært tilgjengelig da prognosen ble produsert. Det innebærer minst:

- siste publiserte og ferdigkjørte termin;
- datavintage og kjente revisjonsbegrensninger;
- regelendringer som var vedtatt og kjent ved $\tau$;
- eksterne variabler med korrekt publiseringslag;
- transformasjoner estimert kun på treningsperioden.

Historiske vintager fra Husbankens statistikkbank er ikke offentlig tilgjengelige. Vintage-realisme må derfor analyseres som en eksplisitt begrensning.

## Beslutningsrelevans

Mulig nytte undersøkes for:

- situasjonsforståelse;
- scenarioanalyse ved regelendringer;
- aktivitets- og kapasitetsplanlegging;
- avviksoppfølging;
- kommunikasjon av prognoseusikkerhet.

Statlig bostøtte finansieres av staten. Påstander om direkte kommunal budsjettvirkning eller konkrete operative beslutninger skal ikke fremsettes uten dokumentasjon fra Velferdsetaten.

## Tre faser

### Fase 1 – datagrunnlag og analytisk rekkevidde

Leveranse: en reproducerbar rapport som dokumenterer kilder, definisjoner, datavintage, datakvalitet, måleregimer, sesong, regelendringer, deskriptive mønstre og prognosepotensial.

Faseport:

- kjernedata er maskinelt validert;
- materielle påstander har verifiserte kilder;
- R/Quarto-miljøet kan bygges fra ren checkout;
- prognoseobjekt og informasjonssett er eksplisitt vedtatt;
- begrensninger og ikke-identifiserbare størrelser er dokumentert;
- fase-1-rapporten kan renderes uten manuelle steg.

### Fase 2 – modellutvikling og prognosetesting

Leveranse: Google Colab-notebooks og gjenbrukbar kode som sammenligner seasonal naïve, statistiske tidsseriemodeller og relevante ML-kandidater.

Krav:

- expanding-window rolling origin;
- evaluering per horisont 1–12;
- fold-riktig preprocessing og tuning;
- ingen fremtidsinformasjon;
- punktprognoser og intervaller;
- dokumentert stabilitet, tolkbarhet og feilsituasjoner;
- ML må vurderes mot enkle baselines, ikke mot fravær av modell.

### Fase 3 – operasjonalisering og MLOps-potensial

Leveranse: en avgrenset mulighetsstudie og driftsdemonstrator dersom fase 2 viser stabil modellverdi.

Vurderinger:

- automatisert innhenting og validering;
- versjonering av data, kode, konfigurasjon og modeller;
- strukturerte logger og run-manifest;
- CI og godkjenningsporter;
- planlagte kjøringer og eventuell retrening;
- overvåkning av datadrift, prognosefeil og strukturelle brudd;
- varsling, manuell kontroll og rollback;
- personvern, tilgang, sikkerhet, kostnad og eierskap.

## Evalueringsdesign

- Ingen tilfeldig datasplitt.
- Seasonal naïve med sesonglengde 12 som obligatorisk baseline.
- Pseudo-out-of-sample rolling-origin-backtesting.
- Resultater per horisont.
- MAE og RMSE som generelle mål; skala- og beslutningsrelevante mål fastsettes før modellrangering.
- Intervallkalibrering vurderes med empirisk dekning og bredde.
- Modellrangering skal inneholde usikkerhet og stabilitet, ikke bare ett gjennomsnitt.
- Regelintervensjoner sammenlignes mot modeller uten eksplisitt intervensjon.

## Tolkning og avgrensning

Prosjektet er prediktivt. Det identifiserer ikke uten et separat design:

- boligbehov;
- berettigelse;
- ikke-bruk eller full take-up;
- individuelle velferdseffekter;
- kausale effekter av bostøtte eller regelendringer;
- direkte virkninger på kommunens budsjett.

## Ikke-mål i fase 1

- individprediksjon eller automatiserte vedtak;
- full MLOps-plattform;
- produksjonssetting hos Oslo kommune;
- bruk av konfidensielle mikrodata;
- modellkonkurranse før datakontrakten er lukket;
- kausal evaluering uten separat estimand og identifikasjonsdesign.
