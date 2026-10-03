"""Compara escenarios reproducibles de talento AWS en tres ciudades.

Los valores son fixtures sintéticos para validar el modelo, no estadísticas oficiales.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.inegi.denue import DenueRecord  # noqa: E402
from app.inegi.enoe import EnoeRecord  # noqa: E402
from app.inegi.labor import LaborMarketSnapshot, build_snapshot  # noqa: E402


SCENARIOS = {
    "Saltillo": {"establishments": 3, "available": 3, "employed": 3, "demand": 8},
    "Monterrey": {"establishments": 8, "available": 10, "employed": 22, "demand": 18},
    "Guadalajara": {"establishments": 12, "available": 15, "employed": 30, "demand": 12},
}


def _records(city: str, values: dict[str, int]):
    enoe = [
        EnoeRecord(city, "Computación", "Cloud Engineer", "busca_cambio", values["available"], "AWS"),
        EnoeRecord(city, "Computación", "Programador", "ocupado", values["employed"], "AWS"),
    ]
    denue = [
        DenueRecord(f"{city}-{i}", f"Empresa tecnológica {i}", "Tecnología", "11 a 30", None, None, city, {})
        for i in range(1, values["establishments"] + 1)
    ]
    return enoe, denue


def classify(snapshot: LaborMarketSnapshot) -> str:
    if snapshot.scarcity_index is None:
        return "sin oferta observable"
    if snapshot.scarcity_index >= 2:
        return "escasez alta"
    if snapshot.scarcity_index > 1:
        return "escasez moderada"
    return "equilibrio o superávit"


def main() -> None:
    results = []
    for city, values in SCENARIOS.items():
        enoe, denue = _records(city, values)
        snapshot = build_snapshot(
            geography=city,
            skill="AWS",
            enoe_records=enoe,
            denue_records=denue,
            demand=values["demand"],
            demand_source="scenario_fixture",
        )
        results.append({
            "city": city,
            "technology_establishments": snapshot.technology_establishments,
            "available_talent": snapshot.available_talent,
            "employed_talent": snapshot.employed_talent,
            "demand": snapshot.demand,
            "deficit": snapshot.deficit,
            "scarcity_index": snapshot.scarcity_index,
            "expected_result": classify(snapshot),
        })
    print(json.dumps({"skill": "AWS", "synthetic": True, "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
