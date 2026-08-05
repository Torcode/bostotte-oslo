"""Trekk ut bostøtte-månedsserier fra Husbankens statistikkbank (Qlik Engine API).

Serier per (År, Månedsnr), for Oslo og nasjonalt:
  - ant_husstander_utbetaling : husstander med utbetalt bostøtte (utbetalingsmåned)
  - ant_husstander_termin     : husstander med terminutbetaling/vedtak (terminmåned)
  - ant_soknader              : husstander som søkte (søknadsmåned)
  - ant_avslag                : husstander med avslag
  - utbetalt_belop            : sum beregnet bostøtte (utbetaling)
  - gjsnitt_bostotte          : snitt beregnet bostøtte per husstand (utbetaling)
  - gjsnitt_inntekt_mnd       : snitt samlet inntekt/12 (utbetaling)
  - gjsnitt_boutgift_mnd      : snitt beregnet boutgift/12 (utbetaling)
  - ant_over_tak              : husstander med boutgift over tak (utbetaling)

NB: Prikkingsregelen (vGrenseverdiPrikking=4) er irrelevant på Oslo-/nasjonsnivå,
og vi bruker rå set-uttrykk uten formaterings-if.
"""
import csv
import json
import sys

from qlik_engine import QlikEngine

BST = "VirkemiddelKode={'BOSTØTTE'}"

MEASURES = [
    ("ant_husstander_utbetaling",
     f"count({{<{BST}, TypeTilstand={{'Utbetaling'}}, BstVedtaksutfall={{'Innvilget'}}>}} distinct HusstandId)"),
    ("ant_husstander_termin",
     f"count({{<{BST}, TypeTilstand={{'Terminutbetaling'}}, BostøtteVedtakTeller={{1}}>}} distinct HusstandId)"),
    ("ant_soknader",
     f"count({{<{BST}, TypeTilstand={{'Søknad'}}, BostøtteSøknadTeller={{1}}>}} distinct HusstandId)"),
    ("ant_avslag",
     f"count({{<{BST}, TypeTilstand={{'Avslag'}}, BostøtteAvslagTeller={{1}}>}} distinct HusstandId)"),
    ("utbetalt_belop",
     f"Sum({{<{BST}, TypeTilstand={{'Utbetaling'}}, BostøtteUtbetalingTeller={{1}}>}} [Beregnet bostøtte])"),
    ("gjsnitt_bostotte",
     f"Avg({{<{BST}, TypeTilstand={{'Utbetaling'}}, BostøtteUtbetalingTeller={{1}}>}} [Beregnet bostøtte])"),
    ("gjsnitt_inntekt_mnd",
     f"Avg({{<{BST}, TypeTilstand={{'Utbetaling'}}, BostøtteUtbetalingTeller={{1}}>}} [Samlet inntekt]/12)"),
    ("gjsnitt_boutgift_mnd",
     f"Avg({{<{BST}, TypeTilstand={{'Utbetaling'}}, BostøtteUtbetalingTeller={{1}}>}} [Beregnet boutgift]/12)"),
    ("ant_over_tak",
     f"count({{<{BST}, TypeTilstand={{'Utbetaling'}}, BostøtteUtbetalingTeller={{1}}, [Boutgift over tak]={{1}}>}} distinct HusstandId)"),
]


def select_kommune(eng, app_handle, kommune):
    """Velg kommune-feltverdi (f.eks. 'Oslo')."""
    r = eng.call("GetField", app_handle, {"qFieldName": "Kommune"})
    fh = r["qReturn"]["qHandle"]
    ok = eng.call("SelectValues", fh, {
        "qFieldValues": [{"qText": kommune, "qIsNumeric": False, "qNumber": 0}],
        "qToggleMode": False,
    })
    return ok


def fetch_cube(eng, app_handle, label):
    cube_def = {
        "qInfo": {"qType": "datacube"},
        "qHyperCubeDef": {
            "qDimensions": [
                {"qDef": {"qFieldDefs": ["År"], "qSortCriterias": [{"qSortByNumeric": 1}]}},
                {"qDef": {"qFieldDefs": ["Månedsnr"], "qSortCriterias": [{"qSortByNumeric": 1}]}},
            ],
            "qMeasures": [{"qDef": {"qDef": expr, "qLabel": name}} for name, expr in MEASURES],
            "qInitialDataFetch": [{"qTop": 0, "qLeft": 0, "qWidth": 2 + len(MEASURES), "qHeight": 800}],
            "qSuppressZero": False,
            "qSuppressMissing": True,
            "qInterColumnSortOrder": [0, 1],
        },
    }
    r = eng.call("CreateSessionObject", app_handle, [cube_def])
    ch = r["qReturn"]["qHandle"]
    layout = eng.call("GetLayout", ch)
    hc = layout["qLayout"]["qHyperCube"]
    size = hc["qSize"]
    pages = hc["qDataPages"]
    rows = []
    for p in pages:
        rows.extend(p["qMatrix"])
    # Hent evt. resterende sider
    while len(rows) < size["qcy"]:
        r2 = eng.call("GetHyperCubeData", ch, ["/qHyperCubeDef", [{
            "qTop": len(rows), "qLeft": 0, "qWidth": size["qcx"], "qHeight": min(800, size["qcy"] - len(rows)),
        }]])
        for p in r2["qDataPages"]:
            rows.extend(p["qMatrix"])
    print(f"[{label}] {size['qcy']} rader x {size['qcx']} kolonner")
    out = []
    for row in rows:
        aar = row[0].get("qNum")
        mnd = row[1].get("qNum")
        vals = [c.get("qNum") if c.get("qNum") not in ("NaN",) else None for c in row[2:]]
        out.append([aar, mnd] + vals)
    eng.call("DestroySessionObject", app_handle, [layout["qLayout"]["qInfo"]["qId"]])
    return out


def write_csv(path, rows, geo):
    header = ["aar", "manedsnr"] + [name for name, _ in MEASURES]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header + ["geo"])
        for r in rows:
            vals = ["" if v is None else (int(v) if isinstance(v, (int, float)) and float(v).is_integer() else round(v, 2)) for v in r]
            w.writerow(vals + [geo])
    print(f"  -> {path}")


if __name__ == "__main__":
    eng = QlikEngine()
    h = eng.open_doc()

    # 1) Nasjonalt (ingen selection)
    nat = fetch_cube(eng, h, "Nasjonalt")
    write_csv("../data/raw/husbanken_bostotte_nasjonalt_manedlig.csv", nat, "Norge")

    # 2) Oslo
    select_kommune(eng, h, "Oslo")
    oslo = fetch_cube(eng, h, "Oslo")
    write_csv("../data/raw/husbanken_bostotte_oslo_manedlig.csv", oslo, "Oslo")

    eng.close()
    print("Ferdig.")
