"""Hent støtteserier fra SSB PxWeb-API v0 (data.ssb.no) og flat ut JSON-stat2 til CSV.

Tabeller:
  09895 : Leiemarkedsundersøkelsen, mnd-leie etter prissone x rom (årlig)
  03013 : KPI etter konsumgruppe, 2015=100 (mnd, 1979M01-2025M12; husleieindeks = 04.1)
  14710 : KPI historisk totalindeks 2025=100 (mnd, -> 2026)
  01222 : Befolkningsendringer i kvartalet, Oslo kommune (0301), 1997K4->
"""
import csv
import itertools
import json
import urllib.request

BASE = "https://data.ssb.no/api/v0/no/table/"
RAW = "../data/raw/"
CLEAN = "../data/clean/"


def api(table_id, query):
    url = BASE + table_id
    body = json.dumps({"query": query, "response": {"format": "json-stat2"}}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode())


def flatten(js, path):
    dims = js["id"]
    sizes = js["size"]
    cats = []
    for d in dims:
        cat = js["dimension"][d]["category"]
        idx = sorted(cat["index"], key=lambda k: cat["index"][k])
        labels = cat.get("label", {})
        cats.append([(code, labels.get(code, code)) for code in idx])
    values = js["value"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([f"{d}_kode" for d in dims] + [f"{d}_navn" for d in dims] + ["verdi"])
        for i, combo in enumerate(itertools.product(*cats)):
            codes = [c[0] for c in combo]
            names = [c[1] for c in combo]
            w.writerow(codes + names + [values[i]])
    print(f"  -> {path}  ({len(values)} verdier)")


def meta(table_id):
    with urllib.request.urlopen(BASE + table_id, timeout=60) as r:
        return json.loads(r.read().decode())


def values_of(m, var_code):
    for v in m["variables"]:
        if v["code"] == var_code:
            return v["values"], v["valueTexts"]
    raise KeyError(var_code)


if __name__ == "__main__":
    # --- 09895 Leiemarkedsundersøkelsen ---
    m = meta("09895")
    print("09895 variabler:", [(v["code"], len(v["values"])) for v in m["variables"]])
    soner, sonetekst = values_of(m, "Soner2")
    print("09895 soner:", list(zip(soner, sonetekst)))
    oslosoner = [s for s, t in zip(soner, sonetekst) if "Oslo" in t or "landet" in t.lower()]
    q = [
        {"code": "Soner2", "selection": {"filter": "item", "values": oslosoner}},
        # alle rom, alle innhold, alle år -> utelat filter for resten
    ]
    js = api("09895", q)
    json.dump(js, open(RAW + "ssb_09895_leiemarked.json", "w"))
    flatten(js, CLEAN + "ssb_09895_leiemarked_oslo.csv")

    # --- 03013 KPI etter konsumgruppe ---
    m = meta("03013")
    grupper, grtekst = values_of(m, "Konsumgrp")
    keep = [g for g, t in zip(grupper, grtekst)
            if g in ("TOTAL",) or g.startswith("04.1") or g in ("04",)]
    print("03013 KPI-grupper valgt:", list(zip(keep, [t for g, t in zip(grupper, grtekst) if g in keep]))[:8])
    q = [
        {"code": "Konsumgrp", "selection": {"filter": "item", "values": keep}},
    ]
    js = api("03013", q)
    json.dump(js, open(RAW + "ssb_03013_kpi_konsumgruppe.json", "w"))
    flatten(js, CLEAN + "ssb_03013_kpi_husleie.csv")

    # --- 14710 KPI historisk (2025=100), mnd ---
    js = api("14710", [])
    json.dump(js, open(RAW + "ssb_14710_kpi_historisk.json", "w"))
    flatten(js, CLEAN + "ssb_14710_kpi_totalindeks.csv")

    # --- 01222 Befolkning kvartal, Oslo ---
    m = meta("01222")
    print("01222 variabler:", [(v["code"], len(v["values"])) for v in m["variables"]])
    regs, regtekst = values_of(m, "Region")
    oslo = [r for r, t in zip(regs, regtekst) if t == "Oslo" or r == "0301"]
    print("01222 Oslo-koder:", oslo)
    q = [{"code": "Region", "selection": {"filter": "item", "values": oslo}}]
    js = api("01222", q)
    json.dump(js, open(RAW + "ssb_01222_befolkning_oslo.json", "w"))
    flatten(js, CLEAN + "ssb_01222_befolkning_oslo_kvartal.csv")

    print("Ferdig.")
