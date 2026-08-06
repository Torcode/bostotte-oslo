# Prognose for statlig bostøtte i Oslo

[![Datakontrakt](https://github.com/Torcode/bostotte-oslo/actions/workflows/ci.yml/badge.svg)](https://github.com/Torcode/bostotte-oslo/actions/workflows/ci.yml)

### → [Les rapporten (PDF, 36 sider)](bostotte_oslo.pdf)

[Kilden bak den](bostotte_oslo.qmd) · [datagrunnlaget](data/) · [kodebok](data/docs/kodebok.md) · [endringslogg](logg/)

---

Hvor presist kan månedlig antall husstander med statlig bostøtte i Oslo prognostiseres
1–12 måneder fram ved hjelp av **åpne data** — og hvor mye bedre blir prognosen når
kjente regelendringer modelleres eksplisitt?

Serien er regelstyrt. Antall mottakere bestemmes ikke bare av inntekter, husleier og
søkeatferd, men av hvordan retten til bostøtte til enhver tid er definert, og regelverket
er endret fem ganger siden 2020. En modell som ikke kjenner endringene, leser vedtak som
trend og utbetalingskalender som sesong, og framskriver begge deler feil.

> **Uavhengig prosjekt.** Dette er et privat fag- og porteføljeprosjekt. Det er ikke
> utført på oppdrag fra, eller i samarbeid med, Oslo kommune, Velferdsetaten eller
> Husbanken. Alt datagrunnlag er offentlig tilgjengelig og aggregert; ingen person-
> eller registerdata inngår.
> Hovedformålet er å lære mest mulig, kortest mulig.
> Filene og arbeidetet inneholder ikke-verfisert KI-informasjon.
> 

## Dette er et læringsprosjekt — les dette først

Formålet er **ikke** å levere en ferdig prognosemodell. Formålet er å lære bostøttefeltet
og hele analysekjeden ved å bygge den selv, ett ledd om gangen, med KI som verktøy hele
veien.

Det har en konsekvens som må sies rett ut, ikke gjemmes i en fotnote: **filene og arbeidet
i dette repoet inneholder ikke-verifisert innhold.** Det er et stadium, ikke en
forglemmelse. Et læringsprosjekt som later som alt er ferdigkontrollert, lærer ingen noe —
og det ville vært den ene feilen dette prosjektet handler om å unngå.

Derfor er arbeidet delt i faser, og **rekkefølgen er en læringsrekkefølge**: hver fase har
som eneste jobb å feste én hjørnestein, og neste fase har ikke lov til å hvile på en
hjørnestein som ikke er festet.

| Fase | Hjørnesteinen den skal feste | Status |
|---|---|---|
| **1 — Datagrunnlaget** | Er dataene det de utgir seg for? Kan hver kolonne føres tilbake til en navngitt kilde og et navngitt skript? | Kontrollene kjører; litteraturlista gjenstår |
| **2 — Modellene, i R** | Holder mekanikken? Rullerende opprinnelse, referansemodeller, intervensjonsanalyse, kalibrerte intervaller | Kjørt. Fire feil funnet og åpne |
| **3 — Modellene, i Python** | De klassene R-verktøyet ikke dekker: gradientboosting, bayesiansk strukturell tidsserie, hierarkisk avstemming | Spesifisert, ikke estimert |
| **4 — Drift** | Hva som skal til for at noe slikt kan kjøre i en etat: kjøreplan, terskler, overvåkning, eierskap | Ikke påbegynt |

**Hvorfor R først, og Python etterpå.** Fase 2 er skrevet i R fordi det er der
tidsserieverktøyet bor — `fable`, `tsibble` og `feasts` gir ARIMA med eksogene
regressorer, rullerende opprinnelse og prediksjonsfordelinger i samme rammeverk, og Quarto
gjør hele dokumentet reproduserbart i én kommando. Det er den korteste veien til å forstå
*hva som faktisk skjer* i en prognose. Fase 3 flytter til Python fordi modellklassene som
gjenstår hører hjemme der, og fordi det er den overgangen som er verdt å lære: fra en
modell man kan gjøre rede for, til en modell som må evalueres mot den første for å
forsvare seg.

**Hva som har hvilken status i dag:**

| Hva | Status |
|---|---|
| **Datagrunnlaget** | Verifisert. 47 maskinelle datakontrakter ved hver push, ni regnskapsidentiteter ved hver rendering, og ekstern validering mot Husbankens publiserte nasjonale årstall |
| **Evalueringsmekanikken** | Backtestet. 31 prognoseopprinnelser × 8 modeller × horisont 1–12, med Clark–West på nøstede par |
| **Litteraturlista** | Delvis verifisert. 30 av 81 oppføringer har ukontrollert utgiver, URL og sidetall |
| **Enkelte resultatpåstander** | Under retting. Se [åpne issues](https://github.com/Torcode/bostotte-oslo/issues) — blant annet en kodefeil som gjør at modell M7 ikke gjør det teksten beskriver |

Feil som blir funnet, legges ut som issues med hva som er galt, hvordan det ble oppdaget
og hva rettelsen er — framfor å bli stille rettet. Begrunnelsen for hver endring ligger i
[`logg/`](logg/). En rapport som skal kunne etterprøves, må vise sine egne feil like
tydelig som sine funn; det er dét fasene og loggen er til for.

## Hovedfunn

**Ikke-stasjonariteten i serien *er* regelendringene.** Den rå logserien krever
differensiering (KPSS 1,03). Betinget på fem deterministiske ledd — tre
intervensjonsvinduer og to kalenderregressorer — er den stasjonær (KPSS 0,16), og
modellvalget bekrefter det uavhengig: referansen uten regressorer velger *d* = 1,
spesifikasjonene med intervensjonsmatrisen velger *d* = 0.

**Regelverkskalenderen gjør det tunge arbeidet.** Mot termin april 2024 — seriens
største bevegelse, et fall på 25 % på én termin — landet hovedspesifikasjonen på
15 093 husstander fra ni måneders horisont, mot en fasit på 15 588. Sesongnaiv og
SARIMA lander på 19 500–20 900 fra samtlige horisonter.

**Å modellere bruddene forverrer intervalldekningen.** Det var ikke forventet. Modellen
blir mer selvsikker uten å bli mer treffsikker der informasjonen mangler, og
underdekningen er en *skjevhet*, ikke for smale intervaller: der høstpakken 2024 ikke er
estimerbar, underpredikerer modellen med 7,2 % — praktisk talt den utelatte koeffisienten.
Konformal etterkalibrering reparerer dekningen.

**En regressor kan ikke estimeres før hendelsen har skjedd.** Ved 24 av 31
prognoseopprinnelser er høstpakken identisk null i treningsvinduet. Det rammer 56 % av
prognosepunktene og er ikke en modelleringssvakhet, men en grense for hva serien kan
bære alene. Effektstørrelsen må i så fall hentes utenfra — fra et datert forhåndsanslag.

To av fem forhåndsregistrerte implikasjoner overlevde ikke møtet med dataene. Begge
feilene, og begrunnelsen for hver, står i kapittel 4.

## Kom i gang

Første gang, i R:

```r
source("oppsett.R")     # installerer det som mangler og sjekker miljøet
```

Deretter, i RStudio med `Velferdsprosjekt.Rproj` åpen — bruk Render-knappen, eller:

```r
source("verifiser.R")   # to sekunder: parser dokumentet i verste tegnsett
quarto render bostotte_oslo.qmd
```

Bygger hele dokumentet — data lastes, verifikasjonskontrollene kjøres, modellene
estimeres og figurene tegnes. Første kjøring tar rundt ti minutter; den rullerende
kryssvalideringen er cachet, så senere tekstendringer koster sekunder.

Krever R med `tidyverse`, `knitr`, `fable`, `fabletools`, `feasts`, `tsibble`, `urca`
og `distributional`, samt Quarto ≥ 1.7. **Ingen LaTeX** — Typst følger med
Quarto, og malen bruker bare fonter Typst har innebygd, slik at PDF-en blir identisk på
enhver maskin.

## Hva ligger hvor

**Leveransen**

| Sti | Innhold |
|---|---|
| [`bostotte_oslo.pdf`](bostotte_oslo.pdf) | Rapporten, ferdig bygget. Versjoneres bevisst, slik at den kan leses uten å installere noe |
| [`bostotte_oslo.qmd`](bostotte_oslo.qmd) | Hele arbeidet: teori, metode, resultater. All beregning kjører ved rendering |
| [`referanser.bib`](referanser.bib) | Litteraturliste |

**Datagrunnlaget** — [`data/`](data/)

| Sti | Innhold |
|---|---|
| [`data/raw/`](data/raw/) | Rådata og primærkilder, arkivert slik de ble hentet |
| [`data/clean/`](data/clean/) | Bearbeidede serier og kuraterte oppslagstabeller |
| [`data/docs/kodebok.md`](data/docs/kodebok.md) | Hva hver kolonne betyr |
| [`data/docs/datakilder.md`](data/docs/datakilder.md) | Hvor hvert tall kommer fra |
| [`data/scripts/`](data/scripts/) | Uttrekksskript (Python) og R-laster for datapakken |

**Å bygge og etterprøve**

| Sti | Innhold |
|---|---|
| [`oppsett.R`](oppsett.R) | Installerer det som mangler og sjekker miljøet |
| [`verifiser.R`](verifiser.R) | Byggekontroll: parser dokumentet i et rent C-tegnsett og sjekker referanselisten |
| [`scripts/validate_phase1.py`](scripts/validate_phase1.py) | 47 datakontrakter i Python, uten R. Kjøres av GitHub ved hver push |
| [`.Rprofile`](.Rprofile) | Sikrer UTF-8 ved oppstart, også i R-prosessen Quarto starter |
| [`mal/typst-template.typ`](mal/typst-template.typ) | Dokumentmal (A4, booktabs-tabeller, norsk typografi) |

**Bakgrunn og historikk**

| Sti | Innhold |
|---|---|
| [`logg/`](logg/) | Hva som er endret underveis, og hvorfor. Hver post har før, etter og begrunnelse |
| [`litteratur/`](litteratur/) | Bakgrunnsrapporter som siteres i teksten |

## Datagrunnlaget

Alt er åpne data, hentet maskinelt med reproduserbare skript. Det er et designvalg:
det gjør kunnskapsgrunnlaget etterprøvbart for enhver, og det speiler arbeidsvilkårene
til en analysefunksjon som skal dele metode og tall uten å måtte etablere en avtale først.

| Kilde | Rolle | Frekvens × nivå | Dekning |
|---|---|---|---|
| [Husbankens statistikkbank](https://statistikk.husbanken.no/bostotte) | Utfallsserien: mottak, utbetaling, beløp, avslag | måned × Oslo/Norge/bydel/brukergruppe | 2010m1–2026m7 |
| [SSB 09895](https://www.ssb.no/statbank/table/09895/) | Leiemarkedsundersøkelsen | år × prissone × rom | 2012–2025 |
| [SSB 03013](https://www.ssb.no/statbank/table/03013/) | KPI for betalt husleie | måned | 1979–2025 |
| [SSB 14710](https://www.ssb.no/statbank/table/14710/) | KPI-bro inn i 2026 | måned | 1920–2026 |
| [SSB 01222](https://www.ssb.no/statbank/table/01222/) | Befolkning, Oslo | kvartal | 1997K4–2026K1 |
| [Oslo kommunes statistikkbank](https://statistikkbanken.oslo.kommune.no/) | AAP, uføretrygd, sosialhjelp, befolkning og framskriving per bydel | år × bydel | tabellavhengig |
| Husbankens årsrapporter og regelverksveileder | Regelverkskalender og beregningsparametre | hendelsesdatert | 2020–2026 |

Utfallsserien er en fullstendig administrativ registrering, ikke et utvalg, hentet fra
statistikkbankens Qlik Engine-API. Ved siden av ligger fem kuraterte tabeller bygget fra
primærkilder: regelverkskalenderen, forskriftsparametrene, strømtiltakenes månedsbeløp,
publiserte nasjonale årstall og daterte effektanslag.

**Datagrunnlaget er verifisert, ikke antatt.** Kontrollene ligger i to lag som ikke
overlapper i formål. Ni regnskapsidentiteter kjøres ved hver rendering, og en kontroll
som feiler stopper byggingen — de sikrer at *rapporten* ikke kan trykke et tall som
ikke stemmer. Ved siden av kjører [`scripts/validate_phase1.py`](scripts/validate_phase1.py)
47 datakontrakter i ren Python ved hver push til GitHub: bydelstallene summerer til
Oslo, brukergruppene summerer til Oslo, termin- og utbetalingskalenderen henger sammen
over 198 par, sanntidskanten er identifisert. De trenger ikke R, og gjør at
**en leser kan se at dataene holder uten å installere noe** — merket øverst er den
kjøringen.

Uttrekket er dessuten validert eksternt mot Husbankens publiserte nasjonale årstall:
avvik på 0,00 til −2,10 % over fem år, med et ensidig negativt avvik som er signaturen
til etterkontroll mot skatteoppgjøret. Beløpsserien måler altså omregnet rett, ikke
utbetalt kasse.

## Kjente begrensninger

Disse står her fordi de begrenser hva som kan konkluderes, ikke fordi de er små.

**Aggregatene identifiserer ikke** underliggende eller udekket boligbehov, hvem som er
berettiget uten å søke, full take-up, individuelle velferdsutfall, eller kausale
virkninger av bostøtten. En presis prognose viser heller ikke hvilken mekanisme som
skapte utviklingen.

- **Aggregerte data.** Take-up og berettigelse lar seg ikke skille fra hverandre.
  Estimerte intervensjonseffekter er nettoeffekter på beholdningen, der mekanisk og
  atferdsmessig respons er sammenblandet.
- **Ingen kontrollenhet i tid.** Hver regelendring treffer hele landet samtidig.
  Effektene måles mot en modellert kontrafaktisk bane, ikke mot en kontrollgruppe.
  Brukergruppeinndelingen gir derimot kontroller i *mekanismedimensjonen*.
- **Pseudo-sanntid.** Serien revideres bakover, og historiske vintages er ikke
  offentlig tilgjengelige. Evalueringen bruker gjeldende vintage gjennomgående — en
  kjent optimistisk skjevhet som rammer alle modellene likt.
- **Tynt anslagsgrunnlag.** Bare ett rent forhåndsanslag er publisert i materialet.
  For høstpakken 2024 finnes ingen husstandstall i noen av fire gjennomsøkte
  kildefamilier, og metoden for pålagte effektstørrelser kan derfor bare demonstreres
  med perfekt informasjon som øvre grense.
- **Bibliografien er delvis verifisert.** Ingen oppføring trykker lenger
  plassholdertekst i referanselisten — `verifiser.R` kontrollerer det ved hver
  kjøring. Tre oppføringer er verifisert mot primærkilde og rettet, deriblant én
  med *feil tittel*, og fire som ikke lot seg verifisere er fjernet framfor å
  bli stående (se endringsloggen). Men 30 av 81 oppføringer er fortsatt merket
  `note = {PLASSHOLDER}`: forfatter, tittel og år er kontrollert, mens utgiver,
  URL og sidetall ikke er slått opp mot primærkilde. Rapporten er derfor ikke
  kildeferdig slik den står.

## Status

Kapittel 1–4 er skrevet og bygger uten advarsler. Rullerende opprinnelse er kjørt: 31
opprinnelser, 8 modeller, horisont 1–12, med Clark–West på nøstede par og konformal
etterkalibrering. Resultatene for M1–M6 er dermed backtestede, ikke påstander.

**Åpne feil som påvirker hvordan kapittel 4 skal leses.** De står som issues, med
diagnose og rettelse:

- **M7 påfører aldri det pålagte bidraget.** En variabel maskeres inne i `mutate()`, slik
  at testen for om regressoren manglet aldri slår til. M7 er identisk med M6 i alle 372
  punktene. Avsnitt 4.6 og påstanden om verdien av et forhåndsanslag er dermed ikke
  avgjort, og underspørsmål **UB** står ubesvart til dette er rettet og kjørt på nytt.
- **Den konformale kalibreringen bruker feil som ikke var realisert ved opprinnelsen.**
  Dekningen etter kalibrering er derfor bedre enn den ville vært i drift, og effekten
  vokser med horisonten.
- **To ulike dekningstall for samme størrelse** i kapittel 4, fordi tabell og brødtekst
  regner på ulike utvalg uten at det er notert.
- **Siteringsapparatet** har en hengende referanse og en topptekst i `referanser.bib` som
  ikke lenger stemmer.

Bydelsnivået er dokumentert i datagrunnlaget, men ikke analysert. Det finnes ingen
publisert framtidsprognose og ingen produksjonsmodell — fase 3 og 4 er ikke påbegynt.
