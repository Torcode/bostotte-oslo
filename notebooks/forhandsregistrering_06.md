# Forhåndsregistrering, notebook 06: avstemming og dekning

**Committet før noen modell i notebook 06 er kjørt.** Notebook 06 henter filen fra
`main` og viser sha256 og commit-dato ved siden av resultatene. Samme ordning som for
notebook 05.

## De to spørsmålene

Notebook 05 etterlot to ting. Prognosene for de seksten seriene **summerer ikke opp**:
bydelene er prognostisert hver for seg, og summen deres er ikke Oslo-prognosen. Og
ingen kalibrering nådde nominelt nivå — beste dekning var 73,7 mot 80.

## Hierarkiet

Oslo er summen av femten bydeler pluss en ufordelt restnode `0301`. Restnoden er i
praksis tom: i evalueringsvinduet 2023m1–2026m6 er den null i 40 av 42 måneder og én
husstand i de to andre, og fra 2025m12 rapporteres den ikke. Hierarkiet behandles
derfor som Oslo = sum av femten bydeler, med et dokumentert avvik på høyst én
husstand — 0,006 prosent. Avviket måles i notebooken framfor å antas bort.

Bunnnodene er på 363 til 2 212 mottakere i snitt, mot Oslos 17 000.

## Fire påstander

**Q1 — Avstemming gir liten gevinst for Oslo-totalen.**
Notebook 01 målte effektiv dimensjon 1,2 av 15: bydelene bærer i hovedsak én felles
bevegelse, og restleddet er en størrelseseffekt framfor lokal informasjon. MinT henter
styrke fra uavhengig informasjon i bunnnodene, og den er knapp her. I tillegg er
basisprognosene laget av **én** global modell trent på hele panelet, så de deler både
trekk og parametre og har korrelerte feil.
*Felles hvis en avstemt prognose slår den direkte Oslo-prognosen med
Diebold–Mariano over 1,64 på noen av h = 1, 3, 6, 12.*

**Q2 — Bottom-up er dårligere enn direkte prognose for toppnivået.**
Å summere femten prognoser for serier på under to tusen mottakere gir mer varians enn
å prognostisere en total på sytten tusen direkte.
*Felles hvis bottom-up har lavere MASE enn den direkte Oslo-prognosen.*

**Q3 — Avstemming hjelper bunnnivået mer enn toppnivået.**
Avstemming flytter informasjon begge veier, men den velestimerte totalen har mer å gi
de støyende bydelene enn omvendt.
*Felles hvis gjennomsnittlig MASE over de femten bydelene ikke bedres av avstemming.*

**Q4 — Endelig-utvalgskorreksjonen forklarer en del av underdekningen, og mest der
kalibreringsgrunnlaget er tynt.**
Notebook 02 og 05 bruker den empiriske kvantilen direkte. Den endelig-utvalgsgyldige
varianten for split-konformal er $\lceil (n+1)(1-\alpha) \rceil / n$. Med $n = 19$ gir
det nivå 0,842 i stedet for 0,80; med $n = 304$ gir det 0,803. Korreksjonen skal
derfor løfte dekningen merkbart i skjemaet som kalibrerer på Oslos egen historie, og
nesten ikke i panelskjemaet.
*Felles hvis korreksjonen ikke løfter dekningen i egen-historie-skjemaet, eller hvis
den løfter panelskjemaet like mye.*

## Hva som måles ved siden av

- Hvor mye av avstanden opp til 80 prosent som står igjen etter korreksjonen. Blir
  den stående, peker det på at feilene ikke er utbyttbare **over tid** — notebook 05
  målte utbyttbarhet på tvers av serier, ikke over tid — og da er bruddmånedene den
  nærliggende forklaringen.
- Det faktiske koherensavviket mellom Oslo og summen av bydelene, før og etter
  avstemming.

## Oppsett som er bestemt på forhånd

- Basismodell: L0, den lineære modellen fra notebook 04, trent globalt på panelet i
  kommunenummerrekkefølge. Én tilpasning per opprinnelse og horisont, prognoser for
  alle nodene fra den samme.
- Avstemmingsmetoder: bottom-up, top-down med historiske andeler målt i
  treningsvinduet, og MinT med krymping mot diagonalen. Kovariansmatrisen estimeres
  **tidsgyldig**, på prognosefeil som var realisert ved opprinnelsen.
- Samme protokoll: 31 opprinnelser, h = 1–12, 372 punkter per node.
- Nominelt nivå 80 prosent, straffevekt 2/α = 10.
- Ingen hyperparametre justeres.

Alt som avviker fra dette, skal begrunnes i notebooken.
