#!/usr/bin/env python3
"""Validate the frozen phase-1 data contract and emit JSON events."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import re
import sys
import traceback
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
DATA_VINTAGE = "2026-08-04"

OSLO = Path("data/raw/husbanken_bostotte_oslo_manedlig.csv")
BYDEL = Path("data/raw/husbanken_bostotte_oslo_bydel_manedlig.csv")
GROUP = Path(
    "data/raw/"
    "husbanken_bostotte_oslo_brukergruppe_manedlig.csv"
)
INTERVENTIONS = Path("data/clean/intervensjonstabell.csv")
REPORT = Path("bostotte_oslo.qmd")
BIB = Path("referanser.bib")

ADDITIVE = (
    "ant_husstander_utbetaling",
    "ant_husstander_termin",
    "ant_soknader",
    "ant_avslag",
    "utbetalt_belop",
    "ant_over_tak",
)
BASE_COLUMNS = {
    "aar",
    "manedsnr",
    *ADDITIVE,
    "gjsnitt_bostotte",
    "gjsnitt_inntekt_mnd",
    "gjsnitt_boutgift_mnd",
    "geo",
}
EXPECTED_GROUPS = {
    "Eldre",
    "Husstander med midlertidige trygdeytelser",
    "Husstander uten trygdeytelser",
    "Uføre forøvrig",
    "Unge uføre",
}
EXPECTED_BYDELER = {f"{code:04d}" for code in range(311, 326)}
DATE_FIELDS = (
    "dato_virkning",
    "termin_fra",
    "termin_til",
    "utbetaling_fra",
    "utbetaling_til",
)


class Run:
    def __init__(self) -> None:
        self.id = str(uuid.uuid4())
        self.started = datetime.now(timezone.utc)
        self.events: list[dict[str, Any]] = []
        self.files: dict[str, dict[str, Any]] = {}
        self.counts = {"passed": 0, "warning": 0, "error": 0}

    def emit(self, status: str, check: str, **details: Any) -> bool:
        event = {
            "event": "validation_check",
            "run_id": self.id,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "check": check,
            "details": details,
        }
        self.events.append(event)
        self.counts[status] += 1
        print(json.dumps(event, ensure_ascii=False, sort_keys=True))
        return status != "error"

    def check(self, name: str, condition: bool, **details: Any) -> bool:
        return self.emit("passed" if condition else "error", name, **details)

    def warn(self, name: str, **details: Any) -> None:
        self.emit("warning", name, **details)

    def track(self, path: Path) -> None:
        raw = path.read_bytes()
        rel = str(path.relative_to(ROOT))
        self.files[rel] = {
            "path": rel,
            "size_bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        }

    def manifest(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "project": "bostotte-oslo",
            "run_id": self.id,
            "started_at_utc": self.started.isoformat(),
            "finished_at_utc": datetime.now(timezone.utc).isoformat(),
            "data_vintage": DATA_VINTAGE,
            "git": {
                "sha": os.getenv("GITHUB_SHA"),
                "ref": os.getenv("GITHUB_REF"),
                "run_id": os.getenv("GITHUB_RUN_ID"),
                "workflow": os.getenv("GITHUB_WORKFLOW"),
            },
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "ci": os.getenv("CI", "").lower() == "true",
            },
            "summary": {
                **self.counts,
                "status": "failed" if self.counts["error"] else "passed",
            },
            "files": [self.files[key] for key in sorted(self.files)],
            "events": self.events,
        }


def read_csv(run: Run, relative: Path, required: set[str]) -> list[dict[str, str]]:
    path = ROOT / relative
    if not run.check(f"file:{relative}", path.is_file()):
        return []

    run.track(path)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        columns = set(reader.fieldnames or [])

    run.check(f"rows:{relative}", bool(rows), rows=len(rows))
    run.check(
        f"schema:{relative}",
        required <= columns,
        missing=sorted(required - columns),
    )
    return rows


def month_index(row: dict[str, str]) -> int:
    year, month = int(row["aar"]), int(row["manedsnr"])
    if month not in range(1, 13):
        raise ValueError(f"invalid month {year}-{month}")
    return year * 12 + month - 1


def month(row: dict[str, str]) -> str:
    return f"{int(row['aar']):04d}-{int(row['manedsnr']):02d}"


def value(row: dict[str, str], field: str) -> float:
    result = float(row[field])
    if not math.isfinite(result) or result < 0:
        raise ValueError(f"{field}={row[field]}")
    return result


def numeric_contract(run: Run, name: str, rows: list[dict[str, str]]) -> bool:
    errors: list[str] = []
    for row in rows:
        for field in ADDITIVE:
            try:
                value(row, field)
            except (KeyError, TypeError, ValueError) as exc:
                if len(errors) < 10:
                    errors.append(f"{row.get('aar')}-{row.get('manedsnr')}: {exc}")
    return run.check(f"{name}:nonnegative_numeric", not errors, examples=errors)


def oslo_contract(run: Run, rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    if not rows or not numeric_contract(run, "oslo", rows):
        return {}

    invalid: list[str] = []
    keyed: dict[str, dict[str, str]] = {}
    duplicates: list[str] = []
    for row in rows:
        try:
            label = month(row)
            month_index(row)
        except (KeyError, TypeError, ValueError) as exc:
            invalid.append(str(exc))
            continue
        if label in keyed:
            duplicates.append(label)
        keyed[label] = row

    if not run.check("oslo:valid_months", not invalid, examples=invalid[:10]):
        return {}
    run.check("oslo:unique_month", not duplicates, duplicates=sorted(set(duplicates)))
    ordered = sorted(rows, key=month_index)
    gaps = [
        (month(left), month(right))
        for left, right in zip(ordered, ordered[1:])
        if month_index(right) != month_index(left) + 1
    ]
    run.check(
        "oslo:continuous_months",
        not gaps,
        rows=len(ordered),
        first=month(ordered[0]),
        last=month(ordered[-1]),
        gaps=gaps[:10],
    )
    run.check("oslo:minimum_history", len(ordered) >= 120, rows=len(ordered))
    run.check(
        "oslo:geography",
        {row["geo"] for row in ordered} == {"Oslo"},
        observed=sorted({row["geo"] for row in ordered}),
    )

    mismatches = []
    for left, right in zip(ordered, ordered[1:]):
        term = value(left, "ant_husstander_termin")
        payment = value(right, "ant_husstander_utbetaling")
        if term != payment and len(mismatches) < 10:
            mismatches.append(
                {
                    "term_month": month(left),
                    "payment_month": month(right),
                    "term": term,
                    "payment": payment,
                }
            )
    run.check(
        "oslo:term_to_payment",
        not mismatches,
        compared_pairs=max(0, len(ordered) - 1),
        mismatches=mismatches,
    )

    latest = ordered[-1]
    edge = (
        value(latest, "ant_husstander_termin") == 0
        and value(latest, "ant_husstander_utbetaling") > 0
    )
    if edge:
        run.emit("passed", "oslo:realtime_edge", month=month(latest))
    else:
        run.warn(
            "oslo:realtime_edge_review",
            month=month(latest),
            term=latest["ant_husstander_termin"],
            payment=latest["ant_husstander_utbetaling"],
        )
    return keyed


def panel_contract(
    run: Run,
    name: str,
    rows: list[dict[str, str]],
    entity: str,
    oslo: dict[str, dict[str, str]],
) -> None:
    if not rows or not oslo or not numeric_contract(run, name, rows):
        return

    keys = [(row[entity], month(row)) for row in rows]
    run.check(f"{name}:unique_key", len(keys) == len(set(keys)))
    run.check(
        f"{name}:known_months",
        {label for _, label in keys} <= set(oslo),
        unknown=sorted({label for _, label in keys} - set(oslo)),
    )

    entities: dict[str, set[str]] = defaultdict(set)
    for item, label in keys:
        entities[label].add(item)

    if name == "brukergruppe":
        observed = {row[entity] for row in rows}
        run.check(
            "brukergruppe:categories",
            observed == EXPECTED_GROUPS,
            expected=sorted(EXPECTED_GROUPS),
            observed=sorted(observed),
        )
        incomplete = {
            label: sorted(EXPECTED_GROUPS - values)
            for label, values in entities.items()
            if values != EXPECTED_GROUPS
        }
        run.check(
            "brukergruppe:monthly_coverage",
            not incomplete,
            examples=dict(list(incomplete.items())[:10]),
        )
    else:
        codes = {row[entity] for row in rows}
        run.check(
            "bydel:code_format",
            all(re.fullmatch(r"\d{4}", code) for code in codes),
            invalid=sorted(code for code in codes if not re.fullmatch(r"\d{4}", code)),
        )
        incomplete = {
            label: sorted(EXPECTED_BYDELER - entities.get(label, set()))
            for label in oslo
            if not EXPECTED_BYDELER <= entities.get(label, set())
        }
        run.check(
            "bydel:monthly_coverage",
            not incomplete,
            examples=dict(list(incomplete.items())[:10]),
        )

    sums = {field: defaultdict(float) for field in ADDITIVE}
    for row in rows:
        label = month(row)
        for field in ADDITIVE:
            sums[field][label] += value(row, field)

    mismatches = []
    for field in ADDITIVE:
        for label, total in oslo.items():
            expected = value(total, field)
            actual = sums[field].get(label, 0.0)
            if abs(expected - actual) > 0.005 and len(mismatches) < 20:
                mismatches.append(
                    {
                        "field": field,
                        "month": label,
                        "expected": expected,
                        "actual": actual,
                    }
                )
    run.check(
        f"{name}:sums_to_oslo",
        not mismatches,
        measures=list(ADDITIVE),
        months=len(oslo),
        mismatches=mismatches,
    )


def intervention_contract(run: Run) -> None:
    required = {
        "id",
        *DATE_FIELDS,
        "hendelse",
        "type",
        "mekanisme",
        "forventet_effekt_antall",
        "forventet_effekt_belop",
        "geografi",
        "kilde",
        "verifisering",
    }
    rows = read_csv(run, INTERVENTIONS, required)
    if not rows:
        return

    ids = [row["id"] for row in rows]
    run.check("interventions:unique_id", len(ids) == len(set(ids)))
    run.check("interventions:minimum_rows", len(rows) >= 20, rows=len(rows))

    invalid_dates = [
        {"id": row["id"], "field": field, "value": row[field]}
        for row in rows
        for field in DATE_FIELDS
        if row[field] and not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", row[field])
    ]
    run.check("interventions:date_format", not invalid_dates, examples=invalid_dates[:10])
    blanks = [row["id"] for row in rows if not row["kilde"].strip()]
    run.check("interventions:sources_present", not blanks, ids=blanks)

    partial = [row["id"] for row in rows if row["verifisering"] != "bekreftet"]
    if partial:
        run.warn("interventions:partial_source_verification", ids=partial)
    else:
        run.emit("passed", "interventions:all_source_verified")


def citation_contract(run: Run) -> None:
    paths = (ROOT / REPORT, ROOT / BIB)
    if not all(run.check(f"file:{path.relative_to(ROOT)}", path.is_file()) for path in paths):
        return
    for path in paths:
        run.track(path)

    report = paths[0].read_text(encoding="utf-8")
    bibliography = paths[1].read_text(encoding="utf-8")
    cited: set[str] = set()
    for bracket in re.findall(r"\[([^\]]*@[^\]]*)\]", report):
        cited.update(
            key.rstrip(";,.")
            for key in re.findall(r"@([A-Za-z][A-Za-z0-9_:.+-]*)", bracket)
        )
    entries = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", bibliography))
    run.check(
        "report:citation_keys",
        cited <= entries,
        cited=len(cited),
        bibliography_entries=len(entries),
        missing=sorted(cited - entries),
    )

    placeholders = bibliography.count("PLASSHOLDER")
    if placeholders:
        run.warn("report:bibliography_placeholders", occurrences=placeholders)
    else:
        run.emit("passed", "report:no_bibliography_placeholders")


def governance_contract(run: Run) -> None:
    """Filene en leser trenger for aa kunne etterproeve arbeidet.

    Listen er bevisst kort: den skal garantere at dokumentasjonen av data og
    endringer faktisk foelger med repoet, ikke at et bestemt prosessrammeverk
    er fulgt.
    """
    for relative in (
        Path("README.md"),
        Path("bostotte_oslo.qmd"),
        Path("data/docs/kodebok.md"),
        Path("data/docs/datakilder.md"),
        Path("logg/endringslogg-kap1-2.md"),
        Path("logg/endringslogg-kap3-data.md"),
        Path("verifiser.R"),
        Path("oppsett.R"),
    ):
        path = ROOT / relative
        if run.check(f"file:{relative}", path.is_file()):
            run.track(path)


def validate(run: Run) -> None:
    governance_contract(run)
    oslo_rows = read_csv(run, OSLO, BASE_COLUMNS)
    bydel_rows = read_csv(run, BYDEL, (BASE_COLUMNS - {"geo"}) | {"kommunenr", "bydel"})
    group_rows = read_csv(run, GROUP, BASE_COLUMNS | {"brukergruppe"})

    oslo = oslo_contract(run, oslo_rows)
    panel_contract(run, "bydel", bydel_rows, "kommunenr", oslo)
    panel_contract(run, "brukergruppe", group_rows, "brukergruppe", oslo)
    intervention_contract(run)
    citation_contract(run)


def write_manifest(path: Path, run: Run) -> None:
    destination = path if path.is_absolute() else ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(run.manifest(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"event": "manifest_written", "run_id": run.id, "path": str(destination)},
            ensure_ascii=False,
            sort_keys=True,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    run = Run()

    try:
        validate(run)
    except Exception as exc:
        run.emit(
            "error",
            "validator:unexpected_exception",
            exception_type=type(exc).__name__,
            exception=str(exc),
            traceback=traceback.format_exc(),
        )
    finally:
        if args.manifest:
            write_manifest(args.manifest, run)
        print(
            json.dumps(
                {"event": "validation_summary", "run_id": run.id, **run.manifest()["summary"]},
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    return 1 if run.counts["error"] else 0


if __name__ == "__main__":
    sys.exit(main())
