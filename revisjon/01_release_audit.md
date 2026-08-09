# Uavhengig revisjonsrapport: `Torcode/bostotte-oslo`

Revidert 9. august 2026, mot HEAD `4f441560e0baadd67f1e53cbfa52b55fe5d2e112` (`main`),
uttrekk 2026-08-04. Repoet er offentlig (klonet uautentisert). Vedlegg i `revisjon/`:
`kryssrevisjon_av2_mot_av1.csv`, `claim_register.csv`,
`regelverksregister_kunnskapsdatoer.csv`, `gullsett_referanse.csv`,
`repro_protokoll.py`, `repro_k7.py`.

## Dom

En senior fagperson i Velferdsetaten som åpner dette repoet i dag, møter et uvanlig
ærlig og uvanlig godt kontrollert analyseprosjekt som ennå ikke holder det
inngangsdøra lover. README lenker til en «PDF, 36 sider» som er 38, kaller tre feil
åpne der sytten issues står åpne (fem P0), og hevder en PDF som er «identisk på
enhver maskin» — mens den innsjekkede PDF-en har 284 synlige tegnfeil av typen
`<U+00A0>` i nettopp de tabellene resultatene bor i.

Det mest troverdige i repoet er, i denne rekkefølgen: datagrunnlaget (47 kontrakter
kjører i CI og består fra ren checkout; jeg har vist ved mutasjon at de kan stryke),
evalueringsprotokollen (jeg har reprodusert M0/M1-referansene fra rådata med
uavhengig kode — alle ti publiserte tall eksakt), og kvalitetskontrollen i notebook
07: dens hovedtall, inkludert hele K7-tabellen, reproduserer eksakt i et rent miljø
(`repro_k7.py`, 15 av 15 tall). Selvkorreksjonskulturen er reell — feilene M10,
M14–M20 er funnet, målt og logget, ikke skjult.

Det som blokkerer bruk er informasjonssettet, ikke modellene. Kryssvalideringen gir
hver historisk opprinnelse dagens komplette regelverkskalender. Primærkildesporet
jeg har etablert (Norsk Lovtidend, Stortingets innstillinger, regjeringen.no)
avgjør saken: avviklingen med virkning termin april 2024 ble offentlig først
6. oktober 2023, og i juli 2023 var den kunngjorte sluttdatoen 31.12.2023 — den
lovfestede sluttdatoen ble flyttet fem ganger. Flaggskipsresultatet «traff
aprilfallet fra ni måneders horisont» er derfor en betinget orakelberegning, ikke
en prognose. Det ærlige tallet er sterkere enn det ser ut: fra opprinnelse oktober
2023 — etter kunngjøringen — treffer M6 med 15 552 mot fasit 15 588 på seks
måneders horisont, et avvik på 0,2 prosent, og det tallet er rent. I samme kategori
ligger konformalkalibreringen: skjemaet bruker feil som ikke var realisert ved
opprinnelsen, og «45 → 73 prosent» står fortsatt i PDF-en.

Den bærende påstanden etter retting bør være hypotesen dette prosjektet nå faktisk
har belegg for, målt i K7 og reprodusert her: fortrinnet over naiv framskrivning
kommer i det vesentlige fra datert regelverksinformasjon, ikke fra modellkapasitet
— kortsiktsfortrinnet (h 1–3: 0,65 mot naivens 0,74) overlever at framtidige
vedtak er ukjente, langsiktsfortrinnet gjør det ikke (0,85 → 1,34 mot naivens
1,12). Leveransen som følger av det er en versjonert, point-in-time-riktig og
scenarioorientert prognoseprosess for Oslo og bydelene, der vedtatte regler inngår
i basisbanen fra sin dokumenterte kunngjøringsdato og ikke-vedtatte forslag bare
finnes i navngitte scenarioer. Repoet underbygger hypotesen; det håndhever den
ennå ikke.

## Preflight

Kjørt: `git status --porcelain` (rent), `git branch -a`, `git rev-parse HEAD`,
`git remote -v`. HEAD `4f44156` på `main`; eneste sidegren `docs/phase-1-contract`
(grunnlaget for PR #12). Repoet er offentlig. Brukerens lokale arbeidskopi på PC
(`Velferdsprosjekt/`) står på `8a80bc4` — 24 commits bak `main` — med rent tre;
ingen brukerendringer står i fare, men kopien må pulles før videre arbeid der.

Artefaktklassifisering: kilde (`bostotte_oslo.qmd`, `notebooks/*.ipynb`,
`data/scripts/`, `scripts/`, `mal/`, `oppsett.R`, `verifiser.R`); generert utdata
versjonert med hensikt (`bostotte_oslo.pdf`, notebook-utdata i cellene); generert
utdata uten versjonert kilde (`rapport/arbeidsverk2_sammenfatning.pdf` — .tex-kilden
er tapt); arkiv/proveniens (`data/raw/`, `litteratur/`, `logg/`).

CI (`.github/workflows/ci.yml`) kjører nøyaktig to ting: `validate_phase1.py`
(47 datakontrakter, manifest-artefakt) og `python -m compileall` på skriptene.
Den bygger ikke rapporten, kjører ikke notebooks, kjører ikke `verifiser.R`.
Grønn CI beviser datakontrakt og Python-syntaks — ikke «Backtestet»-raden i
READMEs statustabell, og ikke at PDF-en kan gjenskapes.

## A. Kryssrevisjon (vedlegg: `kryssrevisjon_av2_mot_av1.csv`)

Hvert avvik arbeidsverk 2 hevder, er behandlet som hypotese og sporet til kode,
utvalg og berørt sted. Sammendrag av statusene:

- **Bekreftet ved uavhengig reproduksjon** (min kode, fra rådata): konformallekkasjen
  (78,5 mot 67,4 % på nøyaktig 270 felles punkter; asymmetri 32/2; kvantilforhold
  median 1,00 / snitt 1,28 / maks 5,8 — alle eksakt som oppgitt), den manglende
  endelig-utvalgskorreksjonen (lekkasje 11,1 → 11,9 pp, robust; underdekning
  12,6 → 5,6 pp), hele K7-tabellen (15 av 15 tall), M0/M1-referansene (10 av 10),
  osloandelens bane (14,4 / 19,9 / 18,5 %) og at CV-koden bruker
  `LAMBDA_ORAKEL`, ikke `osloandel` — kapittel 4-tallene er ikke berørt av M13.
- **Bekreftet ved kodelesning, tall fra lagret utdata**: K1 (Clark–West-formelen er
  korrekt; 0/36 → 13/36), K2 (klynget test korrekt spesifisert; 5,38 → 1,56;
  MASE-gevinsten 0,836 → 0,797 står), K5 (ny kontroll stryker på mutasjon).
- **Viktig presisering**: arbeidsverk 1 er ikke rammet av K1 — dokumentet bruker
  allerede Clark–West på nøstede par. K2 rammer heller ikke arbeidsverk 1, som
  ikke har bydelsanalyse.
- **Avkreftet**: statusdokumentets «PR #12 er slått sammen» (PR-en er åpen med
  konflikter; CI-delene ble hentet manuelt i `d0d1a40`).
- **Nytt funn ingen av arbeidsverkene har fanget**: metodekapitlet lover en figur
  som skårer prior-implisert λ mot estimert β̂ (T5, «egen figur i kapitlets andre
  del»); den finnes ikke i kapittel 4. `forhandsanslag.csv` leses inn og brukes
  aldri i en beregning.

Arbeidsverk 2 implementerer sine egne rettelser korrekt der jeg har kunnet regne
dem etter. Ett metodespørsmål er avgjort til AV2s fordel med numerisk bevis:
`np.quantile(…, method="linear")` etter nivåjusteringen ⌈(n+1)(1−α)⌉/n ligger
alltid i [s₍ₖ₎, s₍ₖ₊₁₎] og er dermed aldri under den påkrevde ordensstatistikken —
garantien holder, `method="higher"` kreves ikke (eksakt ordensstatistikk fås med
`inverted_cdf`). Uten nivåjusteringen — som i notebook 02/05 og i arbeidsverk 1 —
undershooter den empiriske kvantilen, som er nettopp K3-funnet.

PDF-status: arbeidsverk 1 er 38 sider (README sier 36), har verken sammendrag,
diskusjon eller konklusjon (slutter i 4.8 + referanser), har de motstridende
dekningstallene 73/42 (tabell 17, s. 30) mot 81/45 (brødtekst og figur 4, s. 32)
uten note, og 284–385 escapede tegnsekvenser i 17 maskingenererte tabeller og tre
figuretiketter — den feilen `verifiser.R`-vakten ble bygget for å stoppe, i den
PDF-en som faktisk er sjekket inn. Arbeidsverk 2-rapporten er 16 sider, uten
forfatter, dato, versjon eller commit, og uten kildefil i repoet. Diskusjon og
konklusjon i arbeidsverk 1 kan trygt skrives først når C02/C06/C07 (claim-registeret)
er avgjort — det er de nå, ved denne revisjonen, så skrivingen kan starte, men
teksten må bygge på det tidsgyldige kalibreringsskjemaet og PIT-merkingen.

Kanonisk dokument (forslag — ikke gjennomført): `bostotte_oslo.qmd`/PDF forblir
kanonisk leveranse; arbeidsverk 2-rapporten er kanonisk *metoderevisjon* og får
kildefil + kolofon i repoet; `logg/` forblir revisjonsspor; dagens PDF bevares
uendret til ny render foreligger, deretter erstattes den og den gamle arkiveres
med erratum-note (M15/K3, #17, sidetall). Ingen dokumenter bør slettes.

## B. Claim-register (vedlegg: `claim_register.csv`)

Tjue kontrollerte påstander C01–C20. De som flytter tall eller tolkning:

| | Kortform | Status |
|---|---|---|
| C02 | «45 → 73 %» konformal reparasjon | Avkreftet som driftstall (lekkasje; P0) |
| C06 | `known_from` finnes og håndheves | Avkreftet — finnes ikke (P0; issue #6 er riktig) |
| C07 | PIT/orakel blandes ikke | Delvis avkreftet — flaggskipet 9 mnd er orakelbetinget; PIT-formen (okt. 2023, h=6, 0,2 %) er sterkere og ren |
| C10–C12 | «ikke autoregressiv», «enkleste best», «ikke en prognose» | For sterke som formulert; presise former angitt i registeret |
| C13–C14 | README- og QMD-selvbeskrivelse (36 sider, renv, `unt_1.qmd`) | Avkreftet på HEAD |
| C15 | Lovet prior-λ-figur | Avkreftet — ubetalt løfte (nytt funn) |
| C17 | AV2-rapportens reproduksjonsvei | Avkreftet — kilde utenfor repo |

## C. Reproduksjon og kontroller

Kjørt i denne økten, fra ren checkout: `validate_phase1.py` (47 bestått, 2
advarsler: I11/I18 delvis kildeverifisert, 33 bibliografi-plassholdere) pluss
mutasjonstest — én korrumpert verdi i bydelsfila gir 3 feil og exit-kode 1, så
kontrollen er vist å kunne stryke. `repro_protokoll.py` (min kode): M0/M1 eksakt;
konformalskjemaene eksakt; kvantilmetode-beviset. `repro_k7.py` (min kode, torch
2.13 CPU + xgboost): alle 15 K7-tall eksakt, 374 sekunder.

Ikke kjørbart her, dokumentert som manglende avhengigheter: R + `fable`-stakken og
Quarto (kreves for `verifiser.R` og `quarto render`; miljøet har Python 3, numpy
2.4.4, pandas 3.0.2; torch og xgboost måtte installeres). Rendering av
arbeidsverk 1 og re-kjøring av ETS/SARIMA/M4–M7 står derfor som notebook-/PDF-bundne
resultater; M0/M1/L0/G2-sporet er én-kommando-reproduserbart med skriptene i
`revisjon/`. CI bygger verken rapport eller notebooks — en render-smoketest er
neste naturlige CI-utvidelse (issue #3).

**Gullsett** (vedlegg: `gullsett_referanse.csv`): tre opprinnelser × h ∈ {1,3,6,12}
med fasit, naiv, L0/G2 kjent og fryst — valgt for å spenne regimene: 2023-03
(strømvindu aktivt, ingen vedtakssteg i horisonten — kjent og fryst skal være
identiske, og er det), 2023-10 (avviklingen nettopp kunngjort 6. oktober — PIT-skillet
synlig: kjent ≠ fryst ved h=6 og 12), 2025-06 (siste opprinnelse, etter skjermingen).
Kjør settet før og etter enhver senere rettelse; identiske kjent/fryst-kolonner
ved 2023-03 og 2025-06 er i seg selv en kontroll på at frysingen bare virker der
den skal.

## D. GitHub-styring

18 issues (17 åpne, 1 lukket) + PR #12. Klassifisering:

| Issue | Klassifisering | Anbefaling |
|---|---|---|
| #6 informasjonssett/known_from | fortsatt relevant, P0, kjernen | Behold; primærkildedatoene fra E limes inn (ferdig formulert i `revisjon/github_handlinger.md` — Chrome-broen fikk ikke sendt skjemaer mot GitHub i denne økten, og git-proxyen nekter push) |
| #17 dekningsutvalg | fortsatt relevant, P0; sidetall foreldet (29/31 → 30/32) | Behold, oppdater sidetall |
| #13 M7-korreksjon | fullført men åpen (M10-fiks + to stopifnot-kontroller + regenerert PDF verifisert i kode/PDF) | Lukk med verifikasjonsbevis |
| #14 duplikat av #13 | korrekt lukket | Ingen handling |
| #15 M7-prosa | delvis fullført («tredjedel»-formuleringen er fjernet, prosa inline-bundet); rest: «innenfor tre prosent» (3,2 %) og generell hardkodings-sweep | Behold, innsnevre omfang |
| #3 reproduserbarhetsløfter | fortsatt relevant, P0 — alle premisser verifisert på HEAD (ingen renv.lock, ingen set.seed, to `unt_1.qmd`-referanser, identisk-PDF-påstand motbevist) | Behold |
| #5 konsistensport | fortsatt relevant, sluttport | Behold |
| #1 + PR #12 | avgjørbar nå: main har allerede validator/CI/README; PR-en er konfliktfylt og bygger på utgått arkitektur | Lukk PR #12 som supersedert, deretter #1 |
| #8 Colab-eksperiment | i hovedsak fullført av notebooks 01–07 (kjørbare topp–bunn, versjonert datakilde, lekkasjetester, baseline-sammenlikning); rest: felles pakke i stedet for duplisert protokoll | Lukk med henvisning; flytt resten til nytt issue eller #7 |
| #2, #16 | fortsatt relevante (33 plassholdere; hengende referanser) | Behold |
| #4, #7, #9, #10, #11, #18, #19 | fortsatt relevante | Behold |

Avhengighetsstyrt rekkefølge (ikke øktnummerert):

1. **#6** — known_from-register og port i prognoseløkka. Alt resultatbærende er
   nedstrøms; regelverksregisteret i E gir radene.
2. **Én samlet re-render av arbeidsverk 1** som tar #17, konformalrettelsen
   (C02/M15/K3), «innenfor 3,2 %», `unt_1.qmd`-referansene og renv-setningen —
   rendret i et miljø der tegnsettvakten faktisk stopper, slik at de 284 escapene
   dør i samme operasjon. (#13 lukkes, #15 innsnevres.)
3. **Reproduksjonsveier**: AV2-kilden (.tex) inn i repoet med kolofon; README-fakta
   (38 sider, AV2-status, issue-telling); render-smoketest i CI (#3).
4. **#2/#16** før noen kaller rapporten kildeferdig; **#5** som port til slutt;
   #9/#11/#18/#19 løpende; #10 (drift) etter porten — med varsling på
   intervallskår, ikke MASE, jf. AV2-rapportens 8.2.

## E. Regelverkskilder (vedlegg: `regelverksregister_kunnskapsdatoer.csv`)

Sju hendelser (I01, I05, I12, I14–I17) er etablert utelukkende fra primærkilder:
Norsk Lovtidend-kunngjøringer med fastsettelses- og opphevingsdatoer,
stortingsinnstillinger med voteringsdatoer, og regjeringens fremleggelser. Ingen
rader er lagt inn i `data/` — registeret er revisjonsgrunnlag til issue #6.

Hovedfunnene: (i) point-in-time-registeret **lar seg bygge troverdig** — tre
uavhengige daterte ankere per hendelse (fremleggelse, votering, kunngjøring), og
alle sju kjedene lot seg rekonstruere; (ii) fire av sju regelendringer oppsto i
**budsjettforlik**, ikke i regjeringens dokumenter, så tidligste siterbare
primærkilde (innstillingen) kan ligge dager etter faktisk offentliggjøring —
`effect_known_from` blir konservativt sen, som er riktig side å feile på;
(iii) **solnedgangsdatoer er upålitelige prediktorer** — egenandelsregelen fikk fem
lovfestede sluttdatoer før den faktisk utløp, så et register som tolker
«oppheves»-datoer som framtidskunnskap vil systematisk bomme; K7s frysing er den
konservative nedre grensen, dagens praksis den øvre, og sannheten en tredje bane:
«kunngjort sluttdato per opprinnelse»; (iv) skillet regelendring / bevilgning /
utgiftsanslag / politisk mål er reelt i kildene — Prop. 104 S inneholdt for
bostøtten bare et utgiftsanslag (+232 mill.), mens selve regelendringene kom i
forliket (Innst. 447 S), og I17s faktiske innhold er en
tre-meldekortutbetalinger-korreksjon, ikke en generell etterbetalingsskjerming —
prosjektets etikett må presiseres.

Overvåkning: poll Norsk Lovtidend (endringsforskrifter til FOR-2012-11-29-1283),
Stortingets saksgang for rammeområde 6 og KDD-pressemeldinger; en oppdaget hendelse
legges i et forslagsregister og tas inn i prognosegrunnlaget først etter menneskelig
godkjenning med kilde-URL og datert innhold.

## Utførelse i denne økten

Undersøkt HEAD: `4f441560e0baadd67f1e53cbfa52b55fe5d2e112`. Kommandoer: se
prefligt/C over; fullstendig i skriptene. Kontroller bestått: 47 datakontrakter +
mutasjonstest; 10/10 M0/M1-tall; 270-punkts konformalavstemming; 15/15 K7-tall.
Ikke kjørbart her: `verifiser.R`, `quarto render`, ETS/SARIMA-stigen (krever R).
Bekreftet/avkreftet/åpent: se claim-registeret; åpne står C19 (ekstern validering
mot årsrapporttall) og de R-bundne tallene.

Implementert i denne revisjonen (gren `revisjon/2026-08-09-audit`): denne mappen
(`revisjon/`), konformalrettelsen i `bostotte_oslo.qmd` (tidsgyldig skjema +
endelig-utvalgsnivå, gammelt skjema beholdt som eksplisitt merket
sammenlikningskolonne), retting av de to `unt_1.qmd`-selvreferansene og
renv-setningen, «innenfor 3,2 %» med informasjonssett-forbehold, samt
README-faktarettinger (38 sider, AV2-status, issue-telling). QMD-endringene
krever re-render før PDF-en byttes; dagens PDF er bevart urørt som revisjonsspor.
Push og GitHub-skriving var blokkert i økten (git-proxy uten credential;
Chrome-skjemaer nådde ikke fram) — grenen leveres som bundle/patch, og
issue-handlingene står ferdig formulert i `revisjon/github_handlinger.md`.

## De tre første endringene, i rekkefølge

**1. Innfør `known_from`/`effect_known_from` og håndhev dem per opprinnelse
(issue #6), med radene fra `regelverksregister_kunnskapsdatoer.csv`.** Først fordi
det avgjør hva prosjektets viktigste resultat *er* — K7 og primærkildene viser at
hele langsiktsfortrinnet står og faller med dateringen — og fordi enhver render
før dette bare sementerer en tabell som må regnes om igjen.

**2. Én samlet re-render av arbeidsverk 1 med tidsgyldig konformalskjema,
harmonisert dekningsutvalg (#17) og de små tekstrettelsene — i et miljø der
tegnsettvakten stopper.** Etter 1 fordi rendringen da tar begge tallendringene i
samme operasjon; dette er den ene handlingen som fjerner flest P0-defekter
(C02, #17, C13-delvis, C14, C16 og de 284 escapene) fra selve leveransen.

**3. Legg arbeidsverk 2-rapportens kilde i repoet med forfatter, dato, commit og
byggekommando, og rett README til å beskrive repoet som det er.** Etter 2 fordi
README skal peke på den nye PDF-en med riktig sideantall og status; uten kildefil
er metoderevisjonens egne konklusjoner ikke reproduserbare, og README er det
første en fagfelle ser.
