"""Modelo normalizado para comparar oferta y demanda laboral."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .denue import DenueRecord
from .enoe import EnoeRecord


@dataclass(frozen=True)
class LaborMarketSnapshot:
    geography: str
    skill: str
    technology_establishments: int
    available_talent: float
    employed_talent: float
    demand: float
    demand_source: str
    deficit: float
    scarcity_index: float | None


def build_snapshot(
    *,
    geography: str,
    skill: str,
    enoe_records: Iterable[EnoeRecord],
    denue_records: Iterable[DenueRecord],
    demand: float,
    demand_source: str,
) -> LaborMarketSnapshot:
    """Construye una fotografía agregada sin exponer personas.

    ``demand`` debe venir de vacantes observadas o de un proxy documentado;
    no se inventa desde la encuesta ENOE porque ENOE no es un inventario de vacantes.
    """
    if not geography.strip() or not skill.strip() or demand < 0:
        raise ValueError("geography, skill y demand deben ser válidos")
    if not demand_source.strip():
        raise ValueError("demand_source es obligatorio")
    records = [r for r in enoe_records if r.geography == geography and r.skill == skill]
    establishments = [r for r in denue_records if geography in (r.municipality or "")]
    available = sum(r.expansion_factor for r in records if r.employment_status in {"desempleado", "busca_cambio"})
    employed = sum(r.expansion_factor for r in records if r.employment_status == "ocupado")
    deficit = demand - available
    return LaborMarketSnapshot(
        geography=geography,
        skill=skill,
        technology_establishments=len(establishments),
        available_talent=available,
        employed_talent=employed,
        demand=demand,
        demand_source=demand_source,
        deficit=deficit,
        scarcity_index=(demand / available if available else None),
    )
