"""Ejemplo reproducible de oferta AWS con un extracto ENOE anonimizado."""
from __future__ import annotations

import csv
import json
import argparse
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.inegi.denue import DenueRecord
from app.inegi.enoe import load_enoe_csv
from app.inegi.labor import build_snapshot
from app.inegi.vacancies import count_demand, load_vacancies_csv

def main() -> None:
    parser = argparse.ArgumentParser(description="Calcula oferta, demanda y déficit laboral normalizados.")
    parser.add_argument("--enoe", type=Path, default=ROOT / "data" / "sample" / "enoe_extract_saltillo.csv")
    parser.add_argument("--denue", type=Path, default=ROOT / "data" / "sample" / "denue_saltillo_tech.csv")
    parser.add_argument("--vacancies", type=Path, default=ROOT / "data" / "sample" / "sne_vacancies_saltillo.csv")
    parser.add_argument("--geography", default="Saltillo")
    parser.add_argument("--skill", default="AWS")
    args = parser.parse_args()
    path = args.enoe
    denue_path = args.denue
    vacancy_path = args.vacancies
    enoe_rows = load_enoe_csv(path)
    with denue_path.open(encoding="utf-8", newline="") as handle:
        establishments = [
            DenueRecord(
                establishment_id=row["establishment_id"], name=row["name"], activity=row["activity_group"],
                employee_range=row["employee_range"], latitude=None, longitude=None,
                municipality=row["municipality"], raw=dict(row),
            )
            for row in csv.DictReader(handle)
        ]
    snapshot = build_snapshot(
        geography=args.geography,
        skill=args.skill,
        enoe_records=enoe_rows,
        denue_records=establishments,
        demand=count_demand(load_vacancies_csv(vacancy_path), args.geography, args.skill),
        demand_source="SNE_fixture",
    )
    result = {
        "geography": args.geography,
        "skill": args.skill,
        "technology_establishments_fixture": len(establishments),
        "municipalities": sorted({r.municipality for r in establishments if r.municipality}),
        "supply_available_estimate": snapshot.available_talent,
        "employed_with_skill_estimate": snapshot.employed_talent,
        "demand_fixture": snapshot.demand,
        "deficit_fixture": snapshot.deficit,
        "scarcity_index": snapshot.scarcity_index,
        "status": "escasez" if snapshot.deficit > 0 else "equilibrio_o_superavit",
        "warning": "Ejemplo sintético; no es una estimación oficial ni reemplaza ponderadores ENOE ni un inventario de vacantes.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
