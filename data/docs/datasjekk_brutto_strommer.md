# Datasjekk: brutto strømmer i bostøttebeholdningen for Oslo

Skrevet 18. august 2026, mot statistikkbank-appen dokumentert i
`datakilder.md` (app-id `ee185fe5-e94d-463e-bff8-cd1c5f2f566f`, reload
2026-08-18 05:33 UTC). Alle tall i notatet er avlest fra spørringene i
`data/scripts/utforsking/utforsk_strommer.py`, som regenererer hele belegget
på ett par minutter. Ingen filer i den frosne datapakken (uttrekk 4. august)
er endret; der spørringene overlapper pakken, er verdiene kontrollert like
punktvis (2024m1/m4–m7, 2026m1/m4–m7, eksakt match).

**Spørsmålet.** Kan statistikkbanken skille *innganger* fra *avganger* i
mottakerbeholdningen — månedlig, for Oslo — slik at nettoendringen kan
dekomponeres i brutto strømmer?

**Svaret er ja, observert, ikke bare residualt.** Elementfunksjonen `P()` i
Qlik-motorens set analysis kan telle husstander som er innvilget i termin
*t* **og** var innvilget i termin *t−1* («overlevere»). Begge strømmene
følger da av regnskapet, uten mikrodata:

    innganger_t = beholdning_t − overlevere_t
    avganger_t  = beholdning_{t−1} − overlevere_t

Målt for fem terminpar (Oslo, `Fylke='Oslo'`, samme set-uttrykk som
terminserien i pakken):

| Termin | Beholdning | Overlevere fra t−1 | Innganger | Avganger | – herav førstegang |
|---|---|---|---|---|---|
| 2024m04 | 15 588 | 14 888 | 700 | 5 961 | 472 |
| 2024m05 | 16 353 | 14 186 | 2 167 | 1 402 | 538 |
| 2025m06 | 16 590 | 15 460 | 1 130 | 2 670 | 485 |
| 2025m07 | 16 993 | 15 412 | 1 581 | 1 178 | 501 |
| 2026m06 | 16 428 | 15 340 | 1 088 | 1 735 | 537 |

Tallene forteller en konsistent historie: avviklingsterminen april 2024 er
nesten ren utstrømming (5 961 ut, 700 inn), og allerede måneden etter kommer
2 167 inn igjen — hvorav bare 538 er førstegangssøkere, resten tilbakevendere.
Juni-dippene (2025, 2026) er samme mønster i mindre skala: forhøyet
utstrømming én måned, forhøyet gjeninnstrømming den neste. Kostnaden er noen
sekunder per terminpar; full historikk er en løkke, ikke et hinder.

## Feltene som bærer dette

Fakta-tabellen (67,8 mill. rader) har det som trengs, verifisert ved oppslag:

- `TypeTilstand` ∈ {Søknad, Avslag, Terminutbetaling, Utbetaling, …} med
  tellerne `BostøtteSøknadTeller`, `-VedtakTeller`, `-AvslagTeller`,
  `-UtbetalingTeller` (samme som i uttrekksskriptet).
- `BstVedtaksutfall` ∈ {Innvilget, Avslått} — kobler utfall på søknadsnivå.
- `Førstegangs søknad` ∈ {0, 1} — skiller nye i ordningen fra tilbakevendere.
  Oslo har hatt 482–673 førstegangsinnvilgelser per måned de siste tolv
  terminene; gjeninntreden dominerer altså inngangene.
- `Vedtakskode` — avslagsgrunn, koblet mot bostøttefakta. Oslo 2025:
  «For høy inntekt ift boutgift» 12 194 husstander, deretter «Manglende
  opplysninger» 2 217, «Ikke i folkereg. på sit-dato» 1 536, fire mindre
  grunner. Juni-toppen i avslag er i sin helhet inntektsgrunnen: mai→juni
  2025 økte totalavslagene 3 062 → 4 551, inntektsgrunnen 2 610 → 4 067.

To regnskapsidentiteter holder i alle 198 terminkjørte måneder 2010m1–2026m6
(kontrollert i skriptet): `søknader = innvilgede + avslag`, og fra 2017
`utbetaling_t = innvilgede_{t−1}` uten ett eneste brudd. Den siste bekrefter
vintage-skillet i `datakilder.md`: terminserien er vedtaksmåneden,
utbetalingsserien samme masse én måned senere.

En lesning dagens kolonnenavn inviterer til, er derfor feil: `ant_soknader`
er **ikke** nysøknadstrykk. Månedlig «søknad» i appen er den automatiske
månedsbehandlingen av alle løpende saker pluss nye søknader (derav
identiteten over). Trykket fra *nye* søkere er `Førstegangs søknad`-flagget;
gjentaksavslagene er løpende saker som ryker den måneden — i juni 2025 var
3 902 av 4 551 avslag gjentakssaker.

## Forbehold som må deklareres ved bruk

1. **Husstands-ID-stabilitet er uverifiserbar herfra.** `distinct HusstandId`
   over to terminer forutsetter at samme husstand bærer samme ID; splittes
   husstanden eller bytter hovedperson, telles én reell videreføring som
   avgang + inngang. Kan ikke kontrolleres uten mikrodata.
2. **Oslo-strømmer er geografiske.** Flytting inn/ut av Oslo teller som
   inngang/avgang i Oslo-regnskapet selv om husstanden står i ordningen
   nasjonalt. Skillet kan trolig måles (P() uten fylkesbetingelse i det indre
   settet), men det er ikke gjort her.
3. **Ingen vintage for strømmene.** Appen reloades hver natt og har ikke
   historiske årganger; etterkontrollen mot skatteoppgjøret reviderer
   historikken på stedet. Strømserier kan derfor bare point-in-time-fryses
   fra i dag og framover — en historisk backtest på strømmer arver dagens
   revisjonstilstand, og det må sies høyt i alt som bygges på dem.
4. **Brukergruppestrømmer blander gruppebytte og ordningsbytte.** En husstand
   som går fra «midlertidige trygdeytelser» til «uten trygdeytelser» vil
   framstå som avgang + inngang på gruppenivå. Total-strømmene er upåvirket.

## Status

Dette notatet er en datasjekk, ikke en leveranse av nye serier: ingenting er
lastet inn i datapakken, og ingen notebooks er bygget. Om funnene skal brukes
(brutto strømmer/churn; event-study på brukergrupper), avgjøres i egne
issues med designskisse per notebook.
