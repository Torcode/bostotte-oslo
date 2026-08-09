# Release-verifisering: `release/2026-08-09-port`

Kort sluttkontroll av release-runden 9. august 2026 (kveldsøkt), mot mandatets
ferdigdefinisjon. Full begrunnelse per endring:
`logg/endringslogg-release-2026-08.md`.

## Baseline og sluttilstand

- **Undersøkt baseline:** `origin/main` @
  `d503897507cad97415ea32502648dd6ff67d1c52` (merge av PR #21) — verifisert
  identisk med mandatets kontrollpunkt; `main` hadde ikke beveget seg.
- **Sluttilstand for leveransen:** commit `13433e7` («Regenerert leveranse»);
  dette dokumentet er lagt til i påfølgende commit. Grenen bygger på baseline
  uten historieomskriving; arbeidskopien var ren klone (ingen brukerendringer
  sto i fare).
- **Datavintage:** Husbanken-uttrekk 4. august 2026 (uendret);
  regelverkskalender kuratert per 9. august 2026.

## Kommandoer kjørt (miljø: ren Linux-container, R 4.3.3, Quarto 1.7.34)

```
git clone https://github.com/Torcode/bostotte-oslo && git checkout -b release/2026-08-09-port
Rscript -e 'source("verifiser.R")'          # før og etter hver endringsrunde
python3 scripts/validate_phase1.py           # baseline og slutt
quarto render bostotte_oslo.qmd              # baseline (uendret kilde), midtveis og slutt
python3 revisjon/repro_protokoll.py          # uavhengig protokollreproduksjon, før og etter
python3 scripts/validate_prognose.py         # etter at artefakten fantes
quarto render rapport/arbeidsverk2_sammenfatning.qmd
git clone <lokalt> /tmp/ren && <hele løypa på nytt fra ren checkout>
node test_side.js                            # Playwright-funksjonstest av prognosesiden
```

## Kontroller og resultater

| Kontroll | Resultat |
|---|---|
| `verifiser.R` (parse i C-locale, bibliografi, kryssreferanser) | Bestått ved slutt: 31 chunker, 148 inline-uttrykk, 0 klammetekst, alle 69 kryssreferanser med anker. Underveis fanget den `fn1948` som sitering uten oppføring — kontrollen for manglende siteringer er dermed demonstrert i drift |
| `validate_phase1.py` | 55 kontrakter bestått, 0 feil (2 kjente advarsler: I11/I18 delvis, bibliografi-plassholdere) — baseline og slutt |
| `validate_prognose.py` | 13/13 artefaktkontrakter bestått (P01–P13), inkl. datahash, commit-sporbarhet og README-utdrag ordrett i README |
| Uavhengig reproduksjon (`repro_protokoll.py`) | Uendret etter alle rettelser: 10/10 M0/M1-tall eksakte; 270 felles konformalpunkter; 78,5/67,4-dekomponeringen står |
| Gullsettet (`gullsett_referanse.csv`) | Invariansen holder: kjent- og fryst-kolonnene skiller lag bare ved opprinnelse 2023-10 h=6/h=12 (vedtakssteg i horisonten etter kunngjøringen 6. okt); identiske ved 2023-03 og 2025-06 |
| Full render, arbeidskopi | 44 sider, 0 tegnsett-escapes; sammendragskontrakten (fire deklarerte prosatall dømt mot beregningen) bestått |
| Ren-checkout-test (`/tmp/ren`, uten cache) | Bestått: verifiser.R + 55 datakontrakter + full render uten cache (44 sider, 0 escapes) + 13/13 artefaktkontrakter; alle tolv prognoserader og årsgjennomsnittet bitidentiske med arbeidskopiens artefakt |
| Prognoseside | Funksjonstestet i headless Chromium: tastaturnavigasjon h1→h12, statusbytte vedtatt kalender ↔ basisbane, radmarkering i tolvraders tabell, årssnitt og kolofon; skjermbilder kontrollert visuelt, mobilbredde 390 px OK |
| Visuell sidekontroll PDF | Side 3 (sammendrag), 25 (M7 orakel-metode), 35 (M7 orakel-resultat), 40–42 (prognosekapittel med tabell, fanchart og årsstørrelse) lest i bilde — layout, bånd og betingelseskolonne korrekte |
| README-lenker/-status | Utdraget håndheves ordrett mot artefakten (P13); sideantall (44), kontraktstall (55/13) og issue-omtale uten hardkodet telling lest korrektur mot HEAD |

## Hovedpåstander: bekreftet, avkreftet, presisert

- **Bekreftet:** Prosjektets bærende resultat består etter M7/T5-rettelsen —
  fortrinnet over naiv kommer fra datert regelverksinformasjon, ikke
  modellkapasitet. Rettelsene er semantiske; regenerert tabellverk er
  verifisert identisk (MASE-stigen 0,890/0,931/0,937/0,960/1,003/1,071/
  1,131/1,228; PIT 15 552/15 588; dekning 48 → 79).
- **Avkreftet (og rettet):** at M7 var en modell med daterte forhåndsanslag.
  Kjøringen pålegger full-utvalgskoeffisienten; modellen heter nå M7 orakel
  (øvre grense), og `M7_prior` er reservert og uimplementert i påvente av en
  reell kilde med dokumentert `known_from`.
- **Presisert:** T5 er ikke testbar som forhåndsregistrert (ingen publisert
  husstandsprior for høstpakken; der prior finnes, er koeffisienten
  estimerbar) — konsistent i metode, resultat, diskusjon og konklusjon, med
  merket ettertidspresisering ved den forhåndsregistrerte tabellen.
  Horisontmekanisk «prognose vs. beregning» er erstattet av
  informasjonssett-regelen per målmåned. AV2s «koeffisientene lar seg feste»
  er presisert til variansreduksjon ved pooling, ikke identifikasjon.

## Kjente rester

1. Bibliografi: 25 oppføringer med PLASSHOLDER-metadata; I11 (månedssatser
   jan–apr 2024) og I18 (statsrådens svar) delvis belagt — synlig i
   `logg/kildeverifisering.md`. Rapporten er ikke kildeferdig.
2. GitHub Pages må aktiveres manuelt (Settings → Pages → Source: GitHub
   Actions) før prognosesiden er live; workflowen validerer artefakten før
   publisering. CI-workflowene «Kildeverifisering» og «Rapport-render (PDF)»
   er skrevet og lokalt ekvivalens-testet (samme kommandoer fra ren checkout),
   men får sin første Actions-kjøring først når grenen er pushet.
3. `M7_prior` og β̂-mot-λ-sporingen: presist definert, venter på kilde.
4. Artefaktens commit-felt peker på kildecommiten renderingen leste
   (foreldren til artefakt-commiten) — dokumentert egenskap, ikke avvik.
5. Bundle-filen fra 9. august-økten ligger lokalt hos brukeren og må
   `git bundle verify`-sjekkes mot origin før eventuell sletting; ikke
   tilgjengelig fra denne økten.
