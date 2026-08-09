#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_prognose.py — kontraktstester for den kanoniske prognoseartefakten.

Artefakten (prognose/prognose_gjeldende.csv og .json) produseres av én
navngitt beregning: chunken `prognose-artefakt` i bostotte_oslo.qmd, ved
rendering. Denne validatoren er ren Python uten avhengigheter, slik at CI og
en leser uten R kan kontrollere at artefakten holder sin egen kontrakt.

Kontrakten (jf. revisjon/02_release_verification.md):
  P01  horisontene er nøyaktig 1–12, uten hull eller duplikater
  P02  målmånedene er sammenhengende kalendermåneder
  P03  målmåned = prognoseopprinnelse + h for hver rad
  P04  punktprognose og alle intervallgrenser finnes (ingen tomme felt)
  P05  lo95 <= lo80 <= punkt <= hi80 <= hi95
  P06  ingen prognose eller grense er negativ
  P07  informasjonsstatus følger den vedtatte kalenderen: målmåneder til og
       med siste politisk avklarte periode er «vedtatt_kalender», senere
       måneder «viderefort_regelverk» (uttrykkelig antakelse, ikke vedtak)
  P08  ingen regelverkssteg i horisonten bryter known_from: hvert steg i
       data/clean/regelverk_kunnskap.csv med steg_dato i prognosevinduet har
       effect_known_from <= opprinnelsen (ellers måtte raden vært scenario)
  P09  datahash i artefakten stemmer med md5 av kildefilene den oppgir
  P10  commit-feltet er en 40-tegns SHA (sporbar mot git-historikken)
  P11  CSV og JSON beskriver identiske tall (samme 12 rader)
  P12  n_kalibreringsfeil > 0 og likt oppgitt kalibreringsgrunnlag
  P13  README-utdraget (prognose/README_utdrag.md) står ordrett i README.md,
       slik at README ikke kan sitere andre tall enn artefaktens

Kjøring:  python scripts/validate_prognose.py
Avslutter med kode 0 når alle kontraktene holder, ellers 1.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
CSVFIL = ROT / "prognose" / "prognose_gjeldende.csv"
JSONFIL = ROT / "prognose" / "prognose_gjeldende.json"
KUNNSKAP = ROT / "data" / "clean" / "regelverk_kunnskap.csv"
UTDRAG = ROT / "prognose" / "README_utdrag.md"
README = ROT / "README.md"

feil: list[str] = []
ok_teller = 0


def krav(navn: str, betingelse: bool, detalj: str = "") -> None:
    global ok_teller
    if betingelse:
        ok_teller += 1
        print(f"  OK      {navn}")
    else:
        feil.append(f"{navn}: {detalj}")
        print(f"  FEIL    {navn}  {detalj}")


def les_maaned(s: str) -> date:
    aar, mnd = int(s[:4]), int(s[5:7])
    return date(aar, mnd, 1)


def pluss_mnd(d: date, n: int) -> date:
    m = d.month - 1 + n
    return date(d.year + m // 12, m % 12 + 1, 1)


def main() -> int:
    print("Kontraktstest av prognoseartefakten")
    print("-" * 62)

    for fil in (CSVFIL, JSONFIL, KUNNSKAP):
        if not fil.exists():
            print(f"  MANGLER {fil.relative_to(ROT)}")
            return 1

    with open(JSONFIL, encoding="utf-8") as f:
        art = json.load(f)
    meta = art["meta"]
    rader = art["prognoser"]

    with open(CSVFIL, encoding="utf-8") as f:
        csv_rader = list(csv.DictReader(f))

    opprinnelse = les_maaned(meta["prognoseopprinnelse"])
    vedtatt_til = les_maaned(meta["vedtatt_kalender_til"])

    # P01 horisonter
    hs = [int(r["horisont"]) for r in rader]
    krav("P01 horisonter 1-12", hs == list(range(1, 13)), f"fikk {hs}")

    # P02 sammenhengende målmåneder
    mnd = [les_maaned(r["maalmaned"]) for r in rader]
    sammenhengende = all(mnd[i + 1] == pluss_mnd(mnd[i], 1) for i in range(11))
    krav("P02 sammenhengende maalmaneder", sammenhengende)

    # P03 målmåned = opprinnelse + h
    krav("P03 maalmaned = opprinnelse + h",
         all(m == pluss_mnd(opprinnelse, h) for m, h in zip(mnd, hs)))

    # P04 ingen tomme felt
    felt = ("punkt", "lo80", "hi80", "lo95", "hi95")
    komplett = all(r.get(k) is not None and r.get(k) != "" for r in rader for k in felt)
    krav("P04 punkt og intervaller komplette", komplett)

    # P05 ordning av grenser
    orden = all(
        float(r["lo95"]) <= float(r["lo80"]) <= float(r["punkt"])
        <= float(r["hi80"]) <= float(r["hi95"])
        for r in rader
    )
    krav("P05 lo95 <= lo80 <= punkt <= hi80 <= hi95", orden)

    # P06 ikke-negativitet
    krav("P06 ikke-negative verdier",
         all(float(r[k]) >= 0 for r in rader for k in felt))

    # P07 informasjonsstatus per målmåned
    status_ok = all(
        (r["informasjonsstatus"] == "vedtatt_kalender") == (m <= vedtatt_til)
        for r, m in zip(rader, mnd)
    ) and all(r["informasjonsstatus"] in ("vedtatt_kalender", "viderefort_regelverk")
              for r in rader)
    krav("P07 informasjonsstatus foelger vedtatt kalender",
         status_ok, f"vedtatt til {vedtatt_til}")

    # P08 known_from-porten for steg i prognosevinduet
    brudd = []
    with open(KUNNSKAP, encoding="utf-8") as f:
        for rad in csv.DictReader(f):
            if not rad["steg_dato"]:
                continue
            steg = les_maaned(rad["steg_dato"])
            if mnd[0] <= steg <= mnd[-1]:
                kjent = date.fromisoformat(rad["effect_known_from"])
                # kjent senest ved utgangen av opprinnelsesmåneden
                if kjent > pluss_mnd(opprinnelse, 1):
                    brudd.append(f"{rad['intervensjon_id']} kjent {kjent}")
    krav("P08 ingen regelverkssteg bryter known_from", not brudd, "; ".join(brudd))

    # P09 datahash
    hasher = []
    for kilde in meta["datahash_kilder"]:
        h = hashlib.md5((ROT / kilde).read_bytes()).hexdigest()
        hasher.append(h)
    krav("P09 datahash stemmer med kildefilene",
         hasher == meta["datahash_md5"],
         f"beregnet {hasher} mot oppgitt {meta['datahash_md5']}")

    # P10 commit
    krav("P10 commit er 40-tegns SHA",
         bool(re.fullmatch(r"[0-9a-f]{40}", meta.get("commit", ""))),
         f"fikk '{meta.get('commit', '')}'")

    # P11 CSV og JSON er samme tall
    like = len(csv_rader) == 12 and all(
        c["maalmaned"] == r["maalmaned"]
        and int(c["horisont"]) == int(r["horisont"])
        and all(abs(float(c[k]) - float(r[k])) < 1e-9 for k in felt)
        and c["informasjonsstatus"] == r["informasjonsstatus"]
        for c, r in zip(csv_rader, rader)
    )
    krav("P11 CSV og JSON er identiske", like)

    # P12 kalibreringsgrunnlag
    krav("P12 n_kalibreringsfeil oppgitt og positiv",
         all(int(r["n_kalibreringsfeil"]) > 0 for r in rader))

    # P13 README-utdraget står ordrett i README
    if UTDRAG.exists() and README.exists():
        utdrag = UTDRAG.read_text(encoding="utf-8").strip()
        i_readme = utdrag in README.read_text(encoding="utf-8")
        krav("P13 README-utdraget staar ordrett i README", i_readme,
             "README.md siterer ikke prognose/README_utdrag.md ordrett")
    else:
        krav("P13 README-utdraget finnes", False,
             "prognose/README_utdrag.md eller README.md mangler")

    print("-" * 62)
    print(f"{ok_teller} kontrakter bestått, {len(feil)} feilet")
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(main())
