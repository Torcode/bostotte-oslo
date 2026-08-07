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

## M7. Tre defekter som bare fantes på andres maskin (6. august 2026)

Dokumentet rendret feilfritt i utviklingsmiljøet og feilet på brukerens maskin.
Tre defekter, samme rot: antakelser om vertsmaskinen som mitt miljø tilfeldigvis
oppfylte. Alle tre lå i `unt_1.qmd` før omdøpingen — den første stoppet
renderingen på chunk 1, så de to andre ble aldri nådd. Det er verdt å skrive ned
som det er: *jeg behandlet «den rendrer her» som «den rendrer».*

**D1. Datastien var relativ.** `DATASTI <- "velferdsetaten-data"` forutsetter at
arbeidsmappa under rendering er den samme som i konsollen. Det avhenger av om
det bygges fra konsollen, fra Render-knappen, fra `quarto preview` eller fra CI.
Rettet: tre kandidater prøves — arbeidsmappa, dokumentets egen mappe via
`knitr::current_input(dir = TRUE)`, og full sti — og kandidaten må la seg *åpne*,
ikke bare finnes. Den siste forskjellen er ikke pedanteri: prosjektmappa ligger
i OneDrive, og en fil som bare finnes i skyen gir samme feilmelding som en fil
som ikke finnes.

**D2. Norske tegn i R-navn.** `transmute(År = ...)` og `tibble(Mål = ...)`.
Om en ikke-ASCII bokstav er gyldig i et R-navn avgjøres av *locale*. I en
UTF-8-locale er den det; i en C-locale skriver R bokstaven som escapen
`<U+00C5>`, og parseren stopper på vinkelparentesen. Feilen er usynlig for den
som utvikler i UTF-8 og total for den som ikke gjør det. Rettet med
bakoverfnutter. Merk skillet: norske tegn i *strenger og kommentarer* er
uproblematiske — det er navnene som ikke tåler det.

**D3. Hardt mellomrom som byte i kildekoden.** `big.mark` var en literal U+00A0.
En slik literal leses som «unknown» encoding, og R kan escape den på vei ut;
resultatet var at hvert tusenskille sto som `17<U+00A0>060` i PDF-en — på hver
side med et tall over tusen. Skrevet som R-escape (`" "`) blir strengen
korrekt UTF-8-merket. Feilen var synlig i PDF-en hele tiden; jeg hadde ikke sett
etter den.

**Vakten som ikke stoppet.** Alle tre hadde en locale-vakt over seg som skulle
hindre nettopp dette. Den prøvde bare Unix-navn (`C.UTF-8`, `nb_NO.UTF-8`), som
ikke finnes på Windows, og feilet *stille*. Den lot dokumentet fortsette mot den
feilen den var laget for å stoppe. Vakten prøver nå ni navn i begge familier, og
tester symptomet framfor navnet: overlever en UTF-8-merket streng turen ut til
vertens tegnsett? Går det ikke, **stopper** byggingen med beskjed om hva som må
endres. En vakt som ikke stopper er ingen vakt.

**En NaN i løpende tekst.** Siste rad i uttrekket er strukturell null i både
Oslo- og landsserien — terminkjøringen er ikke gjort ennå. Analysen fjerner den
(vaskeinngrep V1), men ett inline-tall regnet Oslos andel direkte på rådataene,
og 0/0 ble stående som `NaN %` i PDF-en. Landsserien trimmes nå etter samme
regel som Oslo-serien, og andelen regnes i oppsett-chunken med en `stopifnot`
på seg.

Det systematiske svaret er viktigere enn den enkelte rettelsen: `nb()` og `pst()`
stopper nå selv på NA, NaN og Inf. Ni regnskapsidentiteter stoppet byggingen,
men ingen av dem så på et enkelt inline-tall. Skillet mot aksemerker er bevisst
— `nb_akse()`/`pst_akse()` tolererer NA, fordi ggplot2 med vilje sender NA for
kandidatbrudd utenfor skalaen. *En NA i en akse er normal, en NA i en setning er
en feil.* Den første versjonen av vakten skilte ikke, og stoppet renderingen på
sin egen falske positive.

**Nytt: `.Rprofile` og `verifiser.R`.** `.Rprofile` setter UTF-8 ved oppstart,
også i R-prosessen Quarto starter. `verifiser.R` parser hver chunk og hvert
inline-uttrykk i en egen prosess med `LC_ALL=C` — altså i det verste tegnsettet
en leser kan ha — og kontrollerer at ingen bibliografioppføring trykker
klammetekst. Begge kontroller er testet i begge retninger: de faller på den
gamle koden og passerer på den nye.

**Filer endret:** `bostotte_oslo.qmd`, `.Rprofile` (ny), `verifiser.R` (ny),
`.gitignore`, `README.md`, `oppsett.R` (ny).

## M8. Bibliografien: tre verifisert, én rettet feil, fire fjernet (6. august 2026)

Kapitlet krever at tall skal kunne føres tilbake til kilde. Referanselisten
holdt ikke samme standard: seks oppføringer trykte klammetekst av typen
`[Tittel]` og `[institusjon]` i selve PDF-en.

**Verifisert mot primærkilde og rettet:**

`fjelltoft2024` → Fjelltoft, Frøseth og Nordvik (2024), «Bostøttens rolle i den
boligsosiale politikken: Er det behov for å bruke store bokstaver?»,
*Tidsskrift for boligforskning* 7(2), 144–148, doi 10.18261/tfb.7.2.4.

`astrup2024` → Astrup og Pedersen (2024), «Bostøttens egenandelsberegning —
forankring i underliggende prinsipper», BOVEL-notat 2/24, OsloMet,
hdl 11250/3114070. Pedersen var medforfatter, ikke oppført.

`ekspertgruppe2022` hadde **feil tittel**. Jeg hadde skrevet «Gjennomgang av
bostøtteordningen»; rapporten heter «Bostøtten — opprydning og forankring»,
avgitt 9. mai 2022. Dette er den alvorligste av rettelsene: en oppføring som
*ser* komplett ut, men peker på noe som ikke finnes, er verre enn en synlig
plassholder. Den siste ber om å bli sjekket.

**Lagt til, begge verifisert:** `astrup2024b` (svaret på Fjelltoft m.fl., samme
utgave, 149–151) og `sorvoll2018` (Sørvolls forskningsgjennomgang 2005–2018,
*Tidsskrift for boligforskning* 1(1), 45–66). Den faglige uenigheten om
bostøttens rolle er dermed dokumentert som en utveksling, ikke som én påstand.

**Fjernet fordi de ikke lot seg verifisere:** `nordvik2005`, `nordvik2014`,
`menon2020`, `pedersen2023`. Søk i Crossref, DOAJ, institusjonsarkiv og åpne
kilder ga ingen treff som svarte til oppføringene. Det finnes en Menon-utredning
om bostøtten, men verken tittel, nummer eller årstall lot seg fastslå, og en
oppføring med riktig byrå og gale detaljer er ikke bedre enn ingen. En referanse
jeg ikke kan verifisere, er en referanse jeg ikke kan bruke. Setningene de sto i
er omskrevet slik at de nå hviler på de verifiserte kildene — og påstanden om
forlenget mottaksvarighet, som bare `nordvik2005` bar, er tatt ut framfor å bli
stående uten belegg.

**Hva som gjenstår:** 30 av 81 oppføringer er fortsatt merket
`note = {PLASSHOLDER}`. Forfatter, tittel og år er kontrollert; utgiver, URL og
sidetall er ikke slått opp mot primærkilde. Ingen av dem trykker synlig
plassholdertekst, og `verifiser.R` kontrollerer det ved hver kjøring — men
rapporten er ikke kildeferdig før de 30 er gjennomgått.

**Filer endret:** `referanser.bib`, `bostotte_oslo.qmd` (tre avsnitt omskrevet),
`verifiser.R` (bibliografikontroll), `README.md`.

## M9. Repoet strukturert for en leser (6. august 2026)

Repoet var ordnet etter hvordan det ble til, ikke etter hvordan det leses. Det er
nå snudd. En fagfelle som åpner `github.com/Torcode/bostotte-oslo` skal på under
et minutt kunne svare på fire spørsmål: hva er dette, hva ble resultatet, kan
jeg stole på tallene, og kan jeg bygge det selv.

**Datamappa heter `data/`, ikke `velferdsetaten-data/`.** Prosjektet er et eget
initiativ; ingen har bedt om det. En mappe oppkalt etter etaten leses lett som at
arbeidet er gjort på oppdrag, og motsier uavhengighetserklæringen i README-en to
skjermlengder over. Samtidig er `data/` det en leser forventer. Den nøstede
`data/data/raw/` er flatet ut til `data/raw/`. R-lasteren heter nå
`data/scripts/last_datapakke.R`. Trettién henvisninger i fem filer er oppdatert;
eldre loggposter viser fortsatt til `velferdsetaten-data/`, og det er samme mappe.

**Endringsloggene ligger i `logg/`.** De er prosessdokumentasjon, ikke leveransen,
og to filer med lange navn i rota konkurrerte med README-en om oppmerksomheten.

**README-en åpner nå med lenka til rapporten.** Under tittelen står ett kall til
handling — `Les rapporten (PDF, 36 sider)` — og en linje med de fire neste
klikkene: kilden, datagrunnlaget, kodeboka, loggen. Filoversikten er delt i fire
grupper etter hva leseren er ute etter, og hver rad er en lenke. Det var før én
udifferensiert tabell.

**CI hentet fra PR #12, resten ikke.** Grenen `docs/phase-1-contract` inneholdt
fjorten filer. To er tatt inn: `scripts/validate_phase1.py` og
`.github/workflows/ci.yml`. Validatoren kjører 47 datakontrakter i ren Python —
bydelstallene summerer til Oslo, brukergruppene summerer til Oslo, termin- og
utbetalingskalenderen henger sammen over 198 par, sanntidskanten er identifisert
— og trenger ikke R. Det betyr at en leser kan se at datagrunnlaget holder uten
å installere noe, og at et grønt merke i README-en er dekket av noe reelt.

To endringer var nødvendige: den lette etter `unt_1.qmd`, og den krevde seks
prosessdokumenter fra samme gren. Fillisten peker nå på det en leser faktisk
trenger for å etterprøve arbeidet — kodebok, datakilder, endringslogger,
byggekontrollene — framfor på et bestemt prosessrammeverk. Resultat: **47
bestått, 0 feil, 2 advarsler.** Begge advarslene er ekte og står allerede i
README-ens begrensningsliste: to intervensjoner er delvis kildeverifisert, og 30
bibliografioppføringer har uverifiserte metadata.

PR-ens egen `README.md` er ikke tatt inn. Den beskriver prosjektet som at det
«ennå ikke har publisert validerte prognoseresultater». Det var riktig 5. august
og er feil nå. `AGENTS.md`, `CLAUDE.md` og de seks `docs/`-filene står ubesluttet:
de er 1400 linjer prosessdokumentasjon rundt en leveranse på 36 sider, og de
opplyser enhver leser om at repoet drives av agenter. Om det skal vises fram er
en redaksjonell avgjørelse, ikke en teknisk.

**Kontrollene ligger nå i to lag med hvert sitt formål**, og det er verdt å skille
dem: de ni regnskapsidentitetene stopper *renderingen*, slik at rapporten ikke
kan trykke et tall som ikke stemmer; de 47 datakontraktene stopper *pushen*, slik
at ingen kan endre datagrunnlaget uten at det oppdages. `verifiser.R` er et tredje
lag som fanger tegnsettfeller. Ingen av dem erstatter de andre.

**Filer endret:** `velferdsetaten-data/` → `data/` (med flating av `data/data/`),
`velferdsetaten_data.R` → `last_datapakke.R`, `endringslogg-*.md` → `logg/`,
`README.md`, `bostotte_oslo.qmd`, `oppsett.R`, `.gitignore`,
`scripts/validate_phase1.py` (ny), `.github/workflows/ci.yml` (ny).

## M10. M7 gjorde ingenting — en maskert variabel, og kontrollen som manglet (6. august 2026)

Modell M7 skal legge et pålagt bidrag til M6 der høstpakken ikke var estimerbar ved
opprinnelsen. Den gjorde det aldri. Koden var:

```r
mu = mu + if ("pakke_2024h2" %in% ute) LAMBDA_ORAKEL * pakke_2024h2 else 0
```

Inne i `mutate()` treffer `ute` **datarammens kolonne**, ikke funksjonsvariabelen lenger
opp. Kolonnen ble laget som `paste(ute, collapse = ",")`, altså én kommaseparert streng.
`%in%` er eksakt matching, og strengen var alltid `""`, `"k_post"` eller
`"pakke_2024h2,k_post"` — aldri `"pakke_2024h2"` alene. Testen var usann ved samtlige 31
opprinnelser, `LAMBDA_ORAKEL` ble beregnet og aldri brukt, og **M7 var identisk med M6 i
alle 372 punktene.**

Fire linjer lenger ned sto den riktige testen på samme objekt: `str_detect(ute,
"pakke_2024h2")`. Rettelsen er å bruke den, vektorisert, framfor `if`.

**Hva som ble artefakter, og hva de faktisk er.** Tabell 22 viste 0,0 % på alle tre målene.
De reelle tallene, på de 138 rammede punktene:

| Mål | M6 | M7 | Endring |
|---|---|---|---|
| MASE | 1,106 | 0,758 | −31,5 % |
| Dekning ved 80 % | 40 % | 56 % | +16 p.p. |
| Intervallskår | 8 975 | 5 141 | −42,7 % |

Merk hva MASE-tallet betyr: M6 ligger *over* 1 i dette vinduet, altså dårligere enn en
sesongnaiv referanse, mens M7 ligger under. Et datert anslag flytter altså modellen fra
tapende til vinnende der regelendringen ellers er usynlig. Det er svaret på underspørsmål
UB, og det manglet i forrige versjon.

**En påstand som viste seg å ha rett av feil grunn.** Teksten sa at et anslag er verdt
«opptil en tredjedel av prognosefeilen». Den sto som hardkodet prosa ved siden av en tabell
som viste 0,0 %, og var derfor riktig å flagge som selvmotsigelse. Etter rettelsen er
−31,5 % omtrent en tredjedel — påstanden stemte, men hadde ikke belegg i det som faktisk
ble kjørt. Setningen er nå erstattet med et inline-beregnet uttrykk som oppgir MASE før og
etter, slik at prosa og tabell ikke kan gli fra hverandre igjen.

**Kontrollen som manglet.** Avsnitt 3.10 lover at feil skal stoppe byggingen framfor å
passere stille. Ni regnskapsidentiteter kjørte, og ingen av dem så på om en modell faktisk
oppførte seg som spesifisert. To `stopifnot` er lagt inn: M7 må avvike fra M6 et sted, og
M7 må være identisk med M6 der pakken var estimerbar. Den andre er like viktig som den
første — den fanger den motsatte feilen, at bidraget påføres overalt.

Det generelle poenget er verdt å skrive ned: *en modell som per konstruksjon skal avvike
fra sin referanse, og ikke gjør det, er en byggefeil — ikke et resultat.* Kvalitetsapparatet
kontrollerte dataene, ikke modellene.

**Filer endret:** `bostotte_oslo.qmd` (M7-konstruksjonen, to nye kontroller, avsnitt 4.6).


## M11. Formateringen strippet sju merkelapper og escapet en inline-chunk (7. august 2026)

En automatisk formatering — RStudio eller Positrons «Reformat Document», eller en
formatter som kjører ved lagring — hadde skrevet om tabellene i `bostotte_oslo.qmd`.
Det meste var kosmetisk: skillelinjene i tabellhodene komprimert fra padding til
`|---|`, og kulepunkter fra `*   ` til `- `. Begge rendrer likt.

Fire ting var ikke kosmetiske.

**Sju `{#tbl-...}`-merkelapper var fjernet.** `tbl-former`, `tbl-intervensjoner`,
`tbl-kildekart`, `tbl-modeller`, `tbl-res-oppgjor`, `tbl-tester` og `tbl-vask`.
Uten merkelappen får tabellen ikke nummer, og hver `@tbl-...` i teksten rendrer som
en ubesvart referanse. Omfanget var **15 kryssreferanser**, deriblant de fire til
`@tbl-tester` — forhåndsregistreringen som hele kapittel 4 måles mot.

**En inline R-chunk var escapet.** I avsnittet om ekvivalenstesten var

    $p = `r nb(kq$p.value, 3)`$

blitt til `` `r nb(kq$p.value, 3)\`\$ ``. Backticken og dollartegnet var escapet, så
chunken ville ikke kjørt. PDF-en hadde trykt kildekoden i stedet for p-verdien, midt i
argumentet om hvorfor T3 er formulert som ekvivalenstest.

**To uthevinger rundt inline matematikk var brutt.** `*$\theta$ og $E$ er ikke separat
identifisert.*` mistet kursiven mens punkt 2–4 i samme liste beholdt sin, og
`**Hvor $\lambda_j$ kommer fra.**` var blitt `**Hvor** $\lambda_j$ kommer fra.`
Begge er mønsteret til en formatter som ikke håndterer utheving over `$`.

**Rettelse og kontroll.** Merkelappene ble hentet tilbake fra forrige commit ved å
koble bildetekst til etikett, uthevingene og chunken ble gjenopprettet ordrett, og de
kosmetiske endringene ble beholdt. PDF-en er bygget på nytt: 38 sider, 24 tabeller
nummerert 1–24 sammenhengende, null ubesvarte referanser, og T3 trykker `p = 0,933`.

**Det generelle poenget.** `verifiser.R` parser dokumentet i rent C-tegnsett og
kontrollerer referanselisten, men den kontrollerer ikke at kryssreferansene løser seg.
Skaden var derfor usynlig helt til PDF-en ble lest. En kontroll på at hver `@tbl-`,
`@fig-` og `@sec-`-referanse har en merkelapp, og at kilden ikke inneholder escapet
backtick eller dollartegn, fanger hele klassen på et sekund. Den mangler fortsatt.

Én referanse var brutt fra før og er ikke rørt: `@sec-met-m7` peker på en seksjon som
heter `{#sec-met-prior}`.

**Filer endret:** `bostotte_oslo.qmd` (sju merkelapper, én inline-chunk, to uthevinger),
`bostotte_oslo.pdf` (rebygget).

## M12. Arbeidsverk 2 påbegynt: notebook 01 (7. august 2026)

`notebooks/bostotte_01_grunnlag.ipynb` er lagt til. Den estimerer ingen modell — den
fester datagrunnlaget til commit `9b3da3e` med SHA-256 per fil, går gjennom variablene
og hva de tåler, viser fordelingen bak aggregatene, og regner ut hvor mye informasjon
panelet inneholder. Rekkefølgen er tilsiktet: panelets størrelse avgjør hvilke
modellklasser som er forsvarlige, så det tallet må ligge på bordet før valget tas.

Notebooken er committet med utdata, av samme grunn som PDF-en versjoneres: en leser
skal se resultatet uten å installere noe. Den er kjørt i to miljøer med ulike
hovedversjoner av pandas — Colab (3.12.13 / pandas 2.2.2) og en Linux-container
(3.11.15 / pandas 3.0.2) — med identiske tall.

**Fire funn.**

*Panelet er mindre enn nodetallet.* Effektiv dimensjon i rå logvekst er 1,2 av 15
bydeler. Oslo-totalen forklarer median 93 % av hver bydels månedsvekst. En global
modell som får panelet uten videre, tilpasser det samme signalet femten ganger.

*Restleddet er en størrelseseffekt.* Etter at fellesbevegelsen er trukket ut stiger
effektiv dimensjon til 11,3, men restvariasjonen skalerer med bydelsstørrelse:
log(sd) = −0,11 − 0,60·log(n), R² 0,87. Tellegulvet √(2/n) er elleve ganger for stort,
fordi serien er en beholdning der bare strømmen varierer.

*April 2024 er det skarpeste fordelingseksempelet i materialet.* Antall falt 25,2 %,
mens snittinntekt beveget seg −0,2 %, boutgift +0,7 %, bostøtte +0,2 % og antall over
tak +1,3 %. Fordelt på brukergruppe: unge uføre −58,2 %, uføre forøvrig −40,7 %,
midlertidige ytelser −30,3 %, eldre −15,1 %, uten trygdeytelser −7,9 %. Fire snitt står
stille mens sammensetningen bygges om. Et snitt over en gruppe hvis grense settes av
regelverket, beskriver grensen mer enn menneskene innenfor.

*Støygulvet endret en påstand.* Målt mot gruppens eget standardavvik i rolige måneder
er aprilutslaget 1,5 til 10,4 ganger. Husstander uten trygdeytelser ligger på 1,5 og
lar seg ikke skille fra normal variasjon. Figuren kan altså ikke avgjøre at avviklingen
traff den gruppen svakt, bare at den ikke kan avgjøre det.

**Krysstabellen finnes.** Husbankens Qlik-app gir bydel × brukergruppe: 75 bunnceller,
198 måneder, 14 879 observasjoner, full dekning i alle 75, og null avvik mot Oslo,
bydelsmarginalen og brukergruppemarginalen. API-et prikker ikke — 26 celler har verdien
1. Den er kontrollert, ikke tatt i bruk: uttrekket er datert 7. august mot datapakkens
4. august, og to uttrekksdatoer i samme evaluering bryter dateringsdisiplinen.

**README rettet i samme runde.** Fasetabellen hadde overskriftsrad med én celle mot
skillelinje med tre og rendret som ren tekst på forsiden. «Uforanderlig datauttrekk» er
byttet mot sjekksum-mekanismen, siden ingenting håndhevet lovnaden. `notebooks/` er lagt
inn i filoversikten, og SSB 03013 er merket som avsluttet.

**Filer endret:** `notebooks/bostotte_01_grunnlag.ipynb` (ny), `README.md`.

## M13. Tre funn fra arbeidsverk 2 som gjelder del 1 (7. august 2026)

**`osloandel` regnes på hele serien.** Konstruksjonen i oppsett-chunken er
`tail(12)` av det ferdige utvalget. Ved en prognoseopprinnelse i 2021 ville den brukt
2025–26-data. Andelen er ingen konstant: den steg fra 14,4 % i 2010 til 19,9 % i 2021 og
falt til 18,5 % i 2024. M7 skalerer nasjonale forhåndsanslag ned til Oslo med denne.
Størrelsen brukes i dag bare i løpende tekst og ikke i kryssvalideringen, så tallene i
kapittel 4 er ikke berørt — men metoden slik den er beskrevet, lekker. Andelen bør måles
ved hver opprinnelse, av samme grunn som ordensvalget gjentas der.

Nedgangen har en forklaring som selv er et funn. Nasjonalt vokste gruppen med
midlertidige trygdeytelser 72 % fra mars 2021 til mars 2024, mot 44 % i Oslo. SØF-rapport
05/2025 oppgir at ukrainske husstander gikk fra 0,1–0,2 % av mottakerne i 2020–21 til
13,5 % i 2024, og bosettingen skjedde i hovedsak utenfor Oslo. Den største
sammensetningsendringen i perioden er usynlig i variablene datagrunnlaget har.

**Et publisert tall for avviklingen finnes likevel.** M4 konkluderte med at ingen av fire
gjennomsøkte kildefamilier oppgir husstandstall for hendelsene. Det gjaldt høstpakken.
For avviklingen oppgir SØF 05/2025 rundt 25 000 husstander nasjonalt. Tallet er
*etterberegnet*, ikke et forhåndsanslag, og hører derfor inn i `forhandsanslag.csv` med
den merkingen — det kan validere metoden i M7, aldri brukes i en prognose.

SØF daterer hendelsen til mai 2024, dette arbeidet til termin april 2024. Begge er
riktige: termin april utbetales 20. mai. Kalenderidentiteten i avsnitt 3.1 er altså ikke
en pedantisk kontroll — forvekslingen står i en publisert fagrapport.

**Litteraturhullet er dokumentert.** Gjennomgang av Husbanken, NIBR/OsloMet, SSB,
Fafo/NOVA, SØF, ekspertgruppen, Oslo Economics, Vista, SØA og Oslo kommune: det finnes
ingen publisert framskriving av bostøttemottak, verken nasjonalt, for Oslo eller per
bydel. Ingen bruker maskinlæring på feltet. Ingen har gjort kausal intervensjonsanalyse
av 2021-vinduet, avviklingen, høstpakken eller skjermingen. Take-up er sist målt på
2016-data (SSB Rapporter 2019/02: 50–61 %, Oslo høyest blant storbyene), og det finnes
ingen mikrosimuleringsmodell for regelverket i Norge.

De to rapportene i `litteratur/` er de to halvdelene av samme hull. Husbanken 5/2025 har
null forekomster av prognose, framskriving, maskinlæring eller prediksjon i 42 sider.
Velferdsetatens boligbehovskartlegging 2024 teller 3 826 husstander, 1 109 med rus eller
ROP — og nevner ikke ordet bostøtte.

**En datakilde er avsluttet.** SSB 03013, KPI for betalt husleie, stoppet 2025M12.
Repoet bruker den i kildekartet, README, `last_datapakke.R` og `fetch_ssb.py`.
Etterfølgeren er 14700. En pipeline som kjører månedlig, vil stille produsere en
husleieindeks som ikke oppdateres.

**Filer endret:** ingen. Postene står som funn å håndtere i neste patch.

---

## M14. To kalendre i samme rad — en konklusjon som var snudd (7. august 2026)

Avsnitt 4 i notebook 01 sammenliknet termin mars og april 2024 ved å hente alle
kolonnene fra samme rad. Det ga at snittene knapt beveget seg i bruddmåneden, og derav
at frafallet var jevnt fordelt over inntektsskalaen. Begge deler var feil, og
konklusjonen var motsatt av den riktige.

**Hva som er galt med å lese raden.** `ant_husstander_termin` daterer rettighetsmåneden.
Snitt- og beløpskolonnene daterer utbetalingsmåneden, den 20. i måneden etter. Raden for
april 2024 inneholder derfor snittene for termin mars. Sammenlikningen mars-mot-april
sammenliknet i realiteten februar-mot-mars for snittenes del, altså to måneder som begge
ligger før regelendringen. At de ikke rørte seg var derfor ikke et funn, men en følge av
at bruddet ikke var med i vinduet.

| Størrelse, termin mars → april 2024 | Feil lesning | Riktig |
|---|---|---|
| Antall mottakere | −25,2 % | −25,2 % |
| Snittinntekt | −0,2 % | **−16,1 %** |
| Gjennomsnittlig bostøtte | +0,2 % | **+5,8 %** |
| Antall over boutgiftstak | +1,3 % | **−25,4 %** |
| Gjennomsnittlig boutgift | +0,7 % | +0,9 % |

**Hvordan den ble funnet.** Ekstern gjennomlesning pekte på uoverensstemmelsen. Den ble
så prøvd mot tre uavhengige forhold før den ble godtatt: kodebokens ordlyd for
`utbetalt_belop` og `ant_over_tak`, hvilken måned hver serie faktisk brekker i, og
identiteten mellom de to antallskolonnene. Alle tre pekte samme vei. Feilen nådde aldri
en commit.

**Hva som er lagt inn i stedet for en merknad.** Tre kontroller som kjører hver gang:

1. `termin(m) = utbetaling(m+1)` rad for rad. 197 par, 0 avvik. Filranden bekrefter
   den strukturelt: første rad har utbetalingskolonnene på null, fordi utbetalingen som
   hører hjemme der gjelder en termin fra før uttrekket.
2. `utbetalt_belop = ant_husstander_utbetaling × gjsnitt_bostotte`. Maksimalt relativt
   avvik 1,6 · 10⁻⁶ mot utbetalingskalenderen, 25 % mot terminkalenderen. Det plasserer
   både beløpet og snittet, uten skjønn.
3. Bruddtesten: for hver kolonne, hvilken av april og mai bærer det største
   log-utslaget, og er forspranget minst tre ganger? Avgjør fem av seks, alle i favør av
   klassifiseringen. `gjsnitt_boutgift_mnd` står som uavgjort — 0,7 mot 0,9 prosent
   skiller ingenting — framfor å bli talt som bekreftet.

Alle tre er `assert`. Tilgangen går nå gjennom `paa_termin(kolonne, terminmåned)`, som
velger måned etter kolonnens kalender, slik at samme forveksling ikke kan gjøres på nytt
uten at kjøringen stopper.

**Hva den riktige lesningen viser.** Frafallet var sterkt selektert på inntekt.
Gruppene rangert etter tap står samtidig rangert etter inntektsnivå før bruddet, uten
et eneste bytte: unge uføre 28 352 kr og −58,2 %, husstander uten trygdeytelser 8 176 kr
og −7,9 %. Med fem grupper kan hele nullfordelingen telles ut — 120 tilordninger, hvorav
2 gir en rangering uten bytter og 4 gir |r| ≥ 0,88. Sannsynlighetene 2/120 og 4/120 er
eksakte, ikke tilnærminger.

Det stemmer med regelverket. Intervensjon I05 senket det progressive egenandelsleddet
fra 0,28 % til 0,12 % i termin desember 2021 og løftet dermed den implisitte
inntektsgrensen; da leddet ble ført tilbake i termin april 2024, var det husstandene
nærmest grensen som mistet retten. Forbeholdet er notert i teksten: aggregater
identifiserer ikke hvem som falt ut, og fem punkter kan ikke skille inntekt fra noe
annet som følger gruppeinndelingen.

**Det generelle.** Feilen var ikke en regnefeil, men en lesefeil i en tabell der to
tidsakser deler rad. Den er usynlig i koden, gir tall som ser rimelige ut, og ville
forplantet seg til enhver senere sammenlikning av nivå mot snitt. Motmiddelet er at
tilgangen går gjennom en funksjon som kjenner kalenderen, ikke at leseren husker den.

**Filer endret:** `notebooks/bostotte_01_grunnlag.ipynb` (avsnitt 4 skrevet om, avsnitt
9 utvidet med feilen, kjøremanifestet utvidet med de tre kalenderkontrollene).

---

## M15. Protokollen flyttet til Python, og en lekkasje målt (7. august 2026)

Arbeidsverk 2 skal måle maskinlæringsmodeller mot modellstigen i arbeidsverk 1. Det
forutsetter at de måles med samme linjal. Notebook 02 bygger evalueringsprotokollen i
Python og kontrollerer flyttingen der den lar seg kontrollere.

**Hva som er kontrollert, og hvordan.** To av de åtte trinnene i stigen har lukket
form og krever ingen ordensseleksjon: M0 (naiv) og M1 (sesongnaiv). De er
implementert fra bunnen i Python, og de ti tallene arbeidsverk 1 oppgir for dem i
tabell 17 reproduseres alle, med den presisjonen de er oppgitt med.

| | MASE | RMSE | Dekning 80 | Dekning 95 | Intervallskår |
|---|---|---|---|---|---|
| M0, arbeidsverk 1 | 1,003 | 1 698 | 91 % | 98 % | 7 082 |
| M0, notebook 02 | 1,003 | 1 698 | 91 % | 98 % | 7 082 |
| M1, arbeidsverk 1 | 1,228 | 1 844 | 77 % | 97 % | 6 125 |
| M1, notebook 02 | 1,228 | 1 844 | 77 % | 97 % | 6 125 |

I tillegg reproduseres fasekalibreringen av kalenderregressoren: samme vinnerfase, og
samme tre øverste rader som tabell 12 (−16,1 / −10,3; −12,7 / −6,8; −10,0 / −3,8).
Seksten tall i alt, null avvik, holdt av `assert`.

Det som dermed er kontrollert er hele skåringsapparatet — hvilke opprinnelser som
inngår, hvilke horisonter, at MASE-nevneren regnes per opprinnelse på nivåskala i
treningsvinduet, at log tilbaketransformeres ved ren eksponensiering, hvordan
intervaller bygges, hvordan dekning telles og hvordan intervallskåren straffer.

**En konvensjon som ikke sto skrevet.** Intervallmålene traff først når
residualvariansen regnes uten frihetsgradskorreksjon, altså som rent gjennomsnitt av
kvadrerte residualer. Med `n − 1` blir intervallskåren 7 107 for M0 og 6 121 for M1.
Konvensjonen er dermed ikke antatt, men avlest av hvilken av dem som treffer, og
alternativet står i notebooken.

**Kontroller som er bygget inn framfor påstått.** Tre av dem er identiteter som må
holde, og som stopper kjøringen hvis de ikke gjør det:

1. M0 og M1 er **samme prognose ved h = 12**. Den sesongnaive henter fra
   $t_0 + 12 - 12 = t_0$, som er nøyaktig der den naive henter sin. `assert` på at
   tallene viser det.
2. DM-statistikken er derfor **udefinert ved h = 12** — tapsdifferansen er identisk
   null. `assert` på NaN. En implementasjon som fant signal der, ville funnet signal
   i null.
3. V1 slik arbeidsverk 1 definerer det, mot notebook 01s bredere nullfiltrering.
   `assert` på at de faller sammen for Oslo-totalen.

**En forskjell mellom notebookene, notert.** Arbeidsverk 1s V1 fjerner siste rad
*bare hvis* den er null — en strukturell null, fordi terminkjøringen skjer måneden
etter. Notebook 01 filtrerte på `ant_husstander_termin > 0`, som er det bredere
inngrepet. For Oslo-totalen sammenfaller de, og `assert`-en holder det fast. For
bydelspanelet gjør de det ikke, og det må rettes før panelet brukes.

**Nytt funn: den konformale kalibreringen bruker feil som ikke fantes.** Arbeidsverk
1 kalibrerer på $|e_h|$ fra alle opprinnelser med $t_j < t_i$. Men en prognosefeil er
kjent først når målmåneden er observert, altså i $t_j + h$. Kravet skulle vært

$$t_j + h \le t_i.$$

For $h = 1$ er de to kravene like. For $h = 12$ bruker kalibreringen feil som først
blir kjent opptil elleve måneder etter at intervallet skulle vært stilt.

Målt på M0, på de 270 punktene begge skjemaene skårer:

| | Dekning ved nominelt 80 % | Kalibreringspunkter |
|---|---|---|
| Arbeidsverk 1s skjema | 78,5 % | 30 ved enhver horisont |
| Bare realiserte feil | 67,4 % | 30 ved h = 1, 19 ved h = 12 |

Retningen er entydig punkt for punkt: 32 punkter dekkes bare av det lekkende
skjemaet, 2 bare av det tidsgyldige. **Kontrollen på diagnosen** er at de to
skjemaene er identiske ved h = 1, der kravene sammenfaller — det er en `assert`, ikke
en observasjon. Hadde de skilt lag der, ville forskjellen skyldtes noe annet.

Lekkasjen lar seg ikke korrigere bort med en faktor. Medianen av forholdet
$q_A/q_B$ er 1,00, og det tidsgyldige skjemaet gir den største kvantilen i 135 av 270
punkter; snittet av forholdet er likevel 1,28, med 5,8 som største verdi. Lekkasjen
virker altså som en kraftig utvidelse av noen få intervaller — de der framtiden som
lekker inn, inneholder et brudd — ikke som en jevn utvidelse av alle.

Alt dette er regnet på M0. Lekkasjen er en egenskap ved skjemaet, ikke ved modellen,
så mekanismen gjelder alle åtte trinnene; utslaget per trinn er ikke målt.

**Hva som bevisst ikke er flyttet.** ETS, SARIMA og de tre RegARIMA-variantene er
ikke reimplementert. `fable` velger $(p,d,q)(P,D,Q)_{12}$ ved stegvis AICc-søk med
differensiering fra KPSS og et sesongstyrkemål, og gjentar valget ved hver av de 31
opprinnelsene. Python har ingen implementasjon som er dokumentert å gjøre det samme
søket med de samme grensene, så en «M3» her ville vært en annen modell med samme
navn. Referansetabellen i notebooken har derfor en kildekolonne: to rader står som
«kontrollert her», seks som «arbeidsverk 1».

Det generelle poenget: *en protokoll kan flyttes mellom språk og kontrolleres
tallmessig; en tilpasningsalgoritme kan det som regel ikke.*

**Konsekvens for arbeidsverk 1.** Rapporten oppgir at konformal kalibrering løfter
dekningen for hovedspesifikasjonen fra 45 til 73 prosent. Det tallet er beregnet med
det lekkende skjemaet og skal ikke stå uten forbehold. Rettelsen krever render.

**Filer endret:** `notebooks/bostotte_02_protokoll.ipynb` (ny).

---

## M16. Første maskinlæringsmodell: hele fordelen er regelverket (7. august 2026)

Notebook 03 kjører gradientboosting mot protokollen fra notebook 02. Notebooken er
bygget rundt en forhåndsregistrering: fire påstander skrevet ned med begrunnelse
**før** noen modell kjøres, og et oppgjør etterpå.

**Protokollen kontrollert på nytt.** Notebook 02 sto igjen med at protokollfunksjonene
bor i en notebook og kan gli fra hverandre. Løsningen her er ikke å love at kopien er
lik, men å måle det: de samme ti tallene fra arbeidsverk 1 reproduseres også i
notebook 03. Kontrollen koster millisekunder og skal gjentas i hver notebook som
skårer noe.

**Lekkasjetest på trekkene.** Hver trekkverdi regnes to ganger — med data som stopper
ved kildemåneden, og med hele serien tilgjengelig — og må være bit for bit lik.
180 verdier, 0 avvik. Pluss en kontroll på at ingen treningsrad har målmåned etter sin
opprinnelse. Testen fanger den vanligste feilen i denne typen arbeid: et rullende
standardavvik eller en sesongindeks regnet på hele serien og deretter skåret til
treningsvinduet.

**Forhåndsregistreringen.**

| | Påstand | Målt | Utfall |
|---|---|---|---|
| P1 | Nivåmodellen kan ikke ekstrapolere | 0 av 372 prognoser utenfor treningsområdet | holdt |
| P2 | Vekstparametrisering fjerner taket | 44 av 372 utenfor | holdt |
| P3 | Residual-ML slår ikke modellen alene | N1 1,066 mot G1 0,905 | holdt |
| P4 | Kryssæring over bydelene gir lite | G2 0,815 mot G1 0,905, DM 3,51 ved h = 6 | **falt** |

**P1 er demonstrert, ikke påstått.** Gradientboosting på nivå forlot aldri intervallet
mellom høyeste og laveste treningsmål — null av 372. På de 56 punktene der utfallet
ligger over treningens tak, er modellens MASE 1,83 mot 0,74 for den naive: å ikke
gjøre noe er der to og en halv gang bedre. Innenfor treningsområdet er forholdet
snudd, 0,90 mot 1,05. Grensen er ikke en svakhet ved algoritmen, men ved
parametriseringen: samme modell, samme trekk, samme data, bare et annet mål, og taket
forsvinner.

**Hvorfor P4 falt.** Begrunnelsen var riktig målt og feil brukt. Effektiv dimensjon
1,2 (notebook 01) sier at bydelene ikke bærer femten uavhengige signaler om Oslos
framtid. Det stemmer. Men en trebasert modell trent på 60 rader lider av for få
*eksempler*, ikke av for lite informasjon. Femten bydeler som gjentar den samme
sammenhengen, gir femten ganger så mange observasjoner av den og reduserer variansen
i det modellen lærer. Kryssæringen virker som regularisering, ikke som ny informasjon.
Skillet er testbart: gevinsten skal forsvinne hvis Oslo alene får nok data, og skal
ikke vokse av flere kollineære serier. Ingen av delene er prøvd.

**Hovedfunnet: ablasjonen.** G2 — gradientboosting på vekst, trent globalt på
bydelspanelet — har lavest MASE av alt i materialet, 0,815, også lavere enn M7, som
får pålagt en koeffisient estimert på hele utvalget.

| Variant | MASE med regelverk | MASE uten | Naiv referanse |
|---|---|---|---|
| Lokal (G1) | 0,905 | 1,188 | 1,003 |
| Global (G2) | 0,815 | 1,249 | 1,003 |

Uten de fem regelverksregressorene taper begge mot å ikke gjøre noe. Variabelviktighet
gir samme svar fra en annen kant: regressorene står for 55 % av samlet gain, med
`win_strom`, `win_covid` og `k_pre` øverst. **Hele fordelen over referansen er
domenekunnskap.** Modellklassen avgjør hvor fleksibelt informasjonen brukes, og det er
en reell forskjell, men den er annenordens.

Kryssæringen snur også fortegn: med regelverket hjelper panelet (0,905 → 0,815), uten
det skader det (1,188 → 1,249). Det bydelene har til felles er hvordan regelendringer
slår gjennom; uten regressorene som daterer endringene, er de øvrige seriene mest støy
fra andre bydelers særtrekk.

**Forbeholdene, som står i notebooken.** Ingen av de trebaserte modellene skiller seg
fra den naive med en DM-statistikk over 1,64 på noen horisont — forbedringen fra 1,003
til 0,815 er målt på 372 punkter, men er ikke større enn 31 opprinnelser kan skille
fra tilfeldighet. Den eneste sammenlikningen som passerer, er G1 mot G2. RMSE rangerer
dessuten M7 (1 322) og M5 (1 391) foran G2 (1 408): G2 er bedre på den typiske feilen
og dårligere på halen, og hvilken av dem som betyr noe, avhenger av bruken. Videre:
ingen hyperparametersøk, ingen intervaller fra modellene, ett frø, og seks av åtte
trinn i stigen er avskrift fra arbeidsverk 1.

**Filer endret:** `notebooks/bostotte_03_trekk_og_trebasert.ipynb` (ny).

---

## M17. Kapasitet: den beste modellen i arbeidet er lineær (7. august 2026)

Notebook 04 kjører nevrale nett mot samme protokoll og tester forklaringen notebook 03
lot stå åpen: at panelgevinsten er varians framfor informasjon.

**En feil som måtte rettes først, og som er den verste hittil.** Første kjøring brukte
`MLPRegressor` fra scikit-learn med standardiserte trekk og utransformert mål.
Kapasitetsstigen kom ut bakvendt: de smaleste nettene var klart verst, og bare det
bredeste var brukbart. Det så ut som et funn.

Det var det ikke. `MLPRegressor` stopper når tapet forbedres med mindre enn `tol`,
som standard 10⁻⁴. Målet er logvekst med standardavvik rundt 0,09, så tapet starter
rundt 10⁻³. Kriteriet slo inn etter 24–54 av 1 500 tillatte iterasjoner, og nettene
ble aldri trent. Med standardisert mål kjørte de samme nettene 68–292 iterasjoner og
nådde treningstilpasning 0,89–0,98.

Målestokken var altså ikke kapasitet, men hvor fort hvert nett ga opp.

Tiltaket er ikke en merknad. Alt er skrevet om til **PyTorch med fast antall epoker og
full batch**, slik at det ikke finnes noe stoppkriterium som kan slå inn uten at det
står i koden, og **treningstilpasningen rapporteres ved siden av prognosefeilen**, slik
at et utrent nett er synlig.

Dette er en tredje sort feil ved siden av kalenderforvekslingen (M14) og
konformallekkasjen (M15). Den er verre enn begge: et undertrent nett gir hverken
feilmelding eller urimelige tall, og ville passert enhver kontroll som bare ser på om
resultatet er plausibelt.

**Kapasitetsstigen**, alle trent likt på hele panelet:

| Modell | Parametre | R² trening | MASE | RMSE |
|---|---|---|---|---|
| L0, ett lineært lag | 19 | 0,650 | **0,767** | **1 308** |
| N8 | 161 | 0,872 | 0,898 | 1 584 |
| N32 | 1 697 | 0,963 | 0,964 | 1 647 |
| N128 | 19 073 | 0,989 | 0,939 | 1 596 |

Jo bedre treningen sitter, jo dårligere treffer prognosen. N128 har flere parametre
enn treningssettet har rader og forklarer nesten alt den har sett; nettopp derfor
bærer den støy inn i prognosen. Overtilpasning målt, ikke antatt.

**0,767 er laveste MASE i hele arbeidet** — lavere enn gradientboosting (0,815), enn
M5 (0,867) og enn M7 (0,838), som får pålagt en koeffisient estimert på hele utvalget.
Også på RMSE ligger den først, der G2 tapte mot M7. Den beste modellen i prosjektet er
altså en regresjon med atten forklaringsvariabler, tilpasset på et panel. Det er
Zeng m.fl. (AAAI 2023) reprodusert på disse dataene.

**Læringskurven, og en forhåndsregistrering som falt.**

| Serier | Rader | MASE L0 | R² L0 | MASE N32 | R² N32 |
|---|---|---|---|---|---|
| 1 | 84 | 1,454 | 0,843 | 1,167 | 1,000 |
| 2 | 168 | 1,023 | 0,718 | 1,368 | 1,000 |
| 4 | 336 | 0,896 | 0,694 | 1,182 | 0,998 |
| 8 | 672 | 0,737 | 0,678 | 0,999 | 0,989 |
| 16 | 1 344 | 0,767 | 0,650 | 0,964 | 0,963 |

Jeg registrerte at gevinsten skulle være størst for modellen med mest kapasitet, siden
varians var forklaringen. Det motsatte skjedde: den lineære modellen forbedret seg
0,687 fra én til seksten serier, nettet 0,203.

Treningstilpasningen forklarer hvorfor. **Nettet interpolerer uansett datamengde** —
R² 1,000 ved 84 rader og fortsatt 0,963 ved 1 344 — så mer panel endrer lite for det.
Den lineære modellen går motsatt vei: R² faller fra 0,84 til 0,65, den slutter å kunne
tilpasse seg støyen, og prognosefeilen faller med den. Panelet gjør altså ikke først
og fremst en fleksibel modell mer stabil. Det gjør en **enkel modell identifiserbar**.
Nitten koeffisienter lar seg ikke feste med 84 observasjoner, og lar seg feste med 672.

Det er en presisering av notebook 03, ikke en tilbaketrekking: kryssæring virker
gjennom varians, men sterkest der modellen er enkel nok til at variansreduksjonen
oversettes til treffsikkerhet.

**Ablasjonen, for tredje gang.** Uten regelverksregressorene faller L0 til 1,498 og
N32 til 1,546, mot naiv 1,003. Samme bilde som for gradientboosting, nå med en annen
modellfamilie: **hverken trær eller nett finner noe i denne serien på egen hånd.** Det
som virker, er daterte regelendringer. Modellklassen avgjør hvor godt den kunnskapen
forvaltes, og der er en lineær spesifikasjon best.

**Oppgjør:** Q1 holdt, Q2a holdt, Q2b falt, Q3 holdt, Q4 holdt.

**Statistisk oppløsning.** Ingen forskjell i toppen av den samlede rangeringen er
skillbar fra tilfeldighet med 31 opprinnelser. Det som *er* skilt, er avstanden mellom
kapasitetsnivåene innad i notebooken — L0 slår N128 med DM over 1,64 på tre av fire
horisonter — og avstanden ned til modellene uten regelverk.

**En endring i arbeidsformen.** Forhåndsregistreringene i notebook 03 og 04 er skrevet
før kjøringen, men filene kan ikke bevise rekkefølgen; prosaen er skrevet etter at
tallene forelå. Fra notebook 05 legges forhåndsregistreringen inn i **en egen commit
før kjøringen starter**, slik at git-historikken bærer tidsstempelet. Svakheten er
notert i notebook 04 framfor å bortforklares.

**Filer endret:** `notebooks/bostotte_04_kapasitet.ipynb` (ny).
