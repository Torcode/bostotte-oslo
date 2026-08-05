"""Hent variabeldefinisjoner (vBst*) og resten av tabellisten."""
import json
from qlik_engine import QlikEngine

eng = QlikEngine()
h = eng.open_doc()

# VariableList
r = eng.call("CreateSessionObject", h, [{
    "qInfo": {"qType": "VariableList"},
    "qVariableListDef": {"qType": "variable", "qShowReserved": False, "qShowConfig": False,
                          "qData": {"tags": "/tags"}},
}])
vh = r["qReturn"]["qHandle"]
layout = eng.call("GetLayout", vh)
items = layout["qLayout"]["qVariableList"]["qItems"]
print(f"=== {len(items)} variabler ===")
for v in items:
    name = v.get("qName", "")
    if name.lower().startswith("vbst") or "prikking" in name.lower() or "grense" in name.lower():
        defn = v.get("qDefinition", "")
        print(f"- {name}: {defn[:220]}")

# Resten av tabellene (fakta)
r = eng.call("GetTablesAndKeys", h, [{"qcx": 1000, "qcy": 1000}, {"qcx": 0, "qcy": 0}, 30, True, False])
print("\n=== fakta-/øvrige tabeller ===")
for t in r.get("qtr", []):
    name = t["qName"]
    if name.startswith("Dim") or name in ("Kalender", "KalenderTilsagn", "KommuneBridge", "Tilstand", "Låneordning"):
        continue
    fields = [f["qName"] for f in t.get("qFields", [])]
    print(f"[{name}] ({t.get('qNoOfRows')} rader)")
    print("   ", ", ".join(fields))

eng.close()
