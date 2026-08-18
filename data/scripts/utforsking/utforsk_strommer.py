"""Datasjekk: kan statistikkbanken skille innganger fra avganger i
mottakerbeholdningen for Oslo, månedlig?

Kjøres mot samme Qlik-app som uttrekket (se qlik_engine.py). Skriptet er
lesende: det endrer ingenting i den frosne datapakken, og skriver all
dokumentasjon til stdout. Funnene er sammenfattet med tall i
data/docs/datasjekk_brutto_strommer.md; dette skriptet er belegget som lar
hvem som helst regenerere dem.

Kjerneidéen i steg 4: Qlik-elementfunksjonen P() gir mengden husstander som
var innvilget i forrige termin, slik at overleverne mellom to terminer kan
telles direkte. Da følger begge bruttostrømmene av regnskapet
    innganger_t = beholdning_t − overlevere_t
    avganger_t  = beholdning_{t−1} − overlevere_t
uten tilgang til mikrodata.

Bruk:
    python utforsk_strommer.py            # hele beleggskjeden, ~2 min
"""
import re
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from qlik_engine import QlikEngine

BST = "VirkemiddelKode={'BOSTØTTE'}"
TRM = "TypeTilstand={'Terminutbetaling'}, BostøtteVedtakTeller={1}"
AVS = "TypeTilstand={'Avslag'}, BostøtteAvslagTeller={1}"

# Månedspar for P()-dekomponeringen: avviklingsterminen april 2024 med
# måneden etter, to meldekortsommere, og siste komplette termin.
PAR = [(2024, 3, 2024, 4), (2024, 4, 2024, 5), (2025, 5, 2025, 6),
       (2025, 6, 2025, 7), (2026, 5, 2026, 6)]


def kube(eng, h, dims, measures, hoyde=1200):
    """Hent en hyperkube som liste av rader [dimtekster..., måltall...]."""
    width = len(dims) + len(measures)
    r = eng.call("CreateSessionObject", h, [{
        "qInfo": {"qType": "datasjekk"},
        "qHyperCubeDef": {
            "qDimensions": [{"qDef": {"qFieldDefs": [d], "qSortCriterias": [{"qSortByNumeric": 1}]}} for d in dims],
            "qMeasures": [{"qDef": {"qDef": m}} for m in measures],
            "qInitialDataFetch": [{"qTop": 0, "qLeft": 0, "qWidth": width, "qHeight": hoyde}],
            "qSuppressMissing": True,
            "qInterColumnSortOrder": list(range(len(dims))),
        },
    }])
    hc = eng.call("GetLayout", r["qReturn"]["qHandle"])["qLayout"]["qHyperCube"]
    rader = []
    for p in hc["qDataPages"]:
        for row in p["qMatrix"]:
            rader.append([c.get("qNum") if isinstance(c.get("qNum"), (int, float)) else c.get("qText") for c in row])
    return rader


def tall(eng, h, expr):
    return kube(eng, h, [], [expr], hoyde=1)[0][0]


def main():
    eng = QlikEngine()
    h = eng.open_doc()

    # ---- 1. Feltinventar: hvilke felter i datamodellen angår strømmer ----
    r = eng.call("GetTablesAndKeys", h, [{"qcx": 1000, "qcy": 1000}, {"qcx": 0, "qcy": 0}, 30, True, False])
    monster = re.compile(r"vedtak|s.knad|avslag|tilstand|utfall|f.rste|teller", re.I)
    print("=== 1. Strømrelevante felter per tabell ===")
    for t in r.get("qtr", []):
        treff = [f["qName"] for f in t.get("qFields", []) if monster.search(f["qName"])]
        if treff:
            print(f"[{t['qName']}] ({t.get('qNoOfRows')} rader): {', '.join(treff)}")

    # ---- 2. Verdiomfang for tilstand, utfall og førstegangsflagget ----
    print("\n=== 2. TypeTilstand × BstVedtaksutfall (distinkte husstander, bostøtte, alle år) ===")
    for rad in kube(eng, h, ["TypeTilstand", "BstVedtaksutfall"], [f"count({{<{BST}>}} distinct HusstandId)"], hoyde=20):
        print(rad)
    print("\n=== 2b. Førstegangs søknad (verdier og masse) ===")
    for rad in kube(eng, h, ["Førstegangs søknad"],
                    [f"count({{<{BST}, TypeTilstand={{'Søknad'}}, BostøtteSøknadTeller={{1}}>}} distinct HusstandId)"], hoyde=5):
        print(rad)

    # ---- Fylke = Oslo for resten av kjøringen (som i extract_bostotte_v2) ----
    r = eng.call("GetField", h, {"qFieldName": "Fylke"})
    eng.call("SelectValues", r["qReturn"]["qHandle"],
             {"qFieldValues": [{"qText": "Oslo", "qIsNumeric": False, "qNumber": 0}], "qToggleMode": False})

    # ---- 3. Oslo månedlig: nivå og identiteter ----
    M = [
        ("beholdning_termin", f"count({{<{BST}, {TRM}>}} distinct HusstandId)"),
        ("soknader", f"count({{<{BST}, TypeTilstand={{'Søknad'}}, BostøtteSøknadTeller={{1}}>}} distinct HusstandId)"),
        ("innvilgede", f"count({{<{BST}, TypeTilstand={{'Søknad'}}, BostøtteSøknadTeller={{1}}, BstVedtaksutfall={{'Innvilget'}}>}} distinct HusstandId)"),
        ("innvilgede_forstegang", f"count({{<{BST}, TypeTilstand={{'Søknad'}}, BostøtteSøknadTeller={{1}}, BstVedtaksutfall={{'Innvilget'}}, [Førstegangs søknad]={{1}}>}} distinct HusstandId)"),
        ("avslag", f"count({{<{BST}, {AVS}>}} distinct HusstandId)"),
        ("utbetaling", f"count({{<{BST}, TypeTilstand={{'Utbetaling'}}, BstVedtaksutfall={{'Innvilget'}}>}} distinct HusstandId)"),
    ]
    rader = kube(eng, h, ["År", "Månedsnr"], [expr for _, expr in M])
    serie = [r_ for r_ in rader if isinstance(r_[0], (int, float)) and r_[2] and r_[2] > 0]
    print(f"\n=== 3. Oslo månedlig, {len(serie)} måneder med terminkjøring "
          f"({int(serie[0][0])}m{int(serie[0][1]):02d}–{int(serie[-1][0])}m{int(serie[-1][1]):02d}) ===")
    print("identitetskontroller over alle måneder:")
    avvik_sok = [f"{int(r_[0])}m{int(r_[1]):02d}" for r_ in serie if abs(r_[3] - (r_[4] + r_[6])) > 0.5]
    print(f"  søknader = innvilgede + avslag brutt i {len(avvik_sok)} måneder {avvik_sok[:5]}")
    etter2017 = [(serie[i], serie[i + 1]) for i in range(len(serie) - 1) if serie[i][0] >= 2017]
    avvik_utb = [f"{int(n[0])}m{int(n[1]):02d}" for f_, n in etter2017 if n[7] and abs(n[7] - f_[4]) > 0.5]
    print(f"  utbetaling_t = innvilgede_(t−1) fra 2017: brutt i {len(avvik_utb)} måneder {avvik_utb[:5]}")
    print("siste 12 måneder (år, mnd, beholdning, søknader, innvilgede, førstegang, avslag):")
    for r_ in serie[-12:]:
        print("  ", [int(x) if isinstance(x, float) else x for x in r_[:7]])

    # ---- 4. P()-dekomponering: observerte bruttostrømmer for utvalgte terminpar ----
    print("\n=== 4. Observerte bruttostrømmer via P() (Oslo) ===")
    print(f"{'termin':>8} {'beh t':>7} {'beh t-1':>8} {'overlev':>8} {'inng':>6} {'avg':>6} {'førstegang':>10}")
    for (y0, m0, y1, m1) in PAR:
        s0 = f"År={{{y0}}}, Månedsnr={{{m0}}}, {BST}, {TRM}"
        s1 = f"År={{{y1}}}, Månedsnr={{{m1}}}, {BST}, {TRM}"
        b0 = tall(eng, h, f"count({{<{s0}>}} distinct HusstandId)")
        b1_ = tall(eng, h, f"count({{<{s1}>}} distinct HusstandId)")
        over = tall(eng, h, f"count({{<{s1}, HusstandId=P({{<{s0}>}} HusstandId)>}} distinct HusstandId)")
        forste = tall(eng, h, f"count({{<{s1}, [Førstegangs søknad]={{1}}>}} distinct HusstandId)")
        print(f"{y1}m{m1:02d} {b1_:7.0f} {b0:8.0f} {over:8.0f} {b1_ - over:6.0f} {b0 - over:6.0f} {forste:10.0f}")

    # ---- 5. Meldekortmånedene: avslagene er gjentakssaker ----
    print("\n=== 5. Avslag: gjentak (løpende sak) vs førstegang (Oslo) ===")
    for (y, m) in [(2025, 5), (2025, 6), (2025, 7), (2026, 5), (2026, 6)]:
        T = f"År={{{y}}}, Månedsnr={{{m}}}, {BST}, {AVS}"
        tot = tall(eng, h, f"count({{<{T}>}} distinct HusstandId)")
        gjen = tall(eng, h, f"count({{<{T}, [Førstegangs søknad]={{0}}>}} distinct HusstandId)")
        print(f"  {y}m{m:02d}: avslag {tot:.0f}, herav gjentak {gjen:.0f}")

    # ---- 6. Avslagsgrunn (Vedtakskode) er koblet til bostøttefakta ----
    print("\n=== 6. Avslagsgrunner (Vedtakskode), Oslo 2025 ===")
    rader = kube(eng, h, ["Vedtakskode"],
                 [f"count({{<{BST}, {AVS}, År={{2025}}>}} distinct HusstandId)"], hoyde=40)
    for r_ in sorted((x for x in rader if isinstance(x[1], (int, float)) and x[1] > 0),
                     key=lambda x: -x[1]):
        print(f"  {r_[0]}: {r_[1]:.0f}")
    print("dominerende grunn i meldekortmånedene (mai → juni 2025 og 2026):")
    for (y, m) in [(2025, 5), (2025, 6), (2026, 5), (2026, 6)]:
        n = tall(eng, h, f"count({{<{BST}, {AVS}, År={{{y}}}, Månedsnr={{{m}}}, "
                         f"Vedtakskode={{'For høy inntekt ift boutgift'}}>}} distinct HusstandId)")
        print(f"  {y}m{m:02d}: avslag med grunn «For høy inntekt ift boutgift»: {n:.0f}")

    eng.close()


if __name__ == "__main__":
    main()
