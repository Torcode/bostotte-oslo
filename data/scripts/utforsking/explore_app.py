"""Utforsk Statistikkbank-appen: felter, master-mål, og verdiomfang for bostøtte."""
import json
from qlik_engine import QlikEngine

eng = QlikEngine()
h = eng.open_doc()

# 1) Master-mål (MeasureList)
r = eng.call("CreateSessionObject", h, [{
    "qInfo": {"qType": "MeasureList"},
    "qMeasureListDef": {"qType": "measure", "qData": {"title": "/qMetaDef/title", "tags": "/qMetaDef/tags", "expression": "/qMeasure/qDef"}},
}])
mh = r["qReturn"]["qHandle"]
layout = eng.call("GetLayout", mh)
measures = layout["qLayout"]["qMeasureList"]["qItems"]
bst = [m for m in measures if (m["qData"].get("title") or "").startswith("BST")]
print(f"=== {len(measures)} master-mål totalt, {len(bst)} BST ===")
for m in bst:
    print(f"- {m['qData']['title']!r:45s} id={m['qInfo']['qId']}")
    print(f"    expr: {str(m['qData'].get('expression'))[:180]}")

# 2) Dimensjoner (DimensionList)
r = eng.call("CreateSessionObject", h, [{
    "qInfo": {"qType": "DimensionList"},
    "qDimensionListDef": {"qType": "dimension", "qData": {"title": "/qMetaDef/title", "grouping": "/qDim/qGrouping", "info": "/qDimInfos"}},
}])
dh = r["qReturn"]["qHandle"]
layout = eng.call("GetLayout", dh)
dims = layout["qLayout"]["qDimensionList"]["qItems"]
print(f"\n=== {len(dims)} master-dimensjoner ===")
for d in dims[:40]:
    print(f"- {d['qData']['title']!r} id={d['qInfo']['qId']}")

# 3) Felter i datamodellen
r = eng.call("GetTablesAndKeys", h, [{"qcx": 1000, "qcy": 1000}, {"qcx": 0, "qcy": 0}, 30, True, False])
print("\n=== tabeller/felter ===")
for t in r.get("qtr", []):
    fields = [f["qName"] for f in t.get("qFields", [])]
    print(f"[{t['qName']}] ({t.get('qNoOfRows')} rader)")
    print("   ", ", ".join(fields[:35]))

eng.close()
