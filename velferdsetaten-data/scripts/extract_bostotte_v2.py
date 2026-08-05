"""Bostøtte-uttrekk v2 fra Husbankens statistikkbank (Qlik Engine API).

Funn: Oslo er kodet PER BYDEL (KommuneNr 0311 Gamle Oslo, 0312 Grünerløkka, ...).
Oslo-total = selection Fylke='Oslo'.

Uttrekk:
  1) nasjonalt        : År x Månedsnr                (ingen selection)
  2) oslo_total       : År x Månedsnr                (Fylke='Oslo')
  3) oslo_bydel       : KommuneNr x Kommune x År x Mnd (Fylke='Oslo')
  4) oslo_brukergruppe: Brukergruppe x År x Mnd      (Fylke='Oslo')
  5) nasjonalt_brukergruppe: Brukergruppe x År x Mnd (ingen selection)
"""
import csv

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


def select_field(eng, h, field, value):
    r = eng.call("GetField", h, {"qFieldName": field})
    fh = r["qReturn"]["qHandle"]
    return eng.call("SelectValues", fh, {
        "qFieldValues": [{"qText": value, "qIsNumeric": False, "qNumber": 0}],
        "qToggleMode": False,
    })


def fetch_cube(eng, h, dims, label):
    width = len(dims) + len(MEASURES)
    page_h = max(1, 9500 // width)
    cube_def = {
        "qInfo": {"qType": "datacube"},
        "qHyperCubeDef": {
            "qDimensions": [{"qDef": {"qFieldDefs": [d], "qSortCriterias": [{"qSortByNumeric": 1, "qSortByAscii": 1}]}} for d in dims],
            "qMeasures": [{"qDef": {"qDef": expr, "qLabel": name}} for name, expr in MEASURES],
            "qInitialDataFetch": [{"qTop": 0, "qLeft": 0, "qWidth": width, "qHeight": page_h}],
            "qSuppressZero": False,
            "qSuppressMissing": True,
            "qInterColumnSortOrder": list(range(len(dims))),
        },
    }
    r = eng.call("CreateSessionObject", h, [cube_def])
    ch = r["qReturn"]["qHandle"]
    layout = eng.call("GetLayout", ch)
    hc = layout["qLayout"]["qHyperCube"]
    size = hc["qSize"]
    rows = []
    for p in hc["qDataPages"]:
        rows.extend(p["qMatrix"])
    while len(rows) < size["qcy"]:
        r2 = eng.call("GetHyperCubeData", ch, ["/qHyperCubeDef", [{
            "qTop": len(rows), "qLeft": 0, "qWidth": size["qcx"], "qHeight": min(page_h, size["qcy"] - len(rows))}]])
        for p in r2["qDataPages"]:
            rows.extend(p["qMatrix"])
    print(f"[{label}] {size['qcy']} rader")
    out = []
    for row in rows:
        rec = []
        for i, d in enumerate(dims):
            cell = row[i]
            rec.append(cell.get("qText") if d in ("Kommune", "Brukergruppe", "KommuneNr") else cell.get("qNum"))
        for c in row[len(dims):]:
            v = c.get("qNum")
            rec.append(None if v in (None, "NaN") else v)
        out.append(rec)
    eng.call("DestroySessionObject", h, [layout["qLayout"]["qInfo"]["qId"]])
    return out


def write_csv(path, dims, rows, extra=None):
    header = [d.lower().replace("å", "a") for d in dims] + [m for m, _ in MEASURES]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header + (list(extra.keys()) if extra else []))
        for r in rows:
            vals = ["" if v is None else (int(v) if isinstance(v, float) and v.is_integer() else (round(v, 2) if isinstance(v, float) else v)) for v in r]
            w.writerow(vals + (list(extra.values()) if extra else []))
    print(f"  -> {path}")


if __name__ == "__main__":
    eng = QlikEngine()
    h = eng.open_doc()
    RAW = "../data/raw/"

    nat = fetch_cube(eng, h, ["År", "Månedsnr"], "nasjonalt")
    write_csv(RAW + "husbanken_bostotte_nasjonalt_manedlig.csv", ["aar", "manedsnr"], nat, {"geo": "Norge"})

    natbg = fetch_cube(eng, h, ["Brukergruppe", "År", "Månedsnr"], "nasjonalt x brukergruppe")
    write_csv(RAW + "husbanken_bostotte_nasjonalt_brukergruppe_manedlig.csv", ["brukergruppe", "aar", "manedsnr"], natbg, {"geo": "Norge"})

    select_field(eng, h, "Fylke", "Oslo")

    oslo = fetch_cube(eng, h, ["År", "Månedsnr"], "Oslo total")
    write_csv(RAW + "husbanken_bostotte_oslo_manedlig.csv", ["aar", "manedsnr"], oslo, {"geo": "Oslo"})

    bydel = fetch_cube(eng, h, ["KommuneNr", "Kommune", "År", "Månedsnr"], "Oslo x bydel")
    write_csv(RAW + "husbanken_bostotte_oslo_bydel_manedlig.csv", ["kommunenr", "bydel", "aar", "manedsnr"], bydel)

    oslobg = fetch_cube(eng, h, ["Brukergruppe", "År", "Månedsnr"], "Oslo x brukergruppe")
    write_csv(RAW + "husbanken_bostotte_oslo_brukergruppe_manedlig.csv", ["brukergruppe", "aar", "manedsnr"], oslobg, {"geo": "Oslo"})

    eng.close()
    print("Ferdig.")
