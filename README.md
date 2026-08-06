# Prognose for statlig bostøtte i Oslo

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
> eller registerdata inngår. Uttrekket er frosset per **4. august 2026** — kilden
> revideres bakover, og resultater må derfor alltid knyttes til den datoen.

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

```r
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

| Sti | Innhold |
|---|---|
| `bostotte_oslo.qmd` | Hele arbeidet: teori, metode, resultater. All beregning kjører ved rendering |
| `mal/typst-template.typ` | Dokumentmal (A4, booktabs-tabeller, norsk typografi) |
| `referanser.bib` | Litteraturliste |
| `velferdsetaten-data/data/raw/` | Rådata og primærkilder, arkivert slik de ble hentet |
| `velferdsetaten-data/data/clean/` | Bearbeidede serier og kuraterte oppslagstabeller |
| `velferdsetaten-data/scripts/` | Uttrekksskript (Python) og R-laster for datapakken |
| `velferdsetaten-data/docs/` | `datakilder.md` (hvor tallene kommer fra) og `kodebok.md` (hva hver kolonne betyr) |
| `litteratur/` | Bakgrunnsrapporter som siteres i teksten |
| `endringslogg-*.md` | Hva som er endret underveis, og hvorfor |

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

**Datagrunnlaget er verifisert, ikke antatt.** Ni regnskapsidentiteter kjøres ved hver
rendering, og en kontroll som feiler stopper byggingen. Uttrekket er dessuten validert
eksternt mot Husbankens publiserte nasjonale årstall: avvik på 0,00 til −2,10 % over
fem år, med et ensidig negativt avvik som er signaturen til etterkontroll mot
skatteoppgjøret. Beløpsserien måler altså omregnet rett, ikke utbetalt kasse.

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
- **Bibliografien er ikke kildeferdig.** Seks oppføringer har plassholdertekst som
  faktisk trykkes i referanselisten — fire mangler forfatter eller tittel
  (`fjelltoft2024`, `astrup2024`, `menon2020`, `pedersen2023`), to mangler
  tidsskrift (`nordvik2005`, `nordvik2014`). I tillegg er 37 av 83 oppføringer
  merket `note = {PLASSHOLDER}`: forfatter, tittel og år er riktige så langt de er
  kontrollert, men utgiver, URL og sidetall er ikke verifisert mot primærkilde.
  Rapporten kan derfor ikke leveres som kildeferdig slik den står.

## Status

Kapittel 1–4 er skrevet og bygger uten advarsler. Rullerende opprinnelse er kjørt: 31
opprinnelser, 8 modeller, horisont 1–12, med Clark–West på nøstede par og konformal
etterkalibrering. Resultatene i kapittel 4 er dermed backtestede, ikke påstander.

Modellklassene bayesiansk strukturell tidsserie, gradientboosting og hierarkisk
avstemming er spesifisert i teorikapitlet, men **ikke estimert**. Det finnes ingen
publisert framtidsprognose og ingen produksjonsmodell. Neste steg er beskrevet sist i
kapittel 4; åpne oppgaver ligger som [issues](https://github.com/Torcode/bostotte-oslo/issues).
