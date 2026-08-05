# Datapakke: Bostøtte-prognoseprosjektet (Velferdsetaten-prep)

Bygget 4. august 2026. Alle serier hentet maskinelt fra offisielle kilder med reproduserbare skript (`scripts/`). Kjernefunnet: **Husbankens statistikkbank fører Oslo per bydel**, og både termin- og utbetalingskalenderen ligger i datamodellen — vintage-skillet prosjektdesignet krever er dermed direkte observerbart.

## 1. Kjerneserier — Husbankens statistikkbank (Qlik Engine API)

Kilde: `https://statistikk.husbanken.no/bostotte` — Qlik Sense-app «Statistikkbank» (app-id `ee185fe5-e94d-463e-bff8-cd1c5f2f566f`, åpen anonym tilgang via `wss://qlik.husbanken.no/public`). Appen lastes på nytt hver natt (~05:30 UTC); uttrekket her er fra reload 2026-08-04 05:33 UTC. Uttrekksskript: `scripts/qlik_engine.py` + `scripts/extract_bostotte_v2.py`.

**Historikk: januar 2010 → juli 2026 (199 måneder).** Oslo er kodet per bydel med egne «kommunenumre» (0311 Gamle Oslo … 0325 Søndre Nordstrand; 0301 er en nesten tom rest — ikke bruk den som Oslo-total). Oslo-total = selection `Fylke='Oslo'`.

| Fil (data/raw/) | Dimensjoner | Rader |
|---|---|---|
| `husbanken_bostotte_oslo_manedlig.csv` | år × måned | 199 |
| `husbanken_bostotte_oslo_bydel_manedlig.csv` | bydel × år × måned | 3 022 |
| `husbanken_bostotte_oslo_brukergruppe_manedlig.csv` | brukergruppe × år × måned | 995 |
| `husbanken_bostotte_nasjonalt_manedlig.csv` | år × måned | 199 |
| `husbanken_bostotte_nasjonalt_brukergruppe_manedlig.csv` | brukergruppe × år × måned | 995 |

Kolonner (alle filer): `ant_husstander_utbetaling` (hovedserien: husstander med utbetalt bostøtte, innvilget, per **utbetalingsmåned**), `ant_husstander_termin` (per **terminmåned** = måneden vedtaket gjelder), `ant_soknader`, `ant_avslag`, `utbetalt_belop`, `gjsnitt_bostotte`, `gjsnitt_inntekt_mnd`, `gjsnitt_boutgift_mnd`, `ant_over_tak` (husstander med boutgifter over taket).

Set-uttrykkene bak målene (fra appens datamodell, rå uten prikkings-if):

- utbetaling: `count({<VirkemiddelKode={'BOSTØTTE'}, TypeTilstand={'Utbetaling'}, BstVedtaksutfall={'Innvilget'}>} distinct HusstandId)`
- termin: `count({<…, TypeTilstand={'Terminutbetaling'}, BostøtteVedtakTeller={1}>} distinct HusstandId)`
- beløpsmål bruker `[Beregnet bostøtte]`, inntekt/boutgift `[Samlet inntekt]/12`, `[Beregnet boutgift]/12`, tak `[Boutgift over tak]={1}`.

Brukergrupper: Eldre; Husstander med midlertidige trygdeytelser (= AAP/dagpenger m.m. — **behandlingsgruppen for 2025-skjermingen**); Husstander uten trygdeytelser; Uføre forøvrig; Unge uføre.

**Kalendermekanikk (verifisert i data):** termin *m* utbetales 20. i måned *m+1*. QA: termin(m) = utbetaling(m+1) i **198 av 198** månedspar. Siste observasjon (jul 2026) har termin=0 fordi juli-terminen ennå ikke er kjørt — sanntidskanten er reell og må håndteres med vintage-disiplin (etterkontroll mot skatteoppgjør kan revidere historikk; appen reloades daglig).

Prikking: appen prikker celler < 4 husstander (`vGrenseverdiPrikking=4`). Irrelevant på Oslo-/bydels-totalnivå, men relevant ved fine kryss (bydel × brukergruppe).

## 2. SSB-serier (PxWeb-API v0, `data.ssb.no`) — `scripts/fetch_ssb.py`

| Tabell | Innhold | Frekvens/dekning | Fil (data/clean/) |
|---|---|---|---|
| 09895 | Leiemarkedsundersøkelsen: mnd-leie og kr/kvm, prissone × rom (sone 01 = Oslo og Bærum + hele landet) | årlig 2012–2025 | `ssb_09895_leiemarked_oslo.csv` |
| 03013 | KPI etter konsumgruppe (2015=100): totalindeks, 04 bolig, 04.1/04.1.1/04.1.2 betalt husleie | mnd 1979M01–2025M12 (avsluttet) | `ssb_03013_kpi_husleie.csv` |
| 14710 | KPI historisk totalindeks (2025=100) — bro inn i 2026 | mnd 1920M03–2026M06 | `ssb_14710_kpi_totalindeks.csv` |
| 01222 | Befolkningsendringer i kvartalet, Oslo (0301): folketall, fødte, flytting m.m. | kvartal 1997K4–2026K1 | `ssb_01222_befolkning_oslo_kvartal.csv` |

QA: LMU 2-roms Oslo/Bærum 2025 = **15 260 kr/mnd** — reprodusert eksakt (tallet brukt i innledningen).

## 3. Oslo kommunes statistikkbank (PxWeb-API) — `scripts/fetch_oslo_statbank.py`

Base: `https://statistikkbanken.oslo.kommune.no/statbank/api/v1/no/db1/`. Bydelsnivå, årlige — kovariater/tverrsnitt til bydelsanalysen (D-designene):

| Tabell | Innhold | Fil (data/clean/) |
|---|---|---|
| SOS001 | AAP-mottakere per bydel 2012–2024 | `oslo_sos001_aap_bydel.csv` |
| SOS006 | Uføretrygdmottakere per bydel 2004–2024 | `oslo_sos006_uforetrygd_bydel.csv` |
| STØ013 | Sosialhjelpsmottakere og berørte per bydel 2005–2023 | `oslo_sto013_sosialhjelp_bydel.csv` |
| STØ020 | Antall/andel sosialhjelpsmottakere i befolkningen per bydel 2007–2023 | `oslo_sto020_sosialhjelp_andel_bydel.csv` |
| BEF004 | Folkemengde per bydel og alder 2008–2019 | `oslo_bef004_folkemengde_bydel.csv` |
| BEF005 | Folkemengde per bydel og alder 2017–2026 | `oslo_bef005_folkemengde_bydel.csv` |
| BEF036 | Befolkningsframskriving 2025–2050 (MMM, alle aldre) — delbydelsnivå aggregert til bydel via kodestrukturen (områdekode // 100 = bydelsnr), med Husbanken-kommunenr som koblingsnøkkel | `oslo_bef036_framskriving_bydel.csv` (+ `_omrade.csv` for delbydel) |

Merk: HUS001 (husholdninger) og BOF001 (eierstatus) finnes kun på delbydels-/grunnkretsnivå med navnekollisjoner mot bydelsnavn — parkert; kan aggregeres samme vei som BEF036 ved behov. Bydelsnevnere dekkes av BEF004/BEF005.

## 4. Intervensjonstabell og regelparametre (kuratert fra primærkilder)

- `data/clean/intervensjonstabell.csv` — 20 hendelser 2020–2026 med termin-/utbetalingsdatoer, mekanisme, forventet retning, kilde og verifiseringsstatus. Primærkilde: Husbankens årsrapporter 2021–2025 (PDF-ene ligger i `data/raw/`, tekstversjoner ved siden av).
- `data/clean/regelparametre_gjeldende.csv` — regelmotorens parametre: dekningsgrad 73,7 %, boutgiftstak per husstandsstørrelse (Oslo-tillegg +27 982), egenandelsformel (min 26 576; 16,44 % > 137 462; 63,56 % > 245 278; egne grenser for unge uføre og enslige pensjonister), vekting 1,0/0,13/0,15, minsteutbetaling 63 kr, utbetaling 20. hver måned, prisjustering 1. juni årlig (+ prosentene 2023–2025), midlertidig progressivt ledd 0,28 % → 0,12 %.
- `data/clean/stromstotte_manedlig.csv` — ekstra strømutbetalinger per utbetalingsmåned 2021–2024 (beløp + tillegg per medlem + geografi).
- `data/clean/arsrapport_nokkeltall.csv` — publiserte nasjonale årstall 2021–2025 fra Husbankens årsrapport 2025, tabell 3.1 (unike husstander gjennom året, utbetalt bostøtte, utbetalt strømstøtte). Kuratert for ekstern validering av Qlik-uttrekket: årssummen av `utbetalt_belop` treffer det publiserte beløpet innenfor 2,1 % i alle fem år, med et ensidig negativt avvik fra 2022 som er konsistent med etterkontroll mot skatteoppgjøret.
- `data/clean/forhandsanslag.csv` — daterte effektanslag per intervensjon (åtte rader), skilt etter om anslaget er publisert *før* hendelsen, etterberegnet, eller utledet av regelmekanikken. Grunnlaget for modell M7, som pålegger effektstørrelsen der regressoren ikke kan estimeres. **Kjent hull:** høstpakken 2024 (I14/I15/I16) har bare kronebeløp i årsrapporten; husstandstall bør hentes fra Prop. 1 S / RNB 2024.
- `data/clean/grunnbelop_historisk.csv` — folketrygdens grunnbeløp 2010–2026 (virkningsdato 1. mai + kalenderårssnitt; 2026-G = 136 549). Driver minsteytelsene → inntektsgrunnlaget; mai-regulering + juni-prisjustering av bostøttesatsene gir to regelverksbestemte sesongpunkter. Kilde: nav.no/grunnbelopet. NB 2020: oppgjøret utsatt til høsten, tilbakevirkende fra 1. mai.

Nøkkelrevisjoner mot tidligere notater (H3-prioren):

1. Strøm-ekstrautbetalinger startet allerede **mars 2021** (2 950 + 120, nasjonalt), med en ren **Sør-Norge-runde november 2021** (geografisk differensiert — Oslo inkludert).
2. Det midlertidige vinduet er presist: **redusert progressivt egenandelsledd 0,28 % → 0,12 % fra utbetalingen januar 2022 t.o.m. utbetalingen april 2024**; ~25 000 husstander nasjonalt mistet retten ved avviklingen (termin april 2024).
3. **Oppvarmingstillegget til alle kom 1. september 2024** — ikke 1. oktober som tidligere notert. 1. oktober 2024 = 18/19-åringers inntekt ut.
4. Prisjusteringen skjer **1. juni** hvert år (2017-modellen) — sesongleddet i regelverket ligger altså i juni, med kjente prosenter: 2023: tak +2,5 %; 2024: tak +4,2 %/egenandel +4,7 %; 2025: tak +2,7 %/egenandel +4,1 %.
5. 2025-skjermingen (2/3-medregning i tre-utbetalingsmåneder) er **empirisk synlig**: snittlig |måned-til-måned-endring| for «midlertidige trygdeytelser» nasjonalt falt fra 3 986 (2024) til 1 006 (2025).

## 5. Nasjonale årstall per trygdegruppe

Husbankens årsrapport 2025, tabell 3.16 (2021–2025): søkere, mottakere, utbetalt, snittbeløp/boutgift/inntekt, andel over tak, antall husstander med uføretrygd/alderspensjon/AAP/dagpenger/introduksjonsstønad/inntekt < 50 000. Ligger i PDF-/tekstfilene (`husbanken_arsrapport_2025.txt`, søk «Tabell 3.16»); brukes som kryssjekk mot Qlik-uttrekkene.

## 6. Kjente hull (bevisste, ikke blokkerende)

1. **NAV månedsserier per kommune (AAP155 m.fl.)**: nav.no blokkerer nedlasting fra denne sandkassen (TLS-reset). Filene finnes som xlsx — «AAP155 Mottakere av arbeidsavklaringspenger. Kommune. Tidsserie måned» på nav.no-statistikksidene — og kan lastes ned manuelt ved behov. Behovet er redusert: behandlingsgruppens månedsserie ligger allerede i brukergruppe-uttrekket, og bydels-AAP årlig ligger i SOS001.
2. **Strømbeløpene jan–apr 2024**: måneder bekreftet i årsrapporten, beløp (trolig 1 500 + 150) må bekreftes i Prop. 1 S (2023–2024) KDD. Flagget «delvis» i tabellene.
3. **Meldekort-regressoren** (hvilke kalendermåneder som er tre-utbetalingsmåneder): månedene flytter per person med 14-dagerssyklusen; regressoren bør konstrueres empirisk fra brukergruppeserien (volatilitetsfallet gir identifikasjon) eller beregnes fra 14-dagersgrid med forankringsdato. Ikke en datafil, men et byggesteg.
4. **Juni 2026-justeringsprosenten** er ikke publisert i årsrapport ennå; gjeldende satser (per veileder oppdatert 29.06.2026) ligger i parameterfila.
5. Lovdata er robots-stengt for maskinell henting; forskriftssatser er derfor belagt via Husbankens regelverksveileder (samme innhold, løpende oppdatert).

## 7. Reproduserbarhet

`scripts/qlik_engine.py` (Engine-klient), `extract_bostotte_v2.py` (kjerneuttrekk), `fetch_ssb.py`, `fetch_oslo_statbank.py`. Kartleggingsskriptene fra byggedagen (`explore_app.py`, `explore_vars.py`, `debug_kommune.py`) ligger i `scripts/utforsking/`; de er ikke del av uttrekksløypa, men dokumenterer hvordan datamodellen ble kartlagt. Alle er kjørbare på nytt; Qlik-appen reloades daglig, så en re-kjøring gir ferskeste vintage.
