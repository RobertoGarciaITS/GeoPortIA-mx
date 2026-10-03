from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

import httpx

from .config import InegiSettings


class DenueError(RuntimeError):
    """Error controlado del cliente DENUE."""


@dataclass(frozen=True)
class DenueRecord:
    establishment_id: str
    name: str
    activity: str
    employee_range: str
    latitude: float | None
    longitude: float | None
    municipality: str | None
    raw: dict[str, Any]

    @classmethod
    def from_api(cls, row: dict[str, Any]) -> "DenueRecord":
        def number(value: Any) -> float | None:
            if value in (None, ""):
                return None
            try:
                return float(value)
            except (TypeError, ValueError) as exc:
                raise DenueError(f"Coordenada inválida en registro DENUE: {value!r}") from exc

        return cls(
            establishment_id=str(row.get("Id", "")),
            name=str(row.get("Nombre", "")),
            activity=str(row.get("Clase_actividad", "")),
            employee_range=str(row.get("Estrato", "")),
            latitude=number(row.get("Latitud")),
            longitude=number(row.get("Longitud")),
            municipality=row.get("Ubicacion"),
            raw=dict(row),
        )


class DenueClient:
    """Cliente pequeño y testeable para la API oficial del DENUE."""

    def __init__(self, settings: InegiSettings, http_client: httpx.Client | None = None):
        self.settings = settings
        self._http = http_client or httpx.Client(timeout=settings.timeout_s)

    def _get(self, *parts: object) -> list[dict[str, Any]]:
        if not self.settings.denue_token:
            raise DenueError("Falta INEGI_DENUE_TOKEN; no se ejecuta una consulta real")
        path = "/".join(quote(str(part), safe=",.-_!*()") for part in (*parts, self.settings.denue_token))
        url = self.settings.denue_base_url + path
        try:
            response = self._http.get(url)
        except httpx.HTTPError as exc:
            raise DenueError(f"No se pudo conectar con DENUE: {exc}") from exc
        if response.status_code == 401:
            raise DenueError("DENUE rechazó el token (401)")
        if response.status_code == 429:
            raise DenueError("DENUE indicó límite de consultas (429)")
        if response.status_code >= 400:
            raise DenueError(f"DENUE respondió HTTP {response.status_code}")
        if "no autorizado" in response.text.lower():
            raise DenueError("DENUE rechazó el token: No autorizado")
        try:
            payload = response.json()
        except ValueError as exc:
            raise DenueError("DENUE no devolvió JSON válido") from exc
        if not isinstance(payload, list) or not all(isinstance(row, dict) for row in payload):
            raise DenueError("Respuesta DENUE con formato inesperado")
        return payload

    def search_radius(self, condition: str, latitude: float, longitude: float, meters: int) -> list[DenueRecord]:
        if not condition.strip() or not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180) or not 0 < meters <= 5000:
            raise ValueError("condition, coordenadas y meters deben ser válidos")
        return [DenueRecord.from_api(row) for row in self._get("Buscar", condition, f"{latitude},{longitude}", meters)]

    def search_entity(self, condition: str, entity_code: str, start: int = 1, end: int = 10) -> list[DenueRecord]:
        if not condition.strip() or not entity_code or start < 1 or end < start:
            raise ValueError("Parámetros inválidos para BuscarEntidad")
        return [DenueRecord.from_api(row) for row in self._get("BuscarEntidad", condition, entity_code, start, end)]

    def iter_entity(self, condition: str, entity_code: str, page_size: int = 10, max_pages: int = 100):
        """Itera resultados por ventanas de registros y se detiene al recibir una página corta."""
        if page_size <= 0 or max_pages <= 0:
            raise ValueError("page_size y max_pages deben ser mayores que cero")
        for page in range(max_pages):
            start = page * page_size + 1
            rows = self.search_entity(condition, entity_code, start, start + page_size - 1)
            yield from rows
            if len(rows) < page_size:
                break

    def search_name(self, name: str, entity_code: str, start: int = 1, end: int = 10) -> list[DenueRecord]:
        if not name.strip() or not entity_code or start < 1 or end < start:
            raise ValueError("Parámetros inválidos para Nombre")
        return [DenueRecord.from_api(row) for row in self._get("Nombre", name, entity_code, start, end)]

    def ficha(self, establishment_id: str) -> DenueRecord:
        if not establishment_id.strip():
            raise ValueError("establishment_id es obligatorio")
        rows = self._get("Ficha", establishment_id)
        if not rows:
            raise DenueError("DENUE no encontró el establecimiento")
        return DenueRecord.from_api(rows[0])

    def quantify(self, activity_codes: list[str], geography_codes: list[str], stratum: str = "0") -> list[dict[str, str]]:
        """Cuenta establecimientos por actividad, área geográfica y estrato."""
        if not activity_codes or not geography_codes or stratum not in {"0", "1", "2", "3", "4", "5", "6", "7"}:
            raise ValueError("activity_codes, geography_codes o stratum inválidos")
        rows = self._get("Cuantificar", ",".join(activity_codes), ",".join(geography_codes), stratum)
        result: list[dict[str, str]] = []
        for row in rows:
            if not {"AE", "AG", "Total"} <= row.keys():
                raise DenueError("Respuesta Cuantificar sin columnas AE, AG y Total")
            result.append({"activity_code": str(row["AE"]), "geography_code": str(row["AG"]), "total": str(row["Total"])})
        return result

    def search_area_activity(
        self,
        *,
        entity: str = "0",
        municipality: str = "0",
        locality: str = "0",
        ageb: str = "0",
        block: str = "0",
        sector: str = "0",
        subsector: str = "0",
        branch: str = "0",
        subbranch: str = "0",
        condition: str = "todos",
        start: int = 1,
        end: int = 10,
        stratum: str = "0",
    ) -> list[DenueRecord]:
        """Lista establecimientos por área geoestadística, actividad y estrato."""
        if not condition.strip() or start < 1 or end < start or stratum not in {"0", "1", "2", "3", "4", "5", "6", "7"}:
            raise ValueError("Parámetros inválidos para BuscarAreaAct")
        parts = [
            "BuscarAreaAct", entity, municipality, locality, ageb, block,
            sector, subsector, branch, subbranch, condition, start, end, stratum,
        ]
        return [DenueRecord.from_api(row) for row in self._get(*parts)]
