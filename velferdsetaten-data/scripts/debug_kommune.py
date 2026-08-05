"""Sjekk kommune-feltverdier som matcher Oslo, med antall utbetalingshusstander bak hver."""
from qlik_engine import QlikEngine

eng = QlikEngine()
h = eng.open_doc()

cube_def = {
    "qInfo": {"qType": "datacube"},
    "qHyperCubeDef": {
        "qDimensions": [
            {"qDef": {"qFieldDefs": ["KommuneNr"]}},
            {"qDef": {"qFieldDefs": ["Kommune"]}},
            {"qDef": {"qFieldDefs": ["Fylke"]}},
        ],
        "qMeasures": [{"qDef": {"qDef": "count({<VirkemiddelKode={'BOSTØTTE'}, TypeTilstand={'Utbetaling'}, BstVedtaksutfall={'Innvilget'}, År={2025}>} distinct HusstandId)", "qLabel": "n2025"}}],
        "qInitialDataFetch": [{"qTop": 0, "qLeft": 0, "qWidth": 4, "qHeight": 2000}],
        "qSuppressZero": False,
        "qSuppressMissing": True,
    },
}
r = eng.call("CreateSessionObject", h, [cube_def])
ch = r["qReturn"]["qHandle"]
layout = eng.call("GetLayout", ch)
hc = layout["qLayout"]["qHyperCube"]
rows = []
for p in hc["qDataPages"]:
    rows.extend(p["qMatrix"])
size = hc["qSize"]
while len(rows) < size["qcy"]:
    r2 = eng.call("GetHyperCubeData", ch, ["/qHyperCubeDef", [{"qTop": len(rows), "qLeft": 0, "qWidth": size["qcx"], "qHeight": min(2000, size["qcy"] - len(rows))}]])
    for p in r2["qDataPages"]:
        rows.extend(p["qMatrix"])

print(f"{size['qcy']} kommune-rader totalt; viser alle med 'oslo' i navn/fylke + de 10 største:")
scored = []
for row in rows:
    knr, kn, fy = row[0].get("qText"), row[1].get("qText"), row[2].get("qText")
    n = row[3].get("qNum") or 0
    scored.append((n, knr, kn, fy))
    if kn and "oslo" in kn.lower():
        print(f"  MATCH: KommuneNr={knr!r} Kommune={kn!r} Fylke={fy!r} n2025={n}")
print("\nStørste 2025:")
for n, knr, kn, fy in sorted(scored, reverse=True)[:10]:
    print(f"  {n:>8.0f}  {knr} {kn} ({fy})")

eng.close()
