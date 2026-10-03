from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class EnoeRecord:
    geography: str
    field_of_study: str
    occupation: str
    employment_status: str
    expansion_factor: float
    skill: str = ""


REQUIRED_COLUMNS = {
    "geography",
    "field_of_study",
    "occupation",
    "employment_status",
    "expansion_factor",
}


def validate_enoe_columns(columns: Iterable[str]) -> None:
    missing = REQUIRED_COLUMNS - set(columns)
    if missing:
        raise ValueError("Extracto ENOE sin columnas requeridas: " + ", ".join(sorted(missing)))


def load_enoe_csv(path: str | Path) -> list[EnoeRecord]:
    """Carga un extracto previamente agregado/anonimizado; no acepta microdatos identificables."""
    result: list[EnoeRecord] = []
    with Path(path).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        validate_enoe_columns(reader.fieldnames or [])
        for row in reader:
            if not row["geography"].strip() or not row["employment_status"].strip():
                raise ValueError("Extracto ENOE con geografía o condición laboral vacía")
            result.append(EnoeRecord(
                geography=row["geography"],
                field_of_study=row["field_of_study"],
                occupation=row["occupation"],
                employment_status=row["employment_status"],
                expansion_factor=float(row["expansion_factor"]),
                skill=row.get("skill", ""),
            ))
    return result


def weighted_summary(records: Iterable[EnoeRecord], geography: str, skill: str) -> dict[str, float]:
    selected = [r for r in records if r.geography == geography and (not skill or r.skill == skill)]
    available = sum(r.expansion_factor for r in selected if r.employment_status in {"desempleado", "busca_cambio"})
    employed = sum(r.expansion_factor for r in selected if r.employment_status == "ocupado")
    return {"available_talent": available, "employed": employed, "records_used": float(len(selected))}
