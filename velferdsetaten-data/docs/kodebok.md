# Kodebok — Velferdsprosjektet

Variabelnivå-dokumentasjon for alle 21 datasett i `last_alt()` pluss de konstruerte variablene i analysesettet. Kildenivå-dokumentasjon (URL-er, uttrekksmetode, hull) ligger i `datakilder.md`; denne fila svarer på «hva betyr hver kolonne». Generert og verifisert mot pakken 4. august 2026.

## 0. Lesenøkkel

**To kalendre.** `ant_husstander_termin` i rad for måned *m* er terminen (rettighetsmåneden) *m*; `ant_husstander_utbetaling` i samme rad er utbetalinger i kalendermåned *m*, som gjelder termin *m−1* (utbetalt den 20.). Identiteten termin(m) = utbetaling(m+1) holder i alle 198 månedspar. Siste rad har termin = 0 til terminkjøringen er gjort (sanntidskant) — dette er «ikke kjørt ennå», ikke null mottakere.

**Prikking.** Kilden prikker celler < 4 husstander. Forekommer ikke på nivåene i pakken (Oslo, 15 bydeler, 5 brukergrupper, nasjonalt), men ville truffet finere kryss.

**Vintage.** Statistikkbanken reloades hver natt og revideres bakover ved etterkontroll mot skatteoppgjøret. Uttrekksdato for pakken: 4. august 2026 (reload 05:33 UTC).

## 1. Kjerneserier — Husbanken (5 objekter)

`oslo` (199×13), `nasjonalt` (199×13), `oslo_bydel` (3 022×14), `brukergruppe` (995×14), `nasjonalt_brukergruppe` (995×14). Månedlig 2010m1–2026m7. Felles kolonneskjema:

| Kolonne | Type | Definisjon (Qlik-mål i kursiv) |
|---|---|---|
| `dato` | Date | Første dag i måneden (konstruert av loaderen fra aar × manedsnr) |
| `aar`, `manedsnr` | num | Kalenderår, måned 1–12 |
| `ant_husstander_utbetaling` | num | Husstander med utbetalt bostøtte i måneden: *count(distinct HusstandId), TypeTilstand=Utbetaling, BstVedtaksutfall=Innvilget* |
| `ant_husstander_termin` | num | Husstander med terminvedtak for måneden: *count(distinct HusstandId), TypeTilstand=Terminutbetaling, BostøtteVedtakTeller=1* |
| `ant_soknader` | num | Husstander i terminbehandlingen (inkl. maskinell videreføring av løpende saker) — IKKE nye søknader; *TypeTilstand=Søknad* |
| `ant_avslag` | num | Husstander med avslag i måneden; *TypeTilstand=Avslag* |
| `utbetalt_belop` | num | Sum beregnet bostøtte, kr (utbetalingskalender) |
| `gjsnitt_bostotte` | num | Snitt beregnet bostøtte per husstand, kr/mnd |
| `gjsnitt_inntekt_mnd` | num | Snitt samlet inntekt/12 per husstand, kr/mnd |
| `gjsnitt_boutgift_mnd` | num | Snitt beregnet boutgift/12 per husstand, kr/mnd |
| `ant_over_tak` | num | Husstander med boutgifter over boutgiftstaket (utbetalingskalender) |
| `geo` | chr | "Oslo" / "Norge" (ikke i `oslo_bydel`) |

Snittkolonnene er tomme (NA) i måneder uten utbetalinger (typisk januar 2010 og sanntidskanten).

**`oslo_bydel` i tillegg:** `kommunenr` (chr, behold ledende null!) og `bydel`. Nøkkel: kommunenr = 310 + bydelsnr → 0311 Gamle Oslo, 0312 Grunerløkka (kilden skriver navnet uten omlyd — bruk kildens skrivemåte ved join, normalisér først ved presentasjon), 0313 Sagene, 0314 St. Hanshaugen, 0315 Frogner, 0316 Ullern, 0317 Vestre Aker, 0318 Nordre Aker, 0319 Bjerke, 0320 Grorud, 0321 Stovner, 0322 Alna, 0323 Østensjø, 0324 Nordstrand, 0325 Søndre Nordstrand. **0301 er en nesten tom restkategori (0–3 husstander) — aldri bruk den som Oslo-total**; i metodekapitlet beholdes den som «Ufordelt (0301)» så hierarkiet summerer eksakt.

**`brukergruppe`-verdiene (5, summerer eksakt til total):** Eldre · Unge uføre · Uføre forøvrig · Husstander med midlertidige trygdeytelser (= AAP/dagpenger m.m. — skjermingens behandlingsgruppe, ca. 1/3 av Oslo-mottakerne) · Husstander uten trygdeytelser.

## 2. SSB-tabeller (4 objekter)

Felles PxWeb-skjema: én rad per celle, `*_kode`-kolonner (alltid tekst — «01» skal ikke bli 1), `*_navn`-kolonner, `verdi` (num) og `dato` (parset av loaderen fra Tid_kode: ÅÅÅÅ / ÅÅÅÅMnn / ÅÅÅÅKn → første dag i perioden).

**`leiemarked`** (280×10, årlig 2012–2025) — LMU. `Soner2_kode`: 00 = Hele landet, **01 = Oslo og Bærum**, 03/04/05 = Bergen/Trondheim/Stavanger, 20/21/22 = tettstedsgrupper. `AntRom_kode` 1–5 (5 = «5 rom eller flere»). `ContentsCode_kode` = "Husleie" gir gjennomsnittlig månedlig leie (kr); den andre serien (årlig leie per kvm) identifiseres via `ContentsCode_navn`. Oppskrift brukt i metode: `Soner2_kode=="01", AntRom_kode=="2", ContentsCode_kode=="Husleie"` → 15 260 kr i 2025.

**`kpi_husleie`** (11 280×8, månedlig 1979m1–2025m12, avsluttet serie 2015=100). `Konsumgrp_kode`: TOTAL, 04 (bolig/lys/brensel), **04.1 (betalt husleie)**, 04.1.1, 04.1.2. Fire innholdsserier per gruppe — bruk `ContentsCode_kode=="KpiIndMnd"` for indeksnivået (de andre er endringsrater/årssnitt).

**`kpi_total`** (1 276×6, månedlig 1920m3–2026m6, 2025=100) — broen inn i 2026 etter basisskiftet. Samme filter: `ContentsCode_kode=="KpiIndMnd"`.

**`befolkning_oslo`** (1 254×8, kvartalsvis 1997K4–2026K1, Region 0301). Elleve innholdsserier (fødte, døde, flyttinger, …); nivåserien brukt i metode er `ContentsCode_kode=="Folketallet1"` (befolkning ved inngangen av kvartalet), lineærinterpolert til måned i chunk `met-kovariater`.

## 3. Oslo kommunes statistikkbank (7 objekter)

Felles skjema som SSB, men to feller: (i) `*_kode`-kolonnene er posisjonsindekser fra API-et — **bruk `*_navn`-kolonnene**; (ii) `ContentsCode_kode` = "EliminatedValue" er normalt (eliminert dimensjon). Loaderen legger `aar` (int) forrest, lest fra år-navnkolonnen. Geografikolonnen HETER ULIKT per tabell:

| Objekt | Dekning | Geografikolonne | Øvrige dimensjoner | Verdi |
|---|---|---|---|---|
| `aap_bydel` | 2012–2024 | `geografi_navn` | kjønn, aldersgruppe | antall AAP-mottakere |
| `ufore_bydel` | 2004–2024 | `bosted_navn` | kjønn, aldersgruppe | antall uføretrygdede |
| `sosialhjelp_bydel` | 2005–2023 | `bydel_navn` | mottakere/berørte-kategori | antall |
| `sosialhjelp_andel_bydel` | 2007–2023 | `geografi_navn` | alder, to statistikkvariabler | antall og andel (%) |
| `folkemengde_bydel_0819` | 2008–2019 | `Geografi_navn` | Aldersgrupper | folkemengde per bydel |
| `folkemengde_bydel_1726` | 2017–2026 | `bosted_navn` | aldersgruppe | folkemengde per bydel |
| `framskriving_bydel` | 2025–2050 | `bydel` (+ `bydel_nr`, `husbanken_kommunenr`) | — (MMM, alle aldre) | `framskrevet_folkemengde_mmm` |

Geografiverdiene inkluderer «Oslo i alt» + bydelsnavn; totalrader må filtreres bort før bydelsanalyse. `framskriving_bydel` er ferdig aggregert fra delbydel (områdekode // 100 = bydelsnr) og joiner rett på kjerneseriene via `husbanken_kommunenr`; bydel 16 (Sentrum) og 17 (Marka) mangler Husbanken-motpart (tom nøkkel).

## 4. Kuraterte regelverkstabeller (4 objekter)

**`intervensjoner`** (20×14). Kolonner: `id` (I01–I20), `dato_virkning`/`termin_fra`/`termin_til`/`utbetaling_fra`/`utbetaling_til` (Date, første i måneden; NA = åpen/ikke relevant), `hendelse`, `type` (vindu/trinn/beløp/parameter/kalender), `mekanisme` (fritekst med tall), `forventet_effekt_antall`/`_belop` (opp/ned/nøytral/ingen), `geografi`, `kilde`, `verifisering` (bekreftet/delvis). Hendelsene i kortform: I01 covid-vindu 2020m4–m10 · I02/I03/I04 engangs strøm 2021 (mars nasjonalt; november kun Sør-Norge inkl. Oslo; desember nasjonalt) · **I05 strømvinduet termin 2021m12–2024m3: progressivt egenandelsledd 0,28 %→0,12 %** · I06/I07 strømbeløp per måned 2022/2023 · I08 barnetillegg + vekt 0,13→0,15 (feb 2023) · I09 minstepensjonskompensasjon (mar 2023) · I10 trygdeoppgjørsskjerming juni 2023 · I11 siste strømvindu jan–apr 2024 (delvis: månedsbeløp) · **I12 vinduslukking termin april 2024 (~25 000 ut nasjonalt; −25,2 % i Oslo på én termin, termin mars → termin april)** · I13 prisjustering juni 2024 (+4,2/+4,7 %) · **I14 tak +4 000 + lineær egenandel (juli 2024)** · I15 oppvarmingstillegg til alle (sep 2024) · I16 18/19-åringers inntekt ut (okt 2024) · **I17 AAP/dagpenger-skjermingen (jan 2025)** · I18 økt minsteytelse mai 2025 (delvis) · I19 prisjustering juni 2025 (+2,7/+4,1 %) · I20 statsbudsjett 2026: ingen regelendring.

**`parametre`** (32×6). NB: `verdi` er tekstkolonne (én rad er en dato) — konverter per rad ved bruk. Gruppene: dekningsgrad (73,7 %) · boutgiftstak: 5 grunnsatser etter husstandsstørrelse (92 234–150 385 kr/år) + 4 tillegg (Oslo +27 982; storbygruppe +19 079; gruppe 3 +12 720; spesialtilpasset +5 724) · egenandel: minste 26 576; ledd 1 16,44 % over 137 462; ledd 2 63,56 % over 245 278; egne grenser unge uføre (295 795) og enslige pensjonister (148 275/256 613) · vekter 1,0/0,13/0,15 · minsteutbetaling 63 kr/mnd · utbetalingsdag 20. · meldekortregel 66,67 % · prisjustering 1. juni + prosentene 2023–2025 · midlertidig progressivt ledd 0,28/0,12 %.

**`stromstotte`** (31×9). Én rad per utbetalingsmåned 2021m3–2024m4: `dato_utbetaling` (loaderen; termin = denne minus én måned), `belop_husstand` (kr; 0 i måneder uten utbetaling), `tillegg_per_ekstra_medlem` (120 kr i 2021-engangsrundene, ellers 150), `geografi` (nasjonal / Sør-Norge inkl. Oslo), `verifisering` (jan–apr 2024 «delvis»).

**`arsrapport`** (5×7). Publiserte nasjonale årstall fra Husbankens årsrapport 2025, tabell 3.1, brukt til ekstern validering av Qlik-uttrekket. `aar` (2021–2025), `husstander_unike_aaret` (**unike** husstander gjennom året — *ikke* en månedsbeholdning og ikke direkte sammenliknbar med kjerneseriene), `utbetalt_bostotte_mill` (direkte sammenliknbar med årssummen av `utbetalt_belop`), `utbetalt_stromstotte_mill` (publisert separat, inngår ikke i beløpet over), `geografi`, `kilde`, `verifisering`.

**`grunnbelop`** (17×5). `virkningsdato` (1. mai 2010–2026), `g_belop` (75 641 → 136 549), `g_snitt_kalenderaar`, `merknad` (2020: utsatt oppgjør, tilbakevirkende).

## 5. Konstruerte variabler (analysesettet, metode 3.1–3.2)

Bygges av chunkene i metodekapitlet i `unt_1.qmd` (avsnitt 3.1–3.5); 114 rader (2017m1–2026m6) × 19 kolonner. Radtallet er ikke hardkodet i dokumentet — det utledes av estimeringsutvalget, og en ny datavintage utvider settet uten at renderingen brekker:

| Variabel | Definisjon | Rolle |
|---|---|---|
| `M`, `log_M` | `ant_husstander_termin`, log | Utfallsserien $y_t = \ln M^T_t$ |
| `soknader`, `avslag` | fra kjerneserien | strøm-/pressdiagnostikk |
| `win_covid` | 1 i termin 2020m4–2020m10 | vindu (I01) |
| `win_strom` | 1 i termin 2021m12–2024m3 | vindu (I05/I12); inn-kant forventet gradvis, ut-kant skarp |
| `step_tak`, `step_oppv`, `step_1819` | 1 fra termin 2024m7/m9/m10 | 2024-trinnene — **ikke separerbare enkeltvis**; estimeres som pakke/spike-slab |
| `step_skjerm` | 1 fra termin 2025m1 | kandidatregressor (nivåresidual av I17) |
| `strom_belop` | kr per husstand, forskjøvet til termin | kun beløpsmodeller |
| `u` | antall meldekortutbetalinger i måneden (2/3), 14-dagersgrid med **kalibrert fase** (gap −16 %, t ≈ −10; ukes-alias nest best) | kalenderkilde |
| `k_pre` | (u − 26/12) · 1{t ≤ 2024m12} | kalendereffekt før skjermingen; forventet negativ |
| `k_post` | (u − 26/12) · 1{t ≥ 2025m1} | skarp nullhypotese: 3 × ⅔ = 2 → koeffisient = 0 |
| `kpi_husleie` | 04.1-indeksen (t.o.m. 2025m12) | ML-klasse + driftsdiagnostikk |
| `N` | befolkning, kvartal→måned interpolert | rater/drift; ikke i hovedspek |

## 5b. Identiteter som holder i kildene (verifisert 5. august 2026)

Disse er testet på hele materialet og brukes som kontroller i metodekapitlet. De er også *tolkningsregler*: en identitet som holder eksakt, betyr at de to sidene ikke er uavhengig informasjon.

| Identitet | Status |
|---|---|
| `ant_soknader − ant_avslag = ant_husstander_termin` | Eksakt i alle måneder, alle nivåer (nasjonalt: ett månedspar avviker med ≤ 2, avrunding). **`ant_soknader` er derfor en lineærkombinasjon, ikke selvstendig informasjon.** |
| `utbetalt_belop / ant_husstander_utbetaling = gjsnitt_bostotte` | Maks avvik 0,005 kr over 198 måneder |
| Bydelssum og brukergruppesum = Oslo-total | Eksakt for **alle seks** mål, ikke bare antallet |
| Oslo ≤ Norge | Holder på alle seks mål i alle måneder; Oslo-andelen er ca. 18,5 % |
| Årssum `utbetalt_belop` mot årsrapportens tabell 3.1 | Avvik 0,00 til −2,10 % (se `arsrapport`); ensidig negativt fra 2022, konsistent med etterkontroll mot skatteoppgjøret |

## 6. Vanlige feller

1. 0301 er ikke Oslo (bruk `geo=="Oslo"`-objektet eller summér bydelene + ufordelt).
2. `ant_soknader` er terminbehandlede saker, ikke nye søknader — omtal deretter.
3. Siste rad: termin = 0 er sanntidskant, fjernes før modellering (loaderen/chunken gjør det).
4. `*_kode` skal være tekst; leses filene utenom loaderen mister du ledende nuller.
5. Oslo-statbank: bruk `*_navn` + `aar`, filtrer bort «Oslo i alt»-rader før bydelsbruk.
6. `parametre$verdi` er tekst (én rad er en dato).
7. Snittkolonner er NA der antall = 0 — ikke behandl som 0.
8. Kvartals-/årskovariater er interpolert/trappet der de møter månedsserien — dokumentér valget der det brukes.
9. Bydelspanelet er ubalansert på ett punkt: node 0301 er bare til stede i måneder der den har minst én husstand (162 av 199 måneder mangler). Aggregering til Oslo-total er likevel eksakt, og det verifiseres i `tbl-kontroller`.
10. Node 0301 heter «Oslo» i kilden. Den er ikke Oslo. Metodekapitlet gir den merkelappen «Ufordelt (0301)» før bruk (vaskeinngrep V2).
11. `ant_soknader` er ikke en observasjon ved siden av utfallet — den er innvilget pluss avslag (se 5b). Å bruke den som prediktor for mottakertallet er å regressere en størrelse på seg selv.
12. Avslagsserien er ikke ledende: korrelasjonen med endringen i mottakertallet forsvinner ved to måneders lag.
13. `husstander_unike_aaret` i `arsrapport` er unike husstander gjennom året, ikke en beholdning. Forholdet til snittbeholdningen ligger stabilt på 1,4–1,6.
14. En intervensjonsregressor er null før hendelsen og kan ikke estimeres ved en prognoseopprinnelse som ligger før den. `pakke_2024h2` og `k_post` er uidentifiserbare ved henholdsvis 24 og 30 av 31 opprinnelser i protokollen.
