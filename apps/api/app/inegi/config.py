from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class InegiSettings:
    """Configuración sin secretos en código; el token solo se lee del entorno."""

    denue_token: str | None = None
    denue_base_url: str = "https://www.inegi.org.mx/app/api/denue/v1/consulta/"
    timeout_s: float = 20.0

    @classmethod
    def from_env(cls) -> "InegiSettings":
        timeout = os.getenv("INEGI_HTTP_TIMEOUT_S", "20")
        try:
            timeout_s = float(timeout)
        except ValueError as exc:
            raise ValueError("INEGI_HTTP_TIMEOUT_S debe ser numérico") from exc
        if timeout_s <= 0:
            raise ValueError("INEGI_HTTP_TIMEOUT_S debe ser mayor que cero")
        return cls(
            denue_token=os.getenv("INEGI_DENUE_TOKEN") or None,
            denue_base_url=os.getenv(
                "INEGI_DENUE_BASE_URL",
                "https://www.inegi.org.mx/app/api/denue/v1/consulta/",
            ).rstrip("/") + "/",
            timeout_s=timeout_s,
        )
