# Prognose for statlig bostøtte i Oslo

[![Datakontrakt](https://github.com/Torcode/bostotte-oslo/actions/workflows/ci.yml/badge.svg)](https://github.com/Torcode/bostotte-oslo/actions/workflows/ci.yml)
[![Kildeverifisering](https://github.com/Torcode/bostotte-oslo/actions/workflows/kildeverifisering.yml/badge.svg)](https://github.com/Torcode/bostotte-oslo/actions/workflows/kildeverifisering.yml)
[![Rapport-render (PDF)](https://github.com/Torcode/bostotte-oslo/actions/workflows/render.yml/badge.svg)](https://github.com/Torcode/bostotte-oslo/actions/workflows/render.yml)

Månedlig antall husstander med statlig bostøtte i Oslo, prognostisert 1–12
måneder fram på åpne data — bygget for planleggingsbehovet i en kommunal
analysefunksjon: dimensjonering av førstelinjen i bydelene, og tidlig varsel
når utviklingen avviker fra det ventede.

## Prognosen akkurat nå

| Målmåned | h | Punktprognose | 80 %-intervall | Betingelse |
|---|---|---|---|---|
| 2026m7 | 1 | 16 725 | 15 778–17 729 | vedtatt kalender |
| 2026m8 | 2 | 16 843 | 15 480–18 326 | vedtatt kalender |
| 2026m9 | 3 | 16 838 | 15 409–18 399 | vedtatt kalender |
| 2026m12 | 6 | 16 944 | 15 117–18 993 | vedtatt kalender |
| 2027m6 | 12 | 16 896 | 14 355–19 887 | videreført regelverk |

Forventet gjennomsnittlig månedlig antall mottakende husstander 2026m7–2027m6: **16 961** (punktestimat; intet aggregert intervall, se merknad i artefakten).

Basisbane per opprinnelse 2026m6, uttrekk 2026-08-04: 80 %-intervallene er tidsgyldig konformale og traff 79 % i backtesten — kalibrerte estimater, ikke garantier. Målmåneder etter 2026m12 forutsetter videreført regelverk (ingen vedtatt kalender).

### → [Utforsk prognosen 1–12 måneder fram](https://torcode.github.io/bostotte-oslo/)

Skyvebar over horisontene, intervaller, regelverksstatus per målmåned og
tabell med alle tolv radene. Siden leser den versjonerte artefakten
[`prognose/prognose_gjeldende.json`](prognose/prognose_gjeldende.json)
([CSV](prognose/prognose_gjeldende.csv)) og regner ingenting selv; artefakten
produseres maskinelt ved rendering og kontraktstestes i CI
([`scripts/validate_prognose.py`](scripts/validate_prognose.py)).

## Hovedfunnet

**Fortrinnet over naiv framskrivning kommer i det vesentlige fra datert
regelverksinformasjon, ikke fra modellkapasitet.** Serien er regelstyrt:
betinget på fem deterministiske regelverks- og kalenderledd er den stasjonær
(KPSS 1,03 → 0,16), og uten disse leddene faller både trebaserte, nevrale og
lineære modeller under den naive referansen (arbeidsverk 2).

Det sentrale enkeltresultatet er point-in-time: mot termin april 2024 —
seriens største bevegelse, et fall på 25 % på én termin — traff
hovedspesifikasjonen med **0,2 % avvik fra seks måneders horisont** (15 552
mot fasit 15 588), første opprinnelse etter at avviklingen ble offentlig
6. oktober 2023. Referansemodellene bommet med rundt 30 % fra samtlige
horisonter. Fra ni måneder — *før* kunngjøringen — treffer bare et eksplisitt
merket orakelscenario; point-in-time-modellen deler referansenes skjebne der,
og skal det. Skillet håndheves maskinelt med en port per prognoseopprinnelse
mot et primærkildebelagt kunnskapsregister
([`data/clean/regelverk_kunnskap.csv`](data/clean/regelverk_kunnskap.csv)).

Usikkerheten er målt, ikke lovet: modellenes egne intervaller underdekker
grovt (48 % ved nominelt 80 for hovedspesifikasjonen på
kalibreringsutvalget), tidsgyldig konformal etterkalibrering løfter dekningen
til 79 %, og restfeilen er skjevhet der informasjon mangler — ikke
intervallbredde. Intervallene publiseres derfor som kalibrerte estimater med
oppgitt målt dekning, ikke som garantier.

## Les arbeidet

| | |
|---|---|
| [`bostotte_oslo.pdf`](bostotte_oslo.pdf) | Hovedrapporten (45 sider): teori, metode, backtest, diskusjon, konklusjon — og prognosekapitlet som produserer artefakten |
| [`bostotte_oslo.qmd`](bostotte_oslo.qmd) | Kilden. All beregning kjører ved rendering; ingen tall i teksten er skrevet for hånd |
| [`rapport/`](rapport/) | Arbeidsverk 2: sammenfatning av Python-arbeidet, med versjonert kilde |
| [`notebooks/`](notebooks/) | Arbeidsverk 2, sju notebooks med lagret utdata (protokollport, ML-klasser, kalibrering, avstemming, kvalitetskontroll) |
| [`revisjon/`](revisjon/) | Uavhengig release-revisjon: claim-register, kryssrevisjon, gullsett, reproduksjonsskript og verifikasjonsrapporter |

> **Uavhengig prosjekt.** Dette er et privat fag- og porteføljeprosjekt. Det
> er ikke utført på oppdrag fra, eller i samarbeid med, Oslo kommune,
> Velferdsetaten eller Husbanken. Alt datagrunnlag er offentlig og aggregert;
> ingen person- eller registerdata inngår. Denne versjonen bygger på uttrekket
> datert **4. august 2026**.

## Beviskjeden

Rekkefølgen er bevisst: hvert ledd hviler på leddet før.

1. **Datagrunnlaget er verifisert, ikke antatt.** 55 maskinelle datakontrakter
   i ren Python kjører ved hver push (badge «Datakontrakt»), ni
   regnskapsidentiteter stopper renderingen ved avvik, og uttrekket er
   eksternt validert mot Husbankens publiserte årstall (avvik 0,00 til
   −2,10 %, med etterkontrollens signatur). Kontraktene er mutasjonstestet —
   de er vist å kunne stryke.
2. **Informasjonssettet er datert.** Hvert vedtaksavhengig regelverkssteg har
   en primærkildebelagt kunnskapsdato (Norsk Lovtidend, stortingsinnstillinger,
   regjeringen.no), og point-in-time-porten bruker steget i horisonten bare
   fra den datoen. Orakelkjøringer med dagens fasitkalender finnes utelukkende
   som eksplisitt merkede historiske illustrasjoner.
3. **Evalueringen er backtestet.** Rullerende opprinnelse: 31 opprinnelser ×
   8 modeller × horisont 1–12, med Clark–West på nøstede par, stratifisert på
   bruddnærhet og identifiserbarhet. Kjernetallene er uavhengig reprodusert i
   ren Python ([`revisjon/`](revisjon/)).
4. **Usikkerheten er tidsgyldig kalibrert.** Konformale intervaller bygges
   bare på feil som var realisert ved opprinnelsen, med endelig-utvalgsnivå;
   dekningen rapporteres som målt (48 → 79 % ved nominelt 80).
5. **Framtidsprognosen er én artefakt.** Rapportkapittel, README-utdraget over
   og den interaktive siden leser samme maskinproduserte fil, med opprinnelse,
   vintage, commit, intervallmetode og regelverksstatus per målmåned — og 13
   kontraktstester i CI.

## Reproduser

```r
source("oppsett.R")       # engangs: installerer pakkesettet og sjekker miljøet
source("verifiser.R")     # port: parse i C-tegnsett + referanseintegritet
```

```
quarto render bostotte_oslo.qmd
```

Renderingen er hele løypa: data lastes, kontrollene kjøres, modellene
estimeres, prognoseartefakten skrives og PDF-en bygges. Første kjøring tar
10–15 minutter (den rullerende kryssvalideringen er cachet etterpå). Uavhengige
etterkontroller uten R:

```
python scripts/validate_phase1.py     # 55 datakontrakter
python scripts/validate_prognose.py   # 13 kontrakter på prognoseartefakten
```

Miljøet er låst i [`renv.lock`](renv.lock) (R 4.3.3, eksplisitt pakkesett med
full avhengighetslukning); Quarto ≥ 1.7 med innebygd Typst — **ingen LaTeX**.
Badgene beviser nøyaktig det navnet sier: «Datakontrakt» er
Python-validatorene fra ren checkout, «Kildeverifisering» er parse- og
referansesjekken (`verifiser.R`), og «Rapport-render (PDF)» er en faktisk full
rendering fra ren checkout — den kjører på endringer i beregningsgrunnlaget og
på forespørsel, siden den er for tung for hver push.

## Hva ligger hvor

| Sti | Innhold |
|---|---|
| [`prognose/`](prognose/) | Den kanoniske prognoseartefakten (CSV + JSON), README-utdraget og den statiske prognosesiden |
| [`data/raw/`](data/raw/) | Rådata og primærkilder, arkivert slik de ble hentet |
| [`data/clean/`](data/clean/) | Bearbeidede serier og kuraterte oppslagstabeller, medregnet regelverkskalenderen og kunnskapsregisteret |
| [`data/docs/`](data/docs/) | [Kodebok](data/docs/kodebok.md) og [datakilder](data/docs/datakilder.md) |
| [`data/scripts/`](data/scripts/) | Uttrekksskript (Python) og R-laster for datapakken |
| [`scripts/`](scripts/) | CI-validatorene |
| [`logg/`](logg/) | Endringslogg med før, etter og begrunnelse per post |
| [`arkiv/`](arkiv/) | Tidligere utgaver med erratum-noter |
| [`mal/`](mal/), [`oppsett.R`](oppsett.R), [`verifiser.R`](verifiser.R), [`renv.lock`](renv.lock) | Byggemiljøet |

## Datagrunnlaget

Alt er åpne data, hentet maskinelt med reproduserbare skript. Det er et
designvalg: det gjør kunnskapsgrunnlaget etterprøvbart for enhver, og det
speiler arbeidsvilkårene til en analysefunksjon som skal dele metode og tall
uten å måtte etablere en avtale først.

| Kilde | Rolle | Frekvens × nivå | Dekning |
|---|---|---|---|
| [Husbankens statistikkbank](https://statistikk.husbanken.no/bostotte) | Utfallsserien: mottak, utbetaling, beløp, avslag | måned × Oslo/Norge/bydel/brukergruppe | 2010m1–2026m7 |
| [SSB 09895](https://www.ssb.no/statbank/table/09895/) | Leiemarkedsundersøkelsen | år × prissone × rom | 2012–2025 |
| [SSB 03013](https://www.ssb.no/statbank/table/03013/) | KPI for betalt husleie | måned | 1979–2025 (avsluttet 2025M12; etterfølgeren er [14700](https://www.ssb.no/statbank/table/14700/)) |
| [SSB 14710](https://www.ssb.no/statbank/table/14710/) | KPI-bro inn i 2026 | måned | 1920–2026 |
| [SSB 01222](https://www.ssb.no/statbank/table/01222/) | Befolkning, Oslo | kvartal | 1997K4–2026K1 |
| [Oslo kommunes statistikkbank](https://statistikkbanken.oslo.kommune.no/) | AAP, uføretrygd, sosialhjelp, befolkning og framskriving per bydel | år × bydel | tabellavhengig |
| Husbankens årsrapporter og regelverksveileder | Regelverkskalender og beregningsparametre | hendelsesdatert | 2020–2026 |

Utfallsserien er en fullstendig administrativ registrering hentet fra
statistikkbankens Qlik Engine-API — ikke et utvalg. Ved siden av ligger de
kuraterte oppslagstabellene bygget fra primærkilder: regelverkskalenderen,
kunnskapsregisteret med `effect_known_from` per vedtakssteg,
forskriftsparametrene, strømtiltakenes månedsbeløp, publiserte nasjonale
årstall og daterte effektanslag.

## Kjente begrensninger

Disse står her fordi de begrenser hva som kan konkluderes, ikke fordi de er
små.

- **Aggregerte data.** Take-up og berettigelse lar seg ikke skille; estimerte
  intervensjonseffekter er nettoeffekter der mekanisk og atferdsmessig respons
  er sammenblandet. Aggregatene identifiserer verken udekket boligbehov, full
  take-up eller kausale virkninger.
- **Ingen kontrollenhet i tid.** Hver regelendring treffer hele landet
  samtidig; effekter måles mot en modellert kontrafaktisk bane.
  Brukergruppeinndelingen gir derimot kontroller i *mekanismedimensjonen*.
- **Pseudo-sanntid.** Serien revideres bakover, og historiske vintages er ikke
  offentlig tilgjengelige. Evalueringen bruker gjeldende vintage — en kjent
  optimistisk skjevhet som rammer alle modellene likt.
- **Tynt anslagsgrunnlag.** Bare ett rent forhåndsanslag er publisert i
  materialet. For høstpakken 2024 finnes ingen husstandstall i noen av fire
  gjennomsøkte kildefamilier; verdien av eksterne anslag kan derfor bare
  demonstreres med perfekt informasjon som øvre grense (M7 orakel i
  rapporten), og en operativ `M7_prior` står uimplementert i påvente av en
  reell kilde.
- **Bibliografien er delvis verifisert.** 30 av 82 oppføringer har fortsatt
  metadata som ikke er slått opp mot primærkilde (merket `PLASSHOLDER` —
  merkesystemet *er* kontrollen, og `verifiser.R` teller resten ved hver
  kjøring). Kjernen av regelverkskilder er primærkildebelagt;
  verifiseringsloggen ligger i [`logg/kildeverifisering.md`](logg/kildeverifisering.md).
  Rapporten er ikke kildeferdig før resten er lukket.

## Åpenhet om KI-bruk

Prosjektet er bygget med KI som gjennomgående verktøy — utkast til kode og
tekst, feilsøking, revisjonsrunder og regenerering av dokumenter — styrt og
overprøvd av forfatteren. Erklæringen er presis framfor generell, fordi
kontrollnivået faktisk er differensiert:

- **Kontrollert maskinelt:** 55 datakontrakter og 13 artefaktkontrakter i CI
  fra ren checkout; ni regnskapsidentiteter, point-in-time-portens invarianser
  og modellvaktene stopper renderingen ved avvik; kontraktene er
  mutasjonstestet.
- **Verifisert mot primærkilder:** regelverkskalenderen og kunnskapsdatoene
  (Norsk Lovtidend, stortingsinnstillinger, regjeringen.no); kjernetallene i
  backtesten er i tillegg uavhengig reprodusert i ren Python
  ([`revisjon/`](revisjon/)).
- **Under arbeid:** bibliografiens resterende metadata og to delvis belagte
  intervensjonskilder (I11, I18) — synlig merket i filene og i
  [åpne issues](https://github.com/Torcode/bostotte-oslo/issues).
- **Ansvaret** for faglige valg, tolkninger og publisering ligger hos
  forfatteren. Feil som blir funnet, legges ut som issues med diagnose og
  rettelse framfor å bli stille rettet; begrunnelsen for hver endring ligger i
  [`logg/`](logg/) og i commit-meldingene.

## Status og veien videre

Fase 1 (datagrunnlag) og fase 2 (modeller, R + Python) er gjennomført og
backtestet; resultatene står i rapporten og arbeidsverk 2. Den operative
framtidsprognosen produseres nå som versjonert artefakt fra
hovedspesifikasjonen. Fase 3 (drift: kjøreplan, overvåkning på intervallskår,
registervedlikehold som rutine) er utredet i anbefalingene, men ikke bygget —
og nye modellklasser er bevisst utsatt til release-porten er lukket.

Arbeidslista ligger som [åpne issues](https://github.com/Torcode/bostotte-oslo/issues)
med diagnose og akseptansekriterier; feil lukkes med verifikasjonsbevis, ikke
med påstander.
