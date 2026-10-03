"""Carga normalizada de vacantes publicadas por una fuente autorizada."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class VacancyRecord:
    vacancy_id: str
    geography: str
    title: str
    skill: str
    source: str
    published_date: str


REQUIRED_COLUMNS = {"vacancy_id", "geography", "title", "skill", "source", "published_date"}


def load_vacancies_csv(path: str | Path) -> list[VacancyRecord]:
    result: list[VacancyRecord] = []
    with Path(path).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError("Vacantes sin columnas requeridas: " + ", ".join(sorted(missing)))
        for row in reader:
            if not row["vacancy_id"].strip() or not row["geography"].strip() or not row["skill"].strip():
                raise ValueError("Vacante con identificador, geografía o habilidad vacía")
            result.append(VacancyRecord(**{key: row[key] for key in REQUIRED_COLUMNS}))
    return result


def count_demand(records: Iterable[VacancyRecord], geography: str, skill: str) -> int:
    return sum(1 for row in records if row.geography == geography and row.skill.lower() == skill.lower())
