#!/usr/bin/env python3
"""Validate the frozen phase-1 data contract.

The validator deliberately depends only on the Python standard library. It
prints one JSON event per check, exits non-zero on contract violations, and can
write a machine-readable run manifest for CI or local review.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
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

PROJECT = "bostotte-oslo"
DATA_VINTAGE = "2026-08-04"
ROOT = Path(__file__).resolve().parents[1]

OSLO_FILE = Path(
    "velferdsetaten-data/data/raw/husbanken_bostotte_oslo_manedlig.csv"
)
BYDEL_FILE = Path(
    "velferdsetaten-data/data/raw/husbanken_bostotte_oslo_bydel_manedlig.csv"
)
GROUP_FILE = Path(
    "velferdsetaten-data/data/raw/"
    "husbanken_bostotte_oslo_brukergruppe_manedlig.csv"
)
INTERVENTION_FILE = Path(
    "velferdsetaten-data/data/clean/intervensjonstabell.csv"
)
REPORT_FILE = Path("unt_1.qmd")
BIB_FILE = Path("referanser.bib")

ADDITIVE_MEASURES = (
    "ant_husstander_utbetaling",
    "ant_husstander_termin",
    "ant_soknader",
    "ant_avslag",
    "utbetalt_belop",
    "ant_over_tak",
)

MONTHLY_REQUIRED = {
    "aar",
    "manedsnr",
    *ADDITIVE_MEASURES,
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

EXPECTED_BYDEL_CODES = {f"{code:04d}" for code in range(311, 326)}
DATE_FIELDS = (
    "dato_virkning",
    "termin_fra",
    "termin_til",
    "utbetaling_fra",
    "utbetaling_til",
)


class Recorder:
    """Collect and emit structured validation events."""

    def __init__(self) -> None:
        self.run_id = str(uuid.uuid4())
        self.started_at = datetime.now(timezone.utc)
        self.events: list[dict[str, Any]] = []
        self.files: list[dict[str, Any]] = []
        self.errors = 0
        self.warnings = 0
        self.passed = 0

    def emit(
        self,
        status: str,
        check: str,
        message: str,
        **details: Any,
    ) -> None:
        event = {
            "event": "validation_check",
            "run_id": self.run_id,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "check": check,
            "message": message,
            "details": details,
        }
        self.events.append(event)
        if status == "error":
            self.errors += 1
        elif status == "warning":
            self.warnings += 1
        elif status == "passed":
            self.passed += 1
        print(json.dumps(event, ensure_ascii=False, sort_keys=True))

    def require(
        self,
        condition: bool,
        check: str,
        success: str,
        failure: str,
        **details: Any,
    ) -> bool:
        self.emit(
            "passed" if condition else "error",
            check,
            success if condition else failure,
            **details,
        )
        return condition

    def warn(self, check: str, message: str, **details: Any) -> None:
        self.emit("warning", check, message, **details)

    def register_file(self, path: Path) -> None:
        raw = path.read_bytes()
        self.files.append(
            {
                "path": str(path.relative_to(ROOT)),
                "size_bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
            }
        )

    def manifest(self) -> dict[str, Any]:
        finished = datetime.now(timezone.utc)
        return {
            "schema_version": 1,
            "project": PROJECT,
            "run_id": self.run_id,
            "started_at_utc": self.started_at.isoformat(),
            "finished_at_utc": finished.isoformat(),
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
                "passed": self.passed,
                "warnings": self.warnings,
                "errors": self.errors,
                "status": "failed" if self.errors else "passed",
            },
            "files": sorted(self.files, key=lambda item: item["path"]),
            "events": self.events,
        }


def read_csv(
    relative_path: Path,
    recorder: Recorder,
) -> tuple[list[dict[str, str]], list[str]]:
    path = ROOT / relative_path
    if not recorder.require(
        path.is_file(),
        f"file_exists:{relative_path}",
        "Required file exists.",
        "Required file is missing.",
        path=str(relative_path),
    ):
        return [], []

    recorder.register_file(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        columns = list(reader.fieldnames or [])

    recorder.require(
        bool(rows),
        f"rows_present:{relative_path}",
        "File contains data rows.",
        "File contains no data rows.",
        rows=len(rows),
    )
    return rows, columns


def month_number(row: dict[str, str]) -> int:
    year = int(row["aar"])
    month = int(row["manedsnr"])
    if not 1 <= month <= 12:
        raise ValueError(f"Invalid month: {year}-{month}")
    return year * 12 + month - 1


def month_label(row: dict[str, str]) -> str:
    return f"{int(row['aar']):04d}-{int(row['manedsnr']):02d}"


def number(value: str, field: str, row_label: str) -> float:
    if value is None or value.strip() == "":
        raise ValueError(f"Blank numeric field {field} at {row_label}")
    parsed = float(value)
    if parsed < 0:
        raise ValueError(f"Negative field {field}={parsed} at {row_label}")
    return parsed


def validate_headers(
    recorder: Recorder,
    name: str,
    columns: Iterable[str],
    required: set[str],
) -> bool:
    present = set(columns)
    missing = sorted(required - present)
    return recorder.require(
        not missing,
        f"schema:{name}",
        "Required columns are present.",
        "Required columns are missing.",
        missing=missing,
        columns=sorted(present),
    )


def validate_numeric_fields(
    recorder: Recorder,
    name: str,
    rows: list[dict[str, str]],
    fields: Iterable[str],
) -> None:
    bad: list[str] = []
    for row in rows:
        label = month_label(row)
        for field in fields:
            try:
                number(row.get(field, ""), field, label)
            except (TypeError, ValueError) as exc:
                if len(bad) < 10:
                    bad.append(str(exc))
    recorder.require(
        not bad,
        f"nonnegative_numeric:{name}",
        "Additive measures are numeric and non-negative.",
        "Invalid additive measures found.",
        examples=bad,
    )


def validate_oslo(
    recorder: Recorder,
    rows: list[dict[str, str]],
    columns: list[str],
) -> dict[str, dict[str, str]]:
    if not validate_headers(recorder, "oslo", columns, MONTHLY_REQUIRED):
        return {}

    validate_numeric_fields(recorder, "oslo", rows, ADDITIVE_MEASURES)

    keyed: dict[str, dict[str, str]] = {}
    duplicates: list[str] = []
    invalid_dates: list[str] = []
    for row in rows:
        try:
            label = month_label(row)
            month_number(row)
        except (TypeError, ValueError, KeyError) as exc:
            invalid_dates.append(str(exc))
            continue
        if label in keyed:
            duplicates.append(label)
        keyed[label] = row

    recorder.require(
        not invalid_dates,
        "oslo_valid_months",
        "All Oslo month fields are valid.",
        "Invalid Oslo month fields found.",
        examples=invalid_dates[:10],
    )
    recorder.require(
        not duplicates,
        "oslo_unique_month",
        "Oslo has one row per month.",
        "Duplicate Oslo months found.",
        duplicates=sorted(set(duplicates)),
    )

    ordered = sorted(rows, key=month_number)
    gaps: list[tuple[str, str]] = []
    for left, right in zip(ordered, ordered[1:]):
        if month_number(right) != month_number(left) + 1:
            gaps.append((month_label(left), month_label(right)))
    recorder.require(
        not gaps,
        "oslo_continuous_months",
        "Oslo month index is continuous.",
        "Gaps found in Oslo month index.",
        gaps=gaps[:10],
        rows=len(ordered),
        first=month_label(ordered[0]) if ordered else None,
        last=month_label(ordered[-1]) if ordered else None,
    )
    recorder.require(
        len(ordered) >= 120,
        "oslo_minimum_history",
        "Oslo has at least ten years of monthly history.",
        "Oslo history is too short for the phase-1 contract.",
        rows=len(ordered),
    )
    recorder.require(
        all(row.get("geo") == "Oslo" for row in ordered),
        "oslo_geo",
        "All total rows are labelled Oslo.",
        "Unexpected geography in Oslo total file.",
        values=sorted({row.get("geo") for row in ordered}),
    )

    mismatches: list[dict[str, Any]] = []
    compared = 0
    for left, right in zip(ordered, ordered[1:]):
        term = number(
            left["ant_husstander_termin"],
            "ant_husstander_termin",
            month_label(left),
        )
        payment = number(
            right["ant_husstander_utbetaling"],
            "ant_husstander_utbetaling",
            month_label(right),
        )
        compared += 1
        if term != payment and len(mismatches) < 10:
            mismatches.append(
                {
                    "term_month": month_label(left),
                    "payment_month": month_label(right),
                    "term": term,
                    "payment": payment,
                }
            )
    recorder.require(
        not mismatches,
        "term_to_payment_identity",
        "Every observable term equals next month's payment count.",
        "Term-to-payment mismatches found.",
        compared_pairs=compared,
        mismatches=mismatches,
    )

    if ordered:
        latest = ordered[-1]
        latest_is_edge = (
            number(
                latest["ant_husstander_termin"],
                "ant_husstander_termin",
                month_label(latest),
            )
            == 0
            and number(
                latest["ant_husstander_utbetaling"],
                "ant_husstander_utbetaling",
                month_label(latest),
            )
            > 0
        )
        if latest_is_edge:
            recorder.emit(
                "passed",
                "latest_realtime_edge",
                "Latest row is the expected unprocessed-term edge.",
                month=month_label(latest),
            )
        else:
            recorder.warn(
                "latest_realtime_edge",
                "Latest row is not the expected unprocessed-term edge; "
                "review the source vintage before modelling.",
                month=month_label(latest),
                term=latest["ant_husstander_termin"],
                payment=latest["ant_husstander_utbetaling"],
            )

    return keyed


def validate_panel(
    recorder: Recorder,
    name: str,
    rows: list[dict[str, str]],
    columns: list[str],
    entity_field: str,
    oslo_by_month: dict[str, dict[str, str]],
) -> None:
    required = MONTHLY_REQUIRED - {"geo"} | {entity_field}
    if name == "bydel":
        required |= {"bydel"}
    else:
        required |= {"geo"}
    if not validate_headers(recorder, name, columns, required):
        return

    validate_numeric_fields(recorder, name, rows, ADDITIVE_MEASURES)

    seen: set[tuple[str, str]] = set()
    duplicates: list[tuple[str, str]] = []
    unknown_months: set[str] = set()
    entities_by_month: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        label = month_label(row)
        entity = row[entity_field]
        key = (entity, label)
        if key in seen:
            duplicates.append(key)
        seen.add(key)
        entities_by_month[label].add(entity)
        if label not in oslo_by_month:
            unknown_months.add(label)

    recorder.require(
        not duplicates,
        f"{name}_unique_key",
        f"{name.capitalize()} keys are unique.",
        f"Duplicate {name} × month keys found.",
        duplicates=duplicates[:10],
    )
    recorder.require(
        not unknown_months,
        f"{name}_known_months",
        f"All {name} months exist in Oslo total.",
        f"{name.capitalize()} contains months outside Oslo total.",
        months=sorted(unknown_months),
    )

    if name == "brukergruppe":
        observed = {row[entity_field] for row in rows}
        recorder.require(
            observed == EXPECTED_GROUPS,
            "group_categories",
            "The five expected user groups are present.",
            "Unexpected or missing user groups.",
            expected=sorted(EXPECTED_GROUPS),
            observed=sorted(observed),
        )
        incomplete = {
            month: sorted(EXPECTED_GROUPS - entities)
            for month, entities in entities_by_month.items()
            if entities != EXPECTED_GROUPS
        }
        recorder.require(
            not incomplete,
            "group_month_coverage",
            "Every month contains all five user groups.",
            "User-group coverage is incomplete.",
            examples=dict(list(incomplete.items())[:10]),
        )

    if name == "bydel":
        invalid_codes = sorted(
            {
                row[entity_field]
                for row in rows
                if not re.fullmatch(r"\d{4}", row[entity_field])
            }
        )
        recorder.require(
            not invalid_codes,
            "bydel_code_format",
            "Bydel codes retain four digits.",
            "Invalid bydel codes found.",
            invalid_codes=invalid_codes,
        )
        missing_core: dict[str, list[str]] = {}
        for month in oslo_by_month:
            missing = EXPECTED_BYDEL_CODES - entities_by_month.get(month, set())
            if missing:
                missing_core[month] = sorted(missing)
        recorder.require(
            not missing_core,
            "bydel_month_coverage",
            "All 15 core bydeler are present every month.",
            "Core bydel coverage is incomplete.",
            examples=dict(list(missing_core.items())[:10]),
        )

    sums: dict[str, dict[str, float]] = {
        field: defaultdict(float) for field in ADDITIVE_MEASURES
    }
    for row in rows:
        label = month_label(row)
        for field in ADDITIVE_MEASURES:
            sums[field][label] += number(row[field], field, label)

    mismatches: list[dict[str, Any]] = []
    for field in ADDITIVE_MEASURES:
        for month, total_row in oslo_by_month.items():
            expected = number(total_row[field], field, month)
            actual = sums[field].get(month, 0.0)
            if abs(actual - expected) > 0.005 and len(mismatches) < 20:
                mismatches.append(
                    {
                        "field": field,
                        "month": month,
                        "expected": expected,
                        "actual": actual,
                    }
                )
    recorder.require(
        not mismatches,
        f"{name}_sums_to_oslo",
        f"All additive {name} measures sum to Oslo total by month.",
        f"{name.capitalize()} sums differ from Oslo total.",
        mismatches=mismatches,
        measures=list(ADDITIVE_MEASURES),
        months=len(oslo_by_month),
    )


def validate_interventions(recorder: Recorder) -> None:
    rows, columns = read_csv(INTERVENTION_FILE, recorder)
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
    if not validate_headers(recorder, "interventions", columns, required):
        return

    ids = [row["id"] for row in rows]
    recorder.require(
        len(ids) == len(set(ids)),
        "intervention_unique_id",
        "Intervention IDs are unique.",
        "Duplicate intervention IDs found.",
        duplicates=sorted({item for item in ids if ids.count(item) > 1}),
    )
    recorder.require(
        len(rows) >= 20,
        "intervention_minimum_rows",
        "Intervention register contains at least 20 events.",
        "Intervention register is unexpectedly short.",
        rows=len(rows),
    )

    invalid_dates: list[dict[str, str]] = []
    blank_sources: list[str] = []
    for row in rows:
        for field in DATE_FIELDS:
            value = row[field].strip()
            if value and not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", value):
                invalid_dates.append(
                    {"id": row["id"], "field": field, "value": value}
                )
        if not row["kilde"].strip():
            blank_sources.append(row["id"])
    recorder.require(
        not invalid_dates,
        "intervention_dates",
        "Intervention dates use YYYY-MM.",
        "Invalid intervention dates found.",
        examples=invalid_dates[:10],
    )
    recorder.require(
        not blank_sources,
        "intervention_sources",
        "Every intervention has a source field.",
        "Interventions without source found.",
        ids=blank_sources,
    )

    partial = [row["id"] for row in rows if row["verifisering"] != "bekreftet"]
    if partial:
        recorder.warn(
            "intervention_partial_verification",
            "Some intervention rows are not fully source-verified.",
            ids=partial,
        )
    else:
        recorder.emit(
            "passed",
            "intervention_partial_verification",
            "All intervention rows are marked source-verified.",
        )


def validate_citations(recorder: Recorder) -> None:
    report_path = ROOT / REPORT_FILE
    bib_path = ROOT / BIB_FILE
    for path in (report_path, bib_path):
        if not path.is_file():
            recorder.emit(
                "error",
                f"file_exists:{path.relative_to(ROOT)}",
                "Required report file is missing.",
            )
            return
        recorder.register_file(path)

    report = report_path.read_text(encoding="utf-8")
    bibliography = bib_path.read_text(encoding="utf-8")

    cited: set[str] = set()
    for bracket in re.findall(r"\[([^\]]*@[^\]]*)\]", report):
        cited.update(
            key.rstrip(";,.")
            for key in re.findall(r"@([A-Za-z][A-Za-z0-9_:.+-]*)", bracket)
        )
    entries = set(
        re.findall(r"@\w+\s*\{\s*([^,\s]+)", bibliography)
    )
    missing = sorted(cited - entries)
    recorder.require(
        not missing,
        "citation_keys",
        "All bracket citation keys exist in the bibliography.",
        "Citation keys are missing from the bibliography.",
        cited=len(cited),
        bibliography_entries=len(entries),
        missing=missing,
    )

    placeholder_count = bibliography.count("PLASSHOLDER")
    if placeholder_count:
        recorder.warn(
            "bibliography_placeholders",
            "Bibliography still contains placeholder markers.",
            occurrences=placeholder_count,
        )
    else:
        recorder.emit(
            "passed",
            "bibliography_placeholders",
            "No placeholder markers remain in the bibliography.",
        )


def validate_required_docs(recorder: Recorder) -> None:
    required = (
        Path("README.md"),
        Path("AGENTS.md"),
        Path("docs/PROJECT.md"),
        Path("docs/STATUS.md"),
        Path("docs/DECISIONS.md"),
        Path("docs/EVIDENCE_REGISTER.md"),
    )
    for relative in required:
        path = ROOT / relative
        if recorder.require(
            path.is_file(),
            f"file_exists:{relative}",
            "Required governance document exists.",
            "Required governance document is missing.",
            path=str(relative),
        ):
            recorder.register_file(path)


def run_validation(recorder: Recorder) -> None:
    validate_required_docs(recorder)

    oslo_rows, oslo_columns = read_csv(OSLO_FILE, recorder)
    bydel_rows, bydel_columns = read_csv(BYDEL_FILE, recorder)
    group_rows, group_columns = read_csv(GROUP_FILE, recorder)

    oslo_by_month = validate_oslo(recorder, oslo_rows, oslo_columns)
    if oslo_by_month:
        validate_panel(
            recorder,
            "bydel",
            bydel_rows,
            bydel_columns,
            "kommunenr",
            oslo_by_month,
        )
        validate_panel(
            recorder,
            "brukergruppe",
            group_rows,
            group_columns,
            "brukergruppe",
            oslo_by_month,
        )

    validate_interventions(recorder)
    validate_citations(recorder)


def write_manifest(path: Path, recorder: Recorder) -> None:
    path = path if path.is_absolute() else ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(recorder.manifest(), ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "event": "manifest_written",
                "run_id": recorder.run_id,
                "path": str(path),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        help="Optional JSON manifest path, relative to repo root by default.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    recorder = Recorder()
    try:
        run_validation(recorder)
    except Exception as exc:  # preserve unexpected failures in the manifest
        recorder.emit(
            "error",
            "validator_exception",
            "Unexpected validator exception.",
            exception_type=type(exc).__name__,
            exception=str(exc),
            traceback=traceback.format_exc(),
        )
    finally:
        summary = recorder.manifest()["summary"]
        print(
            json.dumps(
                {
                    "event": "validation_summary",
                    "run_id": recorder.run_id,
                    **summary,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        if args.manifest:
            write_manifest(args.manifest, recorder)

    return 1 if recorder.errors else 0


if __name__ == "__main__":
    sys.exit(main())
