# Endringslogg: release-runden august 2026

Én post per endring, med før, etter og begrunnelse. Runden bringer repoet fra
tilstanden etter PR #20/#21 (merge-commit `d503897`) til releasekandidat;
sluttverifiseringen står i `revisjon/02_release_verification.md`.

## R1. M7/T5-kontrakten: modellen heter det den er

**Før.** Metodekapitlet beskrev M7 som «M6 + pålagt effekt» fra «daterte
forhåndsanslag» (`forhandsanslag.csv`); den faktiske kjøringen påla
`LAMBDA_ORAKEL` — full-utvalgskoeffisienten for høstpakken, estimert på data
som inkluderer utfallet. Resultatkapitlet erkjente dette, men modelltabellen,
metodeteksten og lesernavnet «M7 med pålagt bidrag» beskrev fortsatt en
operativt tilgjengelig modell, og metoden lovet en prior-mot-estimat-figur
(T5, «egen figur i kapitlets andre del») som aldri ble levert.

**Etter.** Modellen heter «M7 orakel (øvre grense)» i tabeller, figurer og
tekst; metodeseksjonen (3.7.1) sier eksplisitt at den kvantifiserer verdien av
perfekt informasjon og ikke er en gjennomførbar historisk eller framtidig
prognosemodell. Betegnelsen `M7_prior` er reservert for en modell som mottar
et datert, verifisert forhåndsanslag — ikke implementert, siden kilden mangler
for hendelsen som trengte den (dokumentert søk i `forhandsanslag.csv`).
Figurløftet er fjernet; $\hat\beta$-mot-$\lambda$-sporingen står som presist
definert framtidig arbeid under `M7_prior`. T5-raden i testtabellen beholder
den forhåndsregistrerte ordlyden, med en merket presisering i ettertid om at
ingen av de to leddene lot seg kjøre som registrert; resultat, diskusjon og
konklusjon dømmer T5 konsistent som «ikke testbar som formulert — bare øvre
grense målt». Intern modellkode (`M7`, `LAMBDA_ORAKEL`) er beholdt for å
unngå unødig beregningsrisiko.

**Virkning på tall: ingen.** Beregningen er uendret; alle verdier i
resultattabellene er identiske før og etter (kontrollert mot regenerert PDF:
MASE-stigen 0,890/0,931/0,937/0,960/1,003/1,071/1,131/1,228, PIT-flaggskipet
15 552/15 588, dekning 48 → 79). Hovedkonklusjonen består derfor uendret —
det som er rettet, er hva tallene *heter* og hva de kan brukes til.

## R2. Kanonisk framtidsprognose som én artefakt

**Før.** Ingen publisert framtidsprognose; README lovet «prognosemodell» uten
å levere en prognose.

**Etter.** Nytt kapittel 7 i rapporten. Chunken `prognose-artefakt` produserer
ved rendering tolv månedsprognoser (h = 1–12) fra siste observerte termin
(2026m6) med M6 som operativ, lekkasjefri modell (begrunnelse i kapitlet), og
skriver `prognose/prognose_gjeldende.csv` + `.json` med opprinnelse, vintage,
commit, genereringstidspunkt, modell, punkt, 80/95-grenser, intervallmetode,
antall realiserte kalibreringsfeil per horisont, kalenderkunnskap, scenario og
informasjonsstatus per målmåned. Rapporttabellen, README-utdraget
(`prognose/README_utdrag.md`, limt ordrett inn i README) og den statiske
prognosesiden leser samme artefakt. Kontraktene P01–P13 håndheves i
`scripts/validate_prognose.py` (CI) og speiles som `stopifnot` i chunken.
Intervallene gjenbruker den tidsgyldige konformalkalibreringen med
endelig-utvalgsnivå og deklarerer målt backtest-dekning (79 % ved nominelt
80) framfor garantier.

## R3. Årsstørrelsen har riktig estimand

Hovedmålet for de kommende tolv månedene er *forventet gjennomsnittlig
månedlig antall mottakende husstander* (16 961 i denne kjøringen); en sum
omtales bare som mottakermåneder. Intet aggregert intervall publiseres:
avhengigheten mellom de tolv prognosefeilene gjør at marginale månedsgrenser
ikke kan aggregeres til et intervall med definert dekningsnivå — punktestimat
med eksplisitt merknad i både rapport, README og artefakt.

## R4. Regelverksbetingelsen er dynamisk, ikke horisontmekanisk

**Før.** Diskusjonen anbefalte «én til tre måneder som prognose, seks til tolv
som beregning» — en mekanisk horisontregel.

**Etter.** Status per målmåned bestemmes av informasjonssettet: til og med
2026m12 vedtatt kalender (statsbudsjettet 2026, I20); fra 2027m1 basisbane
under *uttrykkelig* videreført regelverk, siden ingen kalender for 2027 er
vedtatt. Skillet står i tabellen per rad, i figuren (markert linje), i
artefakten (feltet `informasjonsstatus`, håndhevet av P07) og på
prognosesiden. Ikke-vedtatte forslag ville bare inngått som navngitte
scenarioer; orakelkjøringer finnes bare i historiske metodeillustrasjoner.

## R5. Interaktiv 1–12-visning på GitHub Pages

`prognose/index.html`: statisk side uten rammeverk som leser den versjonerte
JSON-artefakten. Skyvebar (`input type="range"`, 1–12, tastatur- og
mobilvennlig), målmåned/punkt/intervaller/modell/opprinnelse/vintage/status
per horisont, fan chart tegnet fra artefakten, full tolvraders tabell som
alltid synlig fallback, og ærlig intervalltekst fra artefaktens meta.
Funksjonstestet i headless Chromium (tastaturnavigasjon h1→h12,
statusbytte, radmarkering). Publisering via `.github/workflows/pages.yml`;
Pages må aktiveres én gang manuelt (Settings → Pages → Source: GitHub
Actions). README fikk statisk øyeblikksbilde + lenke — ingen død slider.

## R6. Reproduksjon demonstrerbar

`renv.lock` versjonert (R 4.3.3, eksplisitt pakkesett + avhengighetslukning);
`jsonlite` lagt til pakkesettet (artefakten). CI utvidet ærlig: «Datakontrakt»
kjører nå også prognosevalidatoren; ny «Kildeverifisering» kjører
`verifiser.R` fra ren checkout; ny «Rapport-render (PDF)» bygger hele PDF-en
fra ren checkout (på relevante filendringer, hovedgren og forespørsel — for
tung for hver push). Hele løypa er kjørt fra ren klone i denne runden;
reproduserbarhetsavsnittet i rapporten er oppdatert til faktisk tilstand
etterpå, ikke før.

## R7. Arbeidsverk 2 med versjonert kilde

`rapport/arbeidsverk2_sammenfatning.qmd` (Quarto/Typst) med kolofon
(forfatter, dato, vintage, commit, byggekommando, grunnlag). Førsteutgaven
(LaTeX, tapt kilde) er arkivert uendret som
`arkiv/arbeidsverk2_sammenfatning_v1.pdf`; den nye PDF-en er en ny sporbar
versjon, ikke en rekonstruksjon. Tre substansendringer, merket i teksten:
M7-omdøpingen (R1), presisert panelfunn — pooling reduserer estimeringsvarians
og forbedrer ut-av-utvalgsprognoser, men etablerer ikke sanne koeffisienter
(før: «koeffisientene lar seg feste») — og statusnoter der hovedrapporten
senere har gjennomført det AV2 anbefalte (kunnskapsregisteret, tidsgyldig
kalibrering).

## R8. Kilder, rydding og styring

Bibliografitoppteksten beskriver nå sann status (før: «unt_1.qmd» +
«autogenerert … la den overskrive»); `fn1948` er ny, verifisert oppføring
(FN-siteringen i introduksjonen var ren tekst uten oppslag — `verifiser.R`
fanget den som manglende sitering da den ble kodet, som er nøyaktig kontrollen
den skal gjøre). Fem Husbanken-kilder verifisert mot primærkilde med URL og
dato (`logg/kildeverifisering.md`); I11/I18 står som «delvis» med dokumentert
verifiseringsspor og eksplisitt rest. Sju revisjonsverktøy fra 9.
august-økten er fjernet med `git rm` etter referansesøk (git-historikken er
arkivet); revisjonsregistrene, gullsettet og reproduksjonsskriptene står.
Introduksjonen er snudd leser-først (issue #19): styringsproblemet først,
forskningsspørsmålet tidlig, velferdsteorem-passasjen komprimert og
andre-teorem-avsnittet fjernet; nytt sammendrag foran, med
sammendragskontrakt som stopper byggingen hvis tallene i det kommer i utakt
med beregningen.

---

## 14. august 2026 — CRLF brøt prognosekontrakten

**Symptom.** Etter rendring på Windows feilet `Datakontrakt` og `Prognoseside` på
samme steg: P09, «datahash stemmer med kildefilene». Rapport-render og
Kildeverifisering gikk gjennom. Kontrakten hadde bestått i alle tidligere kjøringer.

**Årsak.** `.gitattributes` sto med `* text=auto` alene. Git sjekker da ut tekstfiler
med CRLF på Windows og lagrer dem med LF i repoet. P09 hasher kildefilene **byte for
byte** — `hashlib.md5(path.read_bytes())` — så en render på Windows skriver CRLF-hasher
inn i artefakten, mens CI leser LF og regner ut noe annet. Innholdet er identisk; det
er bare linjeskiftene som skiller.

| Fil | LF (repo) | CRLF (Windows) |
|---|---|---|
| `data/raw/husbanken_bostotte_oslo_manedlig.csv` | `f98f2c56…` | `291e69d7…` |
| `data/clean/regelverk_kunnskap.csv` | `00f1d8a9…` | `d06bf327…` |

Artefakten inneholdt de to høyre. Tidligere artefakter var generert på Linux, så
feilen kunne ikke oppstå før første lokale Windows-render.

**Rettelse, to ledd.** `.gitattributes` tvinger nå `eol=lf` for `*.csv` og `*.json`, så
arbeidskopien er byte-identisk med repoet på alle plattformer. Og de to hashene i
`prognose/prognose_gjeldende.json` er satt til den kanoniske LF-formen. Det er ikke en
omskriving av hva artefakten ble bygget fra — datainnholdet er det samme — men en
retting av hvilken representasjon hashen viser til.

**Merknad.** En kontrakt som hasher bytes, forutsetter at bytene er de samme overalt.
Den forutsetningen var udokumentert til nå. Neste gang noen sjekker ut repoet på
Windows, må `git add --renormalize .` kjøres én gang for at eksisterende arbeidskopier
skal følge den nye regelen.

**Kontrollert:** `validate_prognose.py` 13 av 13, `validate_phase1.py` 55 passert,
0 feil, 2 advarsler (uendret fra før).
