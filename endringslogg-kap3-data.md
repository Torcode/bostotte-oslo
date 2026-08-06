# Endringslogg: revisjon av datakapitlet og dokumentoppsettet (5. august 2026)

Full omskriving av datadelen i metodekapitlet (`unt_1.qmd`, avsnitt 3.1), pluss et
dokumentoppsett som gjør PDF-en presentabel og en opprydding i repoet. Denne loggen
oppgir for hver endring hva som ble endret, og hvorfor. Tallene i «etter»-kolonnene
er beregnet ved rendering fra datapakken i `velferdsetaten-data/`, uttrekk 4. august
2026, ikke skrevet av for hånd.

Utløsende tilbakemelding: kapitlet forklarte dårlig, dekning var oppgitt som om det
var vask, ingenting var reelt vasket, formbegrepet var udefinert, og PDF-en var
uleselig. Alle fem punktene er adressert nedenfor.

---

## A. Struktur og forklaring

**A1. Nytt åpningsavsnitt: idealdata mot faktisk datagrunnlag (3.1.1).**
Før: kapitlet startet med «Studiens datagenererende objekt er Husbankens
bostøttestatistikk» — altså med det vi har, uten å si hva problemet ber om.
Etter: et avsnitt som først spesifiserer det ideelle datagrunnlaget (månedlig
husstandspanel over alle husstander i Oslo, med inntekt, boutgifter, vedtaks-
hendelser og gjeldende regelparametre), så hva et slikt panel ville gitt som
aggregatet ikke kan gi (observert take-up; simulert i stedet for estimert
regeleffekt; separert identifikasjon av høstpakken 2024; talte strømmer), så
hvorfor vi ikke har det (personopplysninger, krever hjemmel og utleveringsavtale;
åpne data er et designvalg; historiske vintages arkiveres uansett ikke), så hva
aggregatet faktisk gir, og til slutt hva forskjellen koster — fire konsekvenser,
hver med sitt designsvar.
Begrunnelse: forskjellen mellom ideelt og faktisk datagrunnlag er ikke en
beklagelse, men listen over hvilke spørsmål studien kan besvare. Uten den blir
begrensningene noe leseren må oppdage selv, og det er den typen mangel en fagkomité
leser som manglende oversikt over eget design. Avsnittet gir også begrunnelsen for
at UA er formulert deskriptivt og for at høstpakken 2024 estimeres samlet — to valg
som tidligere sto som påstander uten forankring i datagrunnlaget.

**A2. Formbegrepet definert (3.1.4).**
Før: «De har fire *former*, og formen bestemmer den kanoniske operasjonen» — uten
å si hva en form er.
Etter: en form defineres eksplisitt som *kornet* (hvilken enhet én rad
representerer), og @tbl-former gir for hver av de fire formene kornet, det kanoniske
grepet og den karakteristiske feilen formen inviterer til.
Begrunnelse: «form» var terminologi uten definisjon. Definisjonen gjør inndelingen
operativ: den sier ikke bare hva datasettene heter, men hva man har lov til å gjøre
med dem og hvilken feil man gjør hvis man glemmer det.

**A3. Kildekartet flyttet fra eget avsnitt inn i datadelen (3.1.3).**
Før: `## Datagrunnlag og proveniens` sto som eget avsnitt *etter* datadelen, med
overlappende innhold.
Etter: kildekartet står i datadelen der det hører hjemme, og frekvenskolonnen er
fjernet fra tabellen fordi den nå beregnes i @tbl-dekning.
Begrunnelse: to steder som beskriver kildene, holdes ikke i takt. Frekvens oppgitt
to steder — én gang for hånd og én gang beregnet — er en feilkilde uten gevinst.

**A4. Kalenderidentiteten flyttet fra estimandavsnittet til datadelen (3.1.2).**
Før: @eq-kalenderidentitet ble definert i 3.2 (estimand), men brukt i 3.1
(verifikasjonstabellen) — en foroverreferanse.
Etter: identiteten defineres der de to kalendrene først beskrives, og
estimandavsnittet refererer tilbake.
Begrunnelse: identiteten er en egenskap ved dataene, ikke ved estimanden. Med
flyttingen leses kapitlet forlengs.

---

## B. Dekning skilt fra vask

**B1. Dekning er nå en egen, beregnet tabell (3.1.5, @tbl-dekning).**
Før: «Dekning» var en hardkodet kolonne i datasettoversikten, i et avsnitt som het
«Verifikasjon og vask».
Etter: eget avsnitt med en tabell som leser frekvens, første og siste periode og
antall perioder direkte fra objektene, pluss en kolonne for avstanden fra hver
kildes siste observasjon til utfallsseriens estimeringskant.
Begrunnelse: (i) dekning er en observasjon om kilden, vask er et inngrep vi gjør —
å oppgi dem under samme overskrift skjuler det skillet; (ii) hardkodet dekning går
ut på dato ved neste vintage; (iii) avstandskolonnen gjør argumentet for en
*deterministisk informert* hovedspesifikasjon synlig i en tabell istedenfor å ligge
som en påstand i løpende tekst.

**B2. Påstanden om at oversiktstabellen er «generert fra datasettene selv» gjort
sann.**
Før: tabelltekst hevdet at tabellen var generert fra datasettene, men bare rad- og
kolonnetall var beregnet; korn og dekning var skrevet for hånd.
Etter: dekning beregnes; korn er fortsatt kuratert, og tabellteksten sier nå
eksplisitt at det er den eneste kuraterte kolonnen. Oppslaget mot formtabellen er
sikret med `stopifnot(setequal(names(d), korn$objekt))`, slik at et uklassifisert
objekt i datapakken stopper renderingen.
Begrunnelse: en dokumentasjonspåstand som ikke holder, er verre enn ingen påstand.

---

## C. Vask: fra tom påstand til fullstendig regnskap

**C1. Vasken er nå spesifisert som to navngitte inngrep (3.1.7, @tbl-vask).**
Før: «Vaskingen er tilsvarende minimal og fullt spesifisert» etterfulgt av to
setninger, hvorav den ene («snittstørrelser beholdes som manglende») ikke er et
inngrep, men et ikke-inngrep.
Etter: tabell med Id, inngrep, omfang, begrunnelse og hva alternativet ville kostet.
V1 er fjerning av sanntidskanten; V2 er ommerking av node 0301 fra kildens «Oslo»
til «Ufordelt (0301)». Deretter en eksplisitt liste over de fem tingene vi ikke gjør
— ingen imputering, ingen uteliggerbehandling, ingen glatting eller
forhåndssesongjustering, ingen revisjon av historikk, ingen enhetsharmonisering —
med begrunnelse for hver.
Begrunnelse: påstanden «ingenting er vasket» må bæres av et argument, ikke av at
listen er kort. Argumentet er at en administrativ totaltelling ikke har målefeil å
vaske bort — tallet *er* antallet vedtak — men at den har representasjonsvalg som
må håndteres. Uten det argumentet står deskriptivdelen på løs grunn: leseren vet
ikke om tallene er kildens egne eller våre.

**C2. V2 er et nytt, tidligere udokumentert inngrep.**
Ommerkingen av 0301 lå i koden (`met-paneler`-chunken) uten å være omtalt som
databehandling.
Begrunnelse: kilden gir restkategorien samme navn som totalen. Å endre etiketten er
riktig, men det er et inngrep og skal stå i regnskapet.

**C3. Ubalansen i bydelspanelet dokumentert.**
Nytt: node 0301 er bare til stede i måneder der den har minst én husstand (162 av
199 måneder mangler). Panelet er altså ubalansert.
Begrunnelse: setningen «aggregér over enheter og få totalen» forutsetter at
manglende rader er nuller. Det er sant her, og at det er sant, verifiseres — men
det skulle vært sagt.

---

## D. Verifikasjon

**D1. Kontrollen stopper nå faktisk renderingen (3.1.6, @tbl-kontroller).**
Før: teksten lovet at «feiler én av dem etter en fremtidig dataoppdatering, feiler
renderingen av tabellen — ikke analysen stille». Koden beregnet og skrev ut, men
kastet ingen feil. Påstanden var usann.
Etter: chunken avsluttes med en `stop()` dersom noen kontroll feiler, og tabellen
har en statuskolonne.
Begrunnelse: en kontroll som ikke kan feile, er ikke en kontroll.

**D2. Prikkingskontrollen omformulert fra NA-telling til avstand til grensen.**
Før: «Prikking (celler < 4) på analysenivåene / ingen manglende antallsverdier /
0 NA». Fravær av NA er svakt bevis: en prikket celle trenger ikke komme som NA.
Etter: to uavhengige argumenter. Minste observerte positive celle på analysenivåene
er 277 husstander, to størrelsesordener over grensen på fire; og summeringsidentitetene
holder eksakt, hvilket de ikke ville gjort dersom en celle var maskert. NA-tellingen
beholdes som egen kontroll (K6), men gjør nå ikke jobben til prikkingskontrollen.
Begrunnelse: den gamle formuleringen brukte ett svakt bevis der to sterke var
tilgjengelige i dataene.

**D3. To nye kontroller.**
K4 (sammenhengende månedsrekke uten hull) og K6 (ingen manglende antallsverdier)
er skilt ut som egne kontroller.
Begrunnelse: hull i månedsrekka ville ødelagt både lag-operatorer og
sesongkomponent, og var tidligere ikke sjekket i det hele tatt.

---

## E. Deskriptiv del: fra oppsummering til observasjoner

**E1. Deskriptivdelen omskrevet til fem nummererte observasjoner med konsekvens
(3.1.9).**
Før: én tabell, ett avsnitt om nivå og volatilitet, og en figur.
Etter: fem observasjoner, hver med et beregnet tall og en eksplisitt konsekvens for
modellvalget.
Begrunnelse: en deskriptiv del som bare rapporterer, gir leseren ingen grunn til å
lese den. Hver observasjon skal enten begrunne et modellvalg eller felle et.

**E2. Ny tabell: de seks største månedsendringene slått opp mot regelverkskalenderen
(@tbl-hendelser).**
Nytt funn: fem av de seks største månedsendringene i estimeringsutvalget faller på
en datert regelendring (I01 inn og ut, I05 inn, I12, I14). Den sjette (termin mai
2021) gjør det ikke, og er meldekortsagtannen.
Begrunnelse: dette er den empiriske begrunnelsen for intervensjonsanalyse framfor
uteliggerdeteksjon, og den sto ingen steder. Oppslaget er automatisk, ikke manuelt.

**E3. Ny figur: mekanismetesten for 2025-skjermingen (@fig-vol).**
Nytt funn, beregnet på Oslo-data: gjennomsnittlig absolutt månedsendring i
behandlingsgruppen («husstander med midlertidige trygdeytelser») faller med faktor
5,0 fra 2025, mens de fire øvrige brukergruppene faller med faktor 1,3 til 2,3.
Begrunnelse: kapitlet hadde bare det nasjonale tallet (3 986 → 1 006 husstander) og
brukte det som en fotnote til kalenderregressoren. Oslo-versjonen med
kontrollgrupper er en helt annen type bevis: studien har ingen kontrollenhet i
tidsdimensjonen — hele landet er behandlet samtidig — men den har fire kontroller i
mekanismedimensjonen. Det gjør T3 til en skarp hypotese med en gruppe der effekten
skal finnes og fire der den ikke skal.

**E4. Aprilfallet 2024 presisert fra «over en femtedel» til beregnet verdi.**
Før: «tok ut over en femtedel av bestanden på én termin».
Etter: −25,2 %, beregnet ved rendering.
Begrunnelse: se G1 — det gamle anslaget stammet fra en feil i kodeboken.

---

## F. Reproduserbarhet i selve dokumentet

**F1. Hardkodede tall erstattet med inline-beregning.**
Før: «114 månedsobservasjoner», «rundt sytten tusen mottakere», «om lag åtte
prosent», «114 terminer × 17 kolonner», «(2017m1–2026m6)» — skrevet av for hånd i
kapittel 2 og 3, seks steder.
Etter: alle beregnes i oppsettchunken og settes inn med inline-R.
Begrunnelse: neste datavintage gir 115 observasjoner. Hardkodede tall blir da feil
uten at noe varsler om det, og et dokument med tall som ikke stemmer med sin egen
datapakke, er verdiløst som kunnskapsgrunnlag.

**F2. `stopifnot(nrow(analyse) == 114)` erstattet med `nrow(analyse) == n_est`.**
Før: en magisk konstant som ville brutt renderingen ved neste dataoppdatering — og
brutt den *feilaktig*, siden en lengre serie ikke er en feil.
Etter: kravet utledes av estimeringsutvalget.
Begrunnelse: en assertion skal fange feil, ikke fange normal utvikling.

**F3. Ny kontroll mot duplisering i strømstøtte-joinen.**
`left_join` mot `stromstotte` ville stille duplisert rader i X dersom kilden fikk
mer enn én rad per utbetalingsmåned (for eksempel ved geografisk oppdeling, som
allerede forekommer i kolonnen `geografi`). Lagt til
`stopifnot(!any(duplicated(strom_termin$dato)))` og `stopifnot(nrow(X) == nrow(mnd_seq))`.
Begrunnelse: joins mot oppslagstabeller er den vanligste stille feilen i denne typen
kode, og den ville gitt feil regressorlengde uten noen synlig feilmelding.

**F4. Meldekortgridet dekker nå hele serieperioden.**
Før: `u_av_fase()` genererte 14-dagersgridet fra ankerdatoen 2014-01-06 og framover,
slik at `u` var NA for alle måneder før 2014. Det gikk upåaktet hen fordi
estimeringsutvalget starter i 2017.
Etter: gridet rygges tilbake i hele 14-dagerssteg til før startdatoen, og
`stopifnot(!anyNA(X$u), all(X$u %in% c(2, 3)))` fanger avviket dersom det oppstår
igjen.
Begrunnelse: en regressor med usynlige hull utenfor estimeringsvinduet er en felle
for enhver robusthetsanalyse som utvider vinduet.

**F5. UTF-8 sikret uavhengig av vertsmaskin.**
Nytt: oppsettchunken setter UTF-8-locale dersom sesjonen ikke allerede har det.
Begrunnelse: i C-locale skriver `knitr::kable()` ikke-ASCII-tegn som `<U+00E5>`.
Dokumentet renderer riktig på Windows, men blir uleselig i container og i CI. Uten
dette kan ikke byggingen automatiseres.

**F6. Tusenskille byttet til hardt mellomrom (U+00A0).**
Begrunnelse: med vanlig mellomrom brakk «20 849» over to linjer i tabellene. Det er
den enkeltfeilen som gjorde de gamle tabellene vanskeligst å lese.

**F7. Kodeekko slått av (`echo: false`).**
Før: samtlige chunks skrev koden sin inn i PDF-en, som dermed inneholdt rå
dplyr-pipelines midt i løpende tekst.
Etter: koden er utelatt; kapitlet sier eksplisitt at koden ligger i `unt_1.qmd` og i
`velferdsetaten-data/scripts/`, og hver tabell oppgir hvilket objekt den er beregnet
fra.
Begrunnelse: proveniens sikres av at koden er versjonert og navngitt, ikke av at den
er limt inn i et dokument som skal leses av fagfolk i etaten.

---

## G. Faktafeil rettet i datapakkens dokumentasjon

**G1. Aprilfallet 2024 i kodeboken.**
Før: «I12 vinduslukking termin april 2024 (~25 000 ut nasjonalt; −21,6 % i Oslo på
én termin)».
Etter: «−25,2 % i Oslo på én termin, termin mars → termin april».
Begrunnelse: −21,6 % er endringen fra termin mars (20 849) til termin **mai**
(16 353), altså over to terminer og forbi bunnpunktet i april. Endringen på én
termin er 20 849 → 15 588 = −25,2 %. Feilen understøttet formuleringen «over en
femtedel» i metodekapitlet; begge er rettet.

**G2. Skrivemåten av bydel 0312.**
Kodeboken skrev «Grünerløkka», kilden skriver «Grunerløkka». Kodeboken sier nå
eksplisitt at kildens skrivemåte gjelder ved join, og at navnet normaliseres først
ved presentasjon.
Begrunnelse: en join på bydelsnavn med kodebokens skrivemåte ville gitt tom match.

**G3. Referanse til slettet fil.**
Kodebokens avsnitt 5 pekte på `03-metode-del1.qmd`. Peker nå på metodekapitlet i
`unt_1.qmd`, og kolonnetallet er oppdatert fra 17 til 19.

**G4. To nye feller lagt til kodebokens felleliste.**
Ubalansen i bydelspanelet (felle 9) og navnekollisjonen for node 0301 (felle 10).

---

## H. Dokumentoppsett

**H1. Egen Typst-mal (`mal/typst-template.typ`).**
Før: Quartos standardmal. Resultatet var brede tabeller med kolliderende kolonner,
tall som brakk over linjeskift, engelske kryssreferanser («Section 2.2»), numeriske
siteringer i klammeparentes, ingen tittelside, ingen innholdsfortegnelse og ingen
kolumnetittel.
Etter: A4 med tilpassede marger, tittelside, innholdsfortegnelse, kolumnetittel,
kapitler på ny side, booktabs-tabeller (linje over, under hodet og under tabellen —
ingen vertikale streker), venstrejusterte figur- og tabelltekster med halvfet
etikett, tabularfigurer slik at sifrene flukter, og brekkbare tabeller slik at en
lang tabell ikke etterlater en halvtom side.
Begrunnelse: dokumentet skal kunne legges fram for fagfolk i etaten. Standardrenderingen
signaliserte at ingen hadde sett på resultatet.

**H2. Språk satt til norsk bokmål (`lang: nb`).**
Effekt: «Tabell», «Figur», «Ligning» i kryssreferanser i stedet for engelske
prefikser, og korrekt norsk orddeling. `crossref: sec-prefix: "avsnitt"` overstyrer
Quartos «Seksjon», som er et anglisisme.
Begrunnelse: «jf. Section 2.2» midt i en norsk setning, og orddelingen
«inntek-tssikring», er feil et fagfellevurderende blikk fester seg ved umiddelbart.

**H3. Siteringer lagt om fra nummer til forfatter–år (`citeproc: true`).**
Før: «modelleres etter G. E. P. Box and G. C. Tiao [15]» — Typsts egen numeriske
stil, med engelsk «and».
Etter: «modelleres etter Box og Tiao (1975)», med referanseliste i forfatter–år og
norske bindeord.
Begrunnelse: nummerert IEEE-stil hører ikke hjemme i norsk samfunnsøkonomisk
litteratur, og engelske bindeord midt i norsk tekst er en språkfeil.

**H4. Bare innebygde fonter.**
Malen bruker Libertinus Serif og DejaVu Sans Mono, som Typst har innebygd.
Begrunnelse: en fontstabel gir ulikt resultat på ulike maskiner og fyller
byggeloggen med «unknown font family». Med innebygde fonter er PDF-en identisk på
Windows, macOS og i CI, og byggeloggen er ren.

**H5. To ligningsfeil rettet.**
`\!` (negativt tynt mellomrom) støttes ikke av Typst og ble satt som en skråstrek
midt i uttrykket — synlig i @eq-bostotte og @eq-estimand. Fjernet begge steder.

**H6. Y-aksen i @fig-serie er ikke lenger nullpunktforankret.**
Begrunnelse: bevegelsene kapitlet beskriver, er på 5–25 prosent av nivået. Mot en
akse fra null forsvant de. Valget er notert i figurteksten, slik at leseren ikke
villedes.

**H7. @fig-vol satt som hantelfigur, ikke helningsfigur.**
Begrunnelse: med fem grupper og tette verdier kolliderte serieetikettene. I
hantelfiguren bærer y-aksen identiteten, og avstanden mellom punktene er selve
budskapet.

---

## I. Opprydding i repoet

| Fjernet eller flyttet | Begrunnelse |
|:---|:---|
| `velferdsetaten-data/scripts/__pycache__/` | Python-bytekode. Regenereres av tolkeren; skal aldri versjoneres. Lagt inn i `.gitignore`. |
| `velferdsetaten-data/data/raw/hb_aarsrapporter.html` | Duplikat-scrape av samme side som `hb_arsrapporter.html`, ulikt innhold fordi den ble hentet på nytt. To kopier av samme kilde uten at det er sagt hvilken som gjelder, er verre enn én. |
| `velferdsetaten-data/scripts/extract_bostotte.py` | Erstattet av `extract_bostotte_v2.py`. Datakildedokumentasjonen viser bare til v2. |
| `03-metode-del1.qmd` | 66 % av linjene var duplisert inn i `unt_1.qmd`, med avvikende avsnittsrekkefølge og en `sec-met-sett`-referanse som ikke lenger fantes. To versjoner av samme kapittel holdes ikke i takt. |
| `explore_app.py`, `explore_vars.py`, `debug_kommune.py` → `scripts/utforsking/` | Kartleggingsskript fra byggedagen. De hører til dokumentasjonen av hvordan datamodellen ble funnet, ikke til uttrekksløypa. Flyttet, ikke slettet, og omtalt i `datakilder.md`. |

`.gitignore` utvidet med `__pycache__/`, `*.py[cod]` og Typst-mellomfiler.

---

## Ikke endret — bevisste valg

Kapittel 1 og 2 er ikke revidert på nytt i denne runden; endringene der er begrenset
til de seks hardkodede tallene i F1. Modell-, protokoll- og evalueringsdelen (del 2)
er fortsatt en stub. Intervensjonsmatrisen og kalenderregressoren er innholdsmessig
uendret; endringene i de avsnittene er de tre nye kontrollene (F3, F4) og
oppdaterte referanser. De to PDF-ene i rotkatalogen er ikke rørt — de er ikke sitert
i `referanser.bib`, men det er en beslutning om litteraturgrunnlag, ikke om rydding.

## Reproduksjon

```
quarto render unt_1.qmd
```

Bygger dokumentet uten advarsler. Feiler en av verifikasjonskontrollene i 3.1.6,
stopper byggingen med melding om hvilken. Avhengigheter: R med `tidyverse` og
`knitr`, Quarto ≥ 1.7 (Typst-motoren følger med). Ingen LaTeX kreves.

---

# Datakvalitetsrevisjon (5. august 2026, andre runde)

Full revisjon av datagrunnlaget før estimeringen settes i gang. Revisjonen testet
det verifikasjonen i første runde ikke dekket: aritmetikken *mellom* kolonnene,
uttrekket mot en ekstern kilde, og om regressorene i det hele tatt lar seg estimere
i et rullerende treningsvindu. Den fant to reelle problemer og bekreftet resten.

## Konklusjon først

Datagrunnlaget holder. Alle interne regnskapsidentiteter holder eksakt, uttrekket
reproduserer Husbankens publiserte nasjonale beløp innenfor 2,1 % i alle fem år, og
kovariatene stemmer med sine kilder. To ting må likevel endres, og den ene av dem
ville brutt estimeringskjøringen.

## R1. `ant_soknader` er ikke data — den er en identitet

**Funn.** `ant_soknader − ant_avslag = ant_husstander_termin` holder *eksakt*, i hver
måned, på hvert aggregeringsnivå (nasjonalt avviker ett månedspar med ≤ 2 husstander,
avrunding). Søknadsserien er altså summen av innvilgede og avslåtte saker i
terminkjøringen — en definisjonsmessig identitet.

**Hva som var galt.** Observasjon 2 i @sec-met-observasjoner sa at søknader og avslag
«er kandidater til ledende informasjon om strømmene i @eq-stockflow». For søknader er
det uriktig per konstruksjon: den kan ikke lede en størrelse den er en
lineærkombinasjon av. For avslag er det empirisk uriktig: korrelasjonen mellom
avslagsandelen og endringen i mottakertallet er −0,58 samtidig og +0,50 på én måneds
lag (mekanisk tilbakeslag), men 0,04 og 0,02 på to og tre måneders lag. En serie som
først røper seg samtidig med utfallet, varsler ingenting.

**Endring.** Observasjon 2 skrevet om fra «saksvolumet er mangedoblet mottakstallet»
til «av de tre seriene er bare to uavhengige — og den tredje leder ingenting», med
begge tallene. Identiteten lagt inn som kontroll K7. Kodeboken har fått et nytt
avsnitt 5b med de verifiserte identitetene og to nye feller (11 og 12).

**Hvorfor det betyr noe.** Deskriptivtabellen presenterer tre serier. Uten dette
funnet ville en leser — eller vi selv i del 2 — kunne brukt søknadsserien som
prediktor for mottakertallet, altså regressert en størrelse på seg selv.

## R2. Regressorene kan ikke estimeres før hendelsen har skjedd

**Funn.** En intervensjonsregressor er null helt til hendelsen inntreffer. Ved en
prognoseopprinnelse før hendelsen er kolonnen identisk null i treningsvinduet, og
koeffisienten finnes ikke. Omfanget:

| Regressor | Opprinnelser uten identifikasjon (av 31) | Rammede prognosepunkter |
|:---|---:|---:|
| `pakke_2024h2` | 24 | 138 |
| `k_post` | 30 | 138 |

210 av 372 prognosepunkter (56 %) har minst én aktiv regressor som ikke var
estimerbar ved opprinnelsen. Andelen stiger fra 39 % på horisont 1 til 74 % på
horisont 12, og er konsentrert i opprinnelsesårene 2024 (90 %) og 2025 (83 %).

**Hva som ville skjedd uten funnet.** Enten en rangdefekt designmatrise og en
avbrutt kjøring, eller — verre — at modelltilpasningen stilltiende dropper de
kollineære kolonnene. I det andre tilfellet ville «M6» vært syv ulike modeller over
de 31 opprinnelsene uten at noen sto oppført, og sammenlikningen M6 mot M3 ville
målt noe annet enn den utgir seg for.

**Endring.** Nytt avsnitt 3.7.1 med (i) en eksplisitt inngangsregel — en regressor
inngår ved opprinnelse τ hvis og bare hvis den har minst seks ikke-null observasjoner
i treningsvinduet, ellers utelates den og det logges; (ii) tabell `tbl-identifikasjon`
som beregner omfanget ved rendering; og (iii) en presisering av hva studien kan
konkludere med. Evalueringen i 3.8 stratifiseres nå også på om regressoren var
estimerbar, og T2 i `tbl-tester` er omformulert tilsvarende.

**Og en gevinst.** Funnet gir underspørsmål **UB** et skarpere svar enn spørsmålet
ble stilt med. For en regelendring som er *vedtatt, men ikke trådt i kraft*, kan
effektstørrelsen ikke estimeres fra serien — den må hentes utenfra. Studien har
allerede kilden: departementets forhåndsanslag på 20 000–25 000 mottakere nasjonalt
for avviklingen i april 2024, bekreftet til om lag 25 000 i etterkant. Et
forhåndsanslag omregnet til Oslos andel er en datert, etterprøvbar prior — nøyaktig
den informasjonen en prognose i drift ville hatt. Om den skal brukes som pålagt
koeffisient, avgjøres i del 2.

## R3. Ekstern validering lagt til (ny seksjon 3.1.7)

Regnskapsidentitetene er interne: de ville holdt også om hele uttrekket var
systematisk feil. Uttrekket er derfor regnet opp mot Husbankens publiserte nasjonale
årstall (årsrapport 2025, tabell 3.1), lagt inn i datapakken som
`arsrapport_nokkeltall.csv`.

| År | Publisert (mill.) | Uttrekk (mill.) | Avvik | Omløp |
|---:|---:|---:|---:|---:|
| 2021 | 2 714 | 2 714 | 0,00 % | 1,47 |
| 2022 | 3 262 | 3 193 | −2,10 % | 1,48 |
| 2023 | 3 610 | 3 569 | −1,15 % | 1,44 |
| 2024 | 3 781 | 3 747 | −0,90 % | 1,57 |
| 2025 | 4 100 | 4 062 | −0,93 % | 1,41 |

To svar. Uttrekket treffer, og omløpstallet (unike husstander gjennom året delt på
snittbeholdning) ligger stabilt på 1,41–1,57 — ingen endring i telleregelen har
sneket seg inn. Men avviket er *ensidig negativt* fra 2022, mens 2021 stemmer
eksakt. Et systematisk underskudd på om lag én prosent er akkurat det etterkontrollen
mot skatteoppgjøret produserer: statistikkbanken viser omregnet rett etter
tilbakekreving, årsrapporten viser hva som faktisk ble utbetalt. Dette er den
empiriske bekreftelsen på revisjonsmekanismen 3.1.2 beskriver — som til nå bare var
sitert — og den har en konsekvens: beløpsserien modellerer *rett*, ikke kasse. For
antallsserien er forskjellen uten betydning.

## R4. Tre nye kontroller

| | Kontroll | Resultat |
|:---|:---|:---|
| **K7** | Saksidentitet: søknader − avslag = mottakere | avvik 0 |
| **K8** | Begge disaggregeringer summerer for **alle seks** mål, ikke bare antallet | avvik 0 |
| **K9** | Beløpsidentitet: beløp / antall = snittkolonnen | maks 0,005 kr |

K8 er den som utvider dekningen mest: første runde testet bare antallsserien, og
lot beløp, søknader, avslag og over-tak stå usjekket på begge disaggregeringene.
Alle fire holder eksakt.

## R5. Bekreftet uten endring

* **Kovariatene stemmer med sine kilder.** KPI-broen 03013/14710 har konstant forhold
  i overlappet (variasjonskoeffisient 0,0008 over 564 måneder). Bydelssummene av
  folkemengde treffer SSBs kvartalstall innenfor 0,51 %. Befolkningsframskrivingen
  for 2025 treffer observert folketall på 12 personer av 724 290 — som den skal,
  siden 2025 er framskrivingens basisår, men det bekrefter at aggregeringen fra
  delbydel er riktig.
* **Intervensjonstabellen er internt konsistent.** `termin_fra ≤ termin_til` i alle
  rader, og `utbetaling_fra = termin_fra + 1 måned` i alle 20. To rader er flagget
  «delvis» og gjelder strømbeløp, ikke datering.
* **Regelmotoren er forenlig med snittkolonnene.** Egenandelen implisert av observert
  snittboutgift og snittbostøtte ligger på 31–54 % av snittinntekten, og faller i
  2020 og 2022 — nøyaktig der koronareglene og strømtiltakene senket den. Det er en
  uavhengig bekreftelse på at intervensjonsdateringene er riktige.
* **Designmatrisen er velkondisjonert** når alle regressorer er aktive:
  kondisjonstall 4,8, ingen parvis korrelasjon over 0,3.
* **Snittkolonnene bærer lite selvstendig informasjon.** Snittboutgift og
  snittinntekt korrelerer 0,87, og andelen over boutgiftstaket ligger stabilt på
  83–85 %. De er nærmere en prisindeks enn en atferdsindikator, og brukes ikke som
  prediktorer.

## Filer endret

`unt_1.qmd` (ny seksjon 3.1.7 og 3.7.1, omskrevet observasjon 2, tre nye kontroller,
stratifisering på identifikasjon), `velferdsetaten-data/data/clean/arsrapport_nokkeltall.csv`
(ny), `velferdsetaten-data/scripts/velferdsetaten_data.R` (laster den),
`kodebok.md` (nytt avsnitt 5b, nytt datasett, fire nye feller), `datakilder.md`.

---

# M7: prior-varianten (5. august 2026, tredje runde)

Designvalget etter datakvalitetsrevisjonen: skal effektstørrelsen for en vedtatt,
men ikke ikrafttrådt regelendring hentes utenfra som en egen modell, eller holdes
til robusthetsanalysen? Valgt: egen modell.

**Begrunnelsen er at det ikke finnes noe nøytralt alternativ.** Å utelate
regressoren pålegger β = 0 — altså en påstand om at en regelendring Stortinget
allerede har vedtatt, ikke vil ha effekt i Oslo. Det er en sterkere antakelse enn å
bruke departementets eget publiserte anslag. Valget står mellom å pålegge null og å
pålegge det beste daterte tallet som finnes; M7 gjør valget eksplisitt og
kildebelagt i stedet for implisitt.

Stillingen dette arbeidet retter seg mot, ligger i en analyse- og
utredningsseksjon som leverer kunnskapsgrunnlag, framskrivinger og
beslutningsgrunnlag. Spørsmålet «hvor mange Oslo-husstander» kommer når endringen
varsles i statsbudsjettet i oktober, ikke etter at den har trådt i kraft i januar.
En modell som først kan svare fra måned syv, svarer etter at beslutningen er tatt.

## M1. Ny modell M7 (avsnitt 3.6.1)

M7 er identisk med M6 bortsett fra ett offset-ledd for regressorer som ikke passerer
inngangsregelen ved opprinnelsen. Leddet inngår i prognosen, men ikke i
estimeringen, slik at det ikke forstyrrer de øvrige koeffisientene.

Anslagene hentes fra ny fil `forhandsanslag.csv` og skaleres med Oslos målte andel
av mottakerne (18,5 %, målt i revisjonen). Tabellen skiller tre typer, og skillet er
ikke kosmetisk: `forhaand` er publisert før hendelsen og er det eneste en prognose i
drift ville hatt; `etterberegnet` er realisert utfall og kan bare brukes til å
validere metoden; `mekanisk` er utledet av regelverket.

**Prioren skal scores, ikke tros.** For `win_strom` finnes både et publisert anslag
og en estimerbar koeffisient. Metoden kalibreres derfor ved å sammenlikne β̂ mot
prior-implisert λ der begge finnes. Treffer de publiserte tallene, er det belegg for
å bruke dem der estimering er umulig; treffer de ikke, er det funnet — og det
forteller hvor mye vekt en konsekvensutredning tåler. Ny T5 i `tbl-tester` med begge
leddene.

## M2. Korreksjon av mitt eget funn R2 fra forrige runde

Da jeg gikk til kildene for å bygge prior-tabellen, viste det seg at R2 var for
grovt formulert. To presiseringer, begge inn i 3.7.1:

**`k_post` er rammet på en ufarlig måte.** Utelatelse pålegger β = 0, og null er
*nøyaktig* det regelmekanikken predikerer: 3 × ⅔ = 2. Utelatelse og korrekt prior
sammenfaller. De 138 rammede punktene for `k_post` er derfor ikke et problem å løse,
men en tilfeldighet i vår favør — og det burde stått. Bare `pakke_2024h2` er
genuint skadelidende, fordi kildene der sier at effekten er positiv.

**Aprilbruddet 2024 er ikke rammet i det hele tatt.** Seriens største bevegelse
bæres av `win_strom`, som er identifisert ved alle 31 opprinnelser fordi vinduets
*åpning* ligger i treningsvinduet. Modellen kan framskrive lukkingen selv om
lukkingen ligger i horisonten. Forrige runde antydet at identifikasjonsproblemet
rammet den hendelsen studien er mest opptatt av. Det gjør det ikke.

Begge presiseringene gjør funnet mindre dramatisk enn først formulert. De står her
fordi en endringslogg som bare registrerer det som styrker konklusjonen, er
verdiløs.

## M3. En kjent begrensning, notert framfor fylt

Høstpakken 2024 — regressoren som faktisk er uidentifisert ved flest opprinnelser —
har ingen publiserte husstandstall. Årsrapporten oppgir bare kronebeløp (14, 22 og 8
mill.), og oppvarmingstillegget gikk dessuten til *eksisterende* mottakere, slik at
en kroner-til-husstander-omregning ville vært direkte feil. Radene står som `ingen`
i `forhandsanslag.csv` med kilde og merknad. M7 kan altså ikke demonstreres på den
hendelsen før anslaget er hentet fra Prop. 1 S / RNB 2024. Det er notert som en åpen
verifiseringsoppgave på linje med de øvrige `delvis`-flaggene, framfor å fylles med
et konstruert tall.

## Filer endret

`unt_1.qmd` (M7 i modellstigen, nytt avsnitt 3.6.1, presisert 3.7.1, ny T5,
protokolltallene oppdatert til åtte modeller),
`velferdsetaten-data/data/clean/forhandsanslag.csv` (ny),
`velferdsetaten-data/scripts/velferdsetaten_data.R`, `kodebok.md`, `datakilder.md`.

## M4. Kildesøk etter de manglende anslagene (5. august 2026)

Søkt etter husstandstall for høstpakken 2024, som M3 flagget som åpen oppgave.
Ett nytt anslag funnet, ett hull bekreftet lukket som ikke-eksisterende, og ett
metodisk funn på kjøpet.

**Funnet: koronavinduet har et publisert anslag.** Husbankens pressemelding
14. juni 2020 oppgir at «om lag 13 000 husstander ekstra kan få bostøtte som følge
av økte inntektsgrenser». Lagt inn som I01 med `anslag_type = samtidig`, ikke
`forhaand`: den ble publisert to terminer *inn* i vinduet, og kunne derfor ikke
vært brukt i en prognose laget før april 2020. Skillet står i tabellen fordi det
avgjør om anslaget kan brukes operativt eller bare til å kalibrere metoden.

Med I01 har tre hendelser nå både et publisert anslag og en estimerbar koeffisient:
koronavinduet, strømvinduets åpning og avviklingen i april 2024. T5 har dermed tre
kalibreringspunkter i stedet for ett.

**Hullet er bekreftet, ikke bare antatt.** Fire kildefamilier gjennomsøkt for
høstpakken 2024: Husbankens årsrapporter 2024 og 2025, Prop. 104 S (2023–2024),
Husbankens egen pressemelding om revidert nasjonalbudsjett, og Innst. 16 S
(2024–2025). Alle oppgir kroner — 85 mill. for boutgiftstaket, 22 mill. for
oppvarmingstillegget, 8 mill. for 18/19-årsregelen — og ingen oppgir husstander.
Radene står nå som `ingen` med søkedato og kildeliste, slik at neste person ikke
gjentar søket. For oppvarmingstillegget ville en omregning fra kroner dessuten vært
direkte feil: tillegget gikk til *eksisterende* mottakere og hevet beløp framfor å
utvide kretsen.

**Det metodiske funnet: rå før-og-etter-differanser duger ikke til kalibrering.**
Ved å regne realisert endring mot publisert anslag for de tre hendelsene, kommer
forholdet ut mellom om lag 0,5 og 0,8 — altså at anslagene systematisk overdriver.
Den konklusjonen holder ikke, og grunnen er tre forhold kapitlet allerede har
dokumentert hver for seg: positive endringer fases inn gradvis, så en kort
etterperiode undervurderer effekten; hendelsene overlapper, så nedgangen etter
april 2024 motvirkes delvis av høstpakken fra juli; og kalendersagtannen på 7–10 %
dominerer enhver enkeltmåneds differanse. Spriket måler altså metoden, ikke
anslagene.

Avsnitt 3.6.1 har fått et eget punkt om dette, og T5 er allerede formulert mot den
estimerte koeffisienten framfor mot en differanse — nå med begrunnelsen skrevet ut.
Tallene fra det rå regnestykket er bevisst *ikke* tatt inn i kapitlet: de ville
blitt lest som et resultat, og de er ikke det.

**Filer endret:** `velferdsetaten-data/data/clean/forhandsanslag.csv` (I01 lagt til,
kildelister og søkedato på 2024-radene), `unt_1.qmd` (3.6.1), `kodebok.md`,
`datakilder.md`.

## M5. Repoet ryddet, dokumentet omdøpt (5. august 2026)

Arbeidsfila het `unt_1.qmd` — et internt utkastnavn. Den heter nå
`bostotte_oslo.qmd`, som er det en leser av repoet leter etter. Innholdet er
uendret ved omdøpingen; det er utelukkende et navnebytte, gjort i sitt eget steg
nettopp for at diffen skal vise det.

**README skrevet om for en leser, ikke for forfatteren.** Den åpner nå med
spørsmålet, en uavhengighetserklæring (privat prosjekt, ikke på oppdrag fra Oslo
kommune, Velferdsetaten eller Husbanken, uttrekk frosset 4. august 2026), fire
hovedfunn med tall, byggeinstruks, kildetabell med lenker, og en egen liste over
kjente begrensninger. Begrensningene står der fordi de begrenser hva som kan
konkluderes — ikke som pliktløp.

**To feil i min egen README, rettet.** Jeg oppga `patchwork` som avhengighet; den
brukes ikke i dokumentet, bare i et frittstående figurskript jeg lagde underveis.
Og jeg skrev «fire plassholdere i `referanser.bib`». Det tallet var galt i min
favør: seks oppføringer trykker plassholdertekst i selve referanselisten, og 37 av
83 er merket `note = {PLASSHOLDER}` — forfatter, tittel og år er kontrollert, men
utgiver, URL og sidetall er ikke verifisert mot primærkilde. Det er samme feiltype
som kapitlet ellers kritiserer, begått av meg, og står nå med riktig tall i README.

**PDF-en versjoneres bevisst.** `bostotte_oslo.pdf` er tatt ut av `.gitignore`.
Genererte filer hører normalt ikke hjemme i et repo, men her er PDF-en selve
leveransen: en leser skal kunne se resultatet uten å installere R, Quarto og ni
pakker først. Kostnaden er at den må bygges på nytt før hver innlevering, ellers
ligger den i utakt med kilden.

**`oppsett.R` lagt til.** Installerer bare det som faktisk mangler, sjekker at
pakkene lar seg laste, at filene ligger der de skal, at datapakken lastes, og
rapporterer Quarto-versjon. Den finnes fordi «kjør `install.packages`» ikke er en
byggeinstruks — den sier ikke hva som gikk galt når noe går galt.

**Filer endret:** `unt_1.qmd` → `bostotte_oslo.qmd`, `README.md`, `oppsett.R` (ny),
`.gitignore`, `mal/typst-template.typ`.

## M6. Portabilitetsfeil i oppsett-chunken (6. august 2026)

Dokumentet renderte hos meg og feilet hos brukeren, med
`Error in file(): cannot open the connection` på `source()`-kallet i chunk
`oppsett` — samtidig som `source("oppsett.R")` i konsollen lastet datapakken uten
problemer. Feilen er min, og typen er verdt å notere: jeg hadde skrevet

```r
DATASTI <- "velferdsetaten-data"
```

altså en relativ sti, med den underforståtte antakelsen at render-prosessen står i
samme mappe som konsollen. Det gjør den ikke nødvendigvis. Arbeidsmappa under
rendering avhenger av om det bygges fra konsollen, fra Render-knappen i RStudio,
fra `quarto preview`, eller fra CI — og en antakelse som holder på én maskin er
ikke en antakelse, det er flaks.

**Rettelsen leter på tre steder** — arbeidsmappa, dokumentets egen mappe
(`knitr::current_input(dir = TRUE)`), og full sti — og **åpner** fila før
kandidaten godtas, framfor bare å sjekke at den finnes. Den siste forskjellen er
ikke pedanteri: prosjektmappa ligger i OneDrive, og en fil som bare finnes i skyen
gir nøyaktig samme feilmelding selv om `file.exists()` er sann. De to årsakene har
ulik løsning, så feilmeldingen skiller dem nå og navngir både arbeidsmappa og
dokumentmappa i klartekst.

Jeg vet ikke sikkert hvilken av de to som var årsaken hos brukeren — begge passer
med observasjonen. Det står her framfor å bli glattet over, og rettelsen dekker
begge. Skulle den komme tilbake, sier meldingen selv hvilken det var.

**Filer endret:** `bostotte_oslo.qmd` (chunk `oppsett`).
