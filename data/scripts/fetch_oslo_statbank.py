"""Hent bydelstabeller fra Oslo kommunes statistikkbank (PxWeb-API).

Tabeller (alle på bydelsnivå, årlige):
  SOS001 : Mottakere av arbeidsavklaringspenger (B) 2012-2024
  SOS006 : Mottakere av uføretrygd (B) 2004-2024
  STØ013 : Sosialhjelpsmottakere og berørte (B) 2005-2023
  STØ020 : Antall og andel sosialhjelpsmottakere i befolkningen (B) 2007-2023
"""
import csv
import itertools
import json
import urllib.parse
import urllib.request

BASE = "https://statistikkbanken.oslo.kommune.no/statbank/api/v1/no/db1/"
RAW = "../data/raw/"
CLEAN = "../data/clean/"

TABLES = {
    "oslo_sos001_aap_bydel": "Trygd, sosiale tjenester og barnevern/Trygd/Ok-SOS001.px",
    "oslo_sos006_uforetrygd_bydel": "Trygd, sosiale tjenester og barnevern/Trygd/OK-SOS006.px",
    "oslo_sto013_sosialhjelp_bydel": "Trygd, sosiale tjenester og barnevern/Sosialtjenesten/OK-STØ013.px",
    "oslo_sto020_sosialhjelp_andel_bydel": "Trygd, sosiale tjenester og barnevern/Sosialtjenesten/OK-STØ020.px",
    "oslo_bef004_folkemengde_bydel": "Befolkning/Folkemengde/OK-BEF004.px",
    "oslo_bef005_folkemengde_bydel": "Befolkning/Folkemengde/OK-BEF005.px",
}

BYDEL = {1: "Gamle Oslo", 2: "Grünerløkka", 3: "Sagene", 4: "St. Hanshaugen", 5: "Frogner",
         6: "Ullern", 7: "Vestre Aker", 8: "Nordre Aker", 9: "Bjerke", 10: "Grorud",
         11: "Stovner", 12: "Alna", 13: "Østensjø", 14: "Nordstrand", 15: "Søndre Nordstrand",
         16: "Sentrum", 17: "Marka"}


def fetch_bef036_bydel():
    """BEF036 (framskriving 2025-2050) er på delbydelsnivå og for stor for full
    henting (403). Henter MMM-scenarioet x 'Alder i alt' x alle delbydeler og
    aggregerer til bydel via kodestrukturen (områdekode // 100 = bydelsnr)."""
    from collections import defaultdict
    path = "Befolkning/Befolkningsframskrivinger/BEF036.px"
    m = get_meta(path)
    sc = next(v for v in m["variables"] if v["code"] == "scenario")
    ald = next(v for v in m["variables"] if v["code"] == "alder")
    q = [
        {"code": "scenario", "selection": {"filter": "item",
         "values": [sc["values"][sc["valueTexts"].index("Mellomalternativet MMM")]]}},
        {"code": "alder", "selection": {"filter": "item",
         "values": [ald["values"][ald["valueTexts"].index("Alder i alt")]]}},
    ]
    js = post_query(path, q)
    json.dump(js, open(RAW + "oslo_bef036_framskriving_omrade.json", "w"))
    flatten(js, CLEAN + "oslo_bef036_framskriving_omrade.csv")
    agg = defaultdict(float)
    with open(CLEAN + "oslo_bef036_framskriving_omrade.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            agg[(int(r["område_kode"]) // 100, int(r["år_navn"]))] += float(r["verdi"])
    with open(CLEAN + "oslo_bef036_framskriving_bydel.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["bydel_nr", "bydel", "husbanken_kommunenr", "aar", "framskrevet_folkemengde_mmm"])
        for (b, aar) in sorted(agg):
            w.writerow([b, BYDEL[b], f"03{10+b}" if b <= 15 else "", aar, int(round(agg[(b, aar)]))])
    print(f"  -> {CLEAN}oslo_bef036_framskriving_bydel.csv ({len(agg)} rader)")


def get_meta(path):
    url = BASE + urllib.parse.quote(path)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read().decode())


def post_query(path, query):
    url = BASE + urllib.parse.quote(path)
    body = json.dumps({"query": query, "response": {"format": "json-stat2"}}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def flatten(js, path):
    dims = js["id"]
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
            w.writerow([c[0] for c in combo] + [c[1] for c in combo] + [values[i]])
    print(f"  -> {path} ({len(values)} verdier)")


if __name__ == "__main__":
    for name, path in TABLES.items():
        try:
            m = get_meta(path)
            print(f"[{name}] {m['title'][:90]}")
            # eksplisitt alle verdier for alle variabler
            q = [{"code": v["code"], "selection": {"filter": "all", "values": ["*"]}}
                 for v in m["variables"]]
            js = post_query(path, q)
            json.dump(js, open(RAW + f"{name}.json", "w"))
            flatten(js, CLEAN + f"{name}.csv")
        except Exception as e:
            print(f"[{name}] FEIL: {e}")
    fetch_bef036_bydel()
